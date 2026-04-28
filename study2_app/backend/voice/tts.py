"""TTS via Aliyun Dashscope (qwen3-tts-instruct-flash-realtime).

Streaming WebSocket API: text in → PCM chunks out. Returns WAV bytes
(24 kHz mono 16-bit PCM wrapped in a WAV container) so the browser can
play it directly via `<audio>`.
"""
from __future__ import annotations

import base64
import os
import queue
import struct
import threading
from typing import Iterator

import dashscope
from dashscope.audio.qwen_tts_realtime import (
    AudioFormat,
    QwenTtsRealtime,
    QwenTtsRealtimeCallback,
)

DASHSCOPE_API_KEY = os.environ.get(
    "DASHSCOPE_API_KEY", "sk-515fc7843e934051bc2d59978fc9e030"
)
dashscope.api_key = DASHSCOPE_API_KEY

_SAMPLE_RATE = 24000
_CHANNELS = 1
_BITS = 16


class _CollectorCallback(QwenTtsRealtimeCallback):
    """Collects all `response.audio.delta` chunks until `session.finished`."""

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[bytes] = []
        self._done = threading.Event()
        self._error: str | None = None

    def on_open(self) -> None:
        pass

    def on_close(self, close_status_code, close_msg) -> None:
        # set in case the server hangs up before session.finished
        self._done.set()

    def on_event(self, response) -> None:
        try:
            t = response.get("type") if isinstance(response, dict) else None
            if t == "response.audio.delta":
                self._chunks.append(base64.b64decode(response["delta"]))
            elif t == "session.finished":
                self._done.set()
            elif t == "error":
                err = response.get("error") or {}
                self._error = err.get("message") if isinstance(err, dict) else str(err)
                self._done.set()
        except Exception as e:  # pragma: no cover — defensive
            self._error = str(e)
            self._done.set()

    def collect(self, timeout: float = 30.0) -> bytes:
        if not self._done.wait(timeout=timeout):
            raise RuntimeError("TTS timeout waiting for session.finished")
        if self._error:
            raise RuntimeError(f"TTS error: {self._error}")
        return b"".join(self._chunks)


def _wav_header(data_size: int) -> bytes:
    """Build a 44-byte WAV header for a PCM stream of ``data_size`` bytes.

    For streaming (size unknown at start) pass a sentinel like ``2**31 - 1``
    so the header parses; browsers tolerate over-declared length and stop
    when the stream ends.
    """
    byte_rate = _SAMPLE_RATE * _CHANNELS * _BITS // 8
    block_align = _CHANNELS * _BITS // 8
    header = b"RIFF" + struct.pack("<I", 36 + data_size) + b"WAVE"
    header += b"fmt " + struct.pack(
        "<IHHIIHH", 16, 1, _CHANNELS, _SAMPLE_RATE, byte_rate, block_align, _BITS
    )
    header += b"data" + struct.pack("<I", data_size)
    return header


def _wrap_wav(pcm: bytes) -> bytes:
    """Wrap raw PCM (24kHz mono 16-bit) in a WAV container (one-shot)."""
    return _wav_header(len(pcm)) + pcm


class _StreamingCallback(QwenTtsRealtimeCallback):
    """Pushes each PCM chunk into a queue as soon as it arrives."""

    def __init__(self) -> None:
        super().__init__()
        self._q: "queue.Queue[bytes | None]" = queue.Queue()
        self._error: str | None = None

    def on_open(self) -> None:
        pass

    def on_close(self, close_status_code, close_msg) -> None:
        self._q.put(None)

    def on_event(self, response) -> None:
        try:
            t = response.get("type") if isinstance(response, dict) else None
            if t == "response.audio.delta":
                self._q.put(base64.b64decode(response["delta"]))
            elif t == "session.finished":
                self._q.put(None)
            elif t == "error":
                err = response.get("error") or {}
                self._error = err.get("message") if isinstance(err, dict) else str(err)
                self._q.put(None)
        except Exception as e:  # pragma: no cover
            self._error = str(e)
            self._q.put(None)

    def chunks(self, timeout: float = 30.0) -> Iterator[bytes]:
        while True:
            try:
                item = self._q.get(timeout=timeout)
            except queue.Empty:
                raise RuntimeError("TTS timeout waiting for next chunk")
            if item is None:
                if self._error:
                    raise RuntimeError(f"TTS error: {self._error}")
                return
            yield item


def synthesize_stream(
    text: str,
    *,
    voice: str = "longxiaochun",
    model: str = "cosyvoice-v1",
    retries: int = 2,
) -> Iterator[bytes]:
    """Yield MP3 audio bytes for ``text``.

    Uses Dashscope cosyvoice-v1 HTTP API (one-shot synth) instead of the
    qwen3-tts realtime WebSocket — empirically the WS endpoint fails to
    connect in <5s on roughly 80% of attempts (5/6 in our diagnostic), so
    even though it offers real-time chunks, the perceived latency is much
    worse. cosyvoice-v1 returns the whole MP3 in 3-8s but is 100% reliable.
    Yielded as a single chunk via FastAPI StreamingResponse so the HTTP
    layer can flush it as soon as it's ready.
    """
    if not DASHSCOPE_API_KEY:
        raise RuntimeError("DASHSCOPE_API_KEY not set.")
    if not text.strip():
        raise ValueError("text must not be empty")
    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            from dashscope.audio.tts_v2 import SpeechSynthesizer
            synthesizer = SpeechSynthesizer(model=model, voice=voice)
            audio = synthesizer.call(text)
            if not audio:
                raise RuntimeError(f"empty audio for text='{text[:60]}'")
            yield audio
            return
        except Exception as e:
            last_exc = e
            if attempt < retries:
                import time as _time
                _time.sleep(0.5)
            continue
    raise RuntimeError(f"Dashscope TTS failed after {retries} attempts: {last_exc}")


def _synthesize_once(text: str, *, voice: str, model: str) -> bytes:
    cb = _CollectorCallback()
    rt = QwenTtsRealtime(model=model, callback=cb)
    rt.connect()
    rt.update_session(
        voice=voice,
        response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
        mode="server_commit",
    )
    rt.append_text(text)
    rt.finish()
    pcm = cb.collect(timeout=30.0)
    if not pcm:
        raise RuntimeError(f"empty audio for text='{text[:60]}'")
    return _wrap_wav(pcm)


def synthesize(
    text: str,
    *,
    voice: str = "Cherry",
    model: str = "qwen3-tts-instruct-flash-realtime",
    retries: int = 3,
) -> bytes:
    """Synthesize ``text`` to WAV bytes via Dashscope qwen3-tts realtime.

    Retries up to ``retries`` times on transient WebSocket failures (the
    realtime endpoint occasionally fails to establish a connection within
    its 5s window).
    """
    if not DASHSCOPE_API_KEY:
        raise RuntimeError("DASHSCOPE_API_KEY not set.")
    if not text.strip():
        raise ValueError("text must not be empty")

    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return _synthesize_once(text, voice=voice, model=model)
        except Exception as e:  # transient: ws connect timeout, etc.
            last_exc = e
            if attempt < retries:
                import time as _time
                _time.sleep(0.5 * attempt)  # 0.5s, 1.0s backoff
            continue
    raise RuntimeError(
        f"Dashscope TTS failed after {retries} attempts: {last_exc}"
    )
