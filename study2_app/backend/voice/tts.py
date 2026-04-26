"""TTS via Aliyun Dashscope (qwen3-tts-instruct-flash-realtime).

Streaming WebSocket API: text in → PCM chunks out. Returns WAV bytes
(24 kHz mono 16-bit PCM wrapped in a WAV container) so the browser can
play it directly via `<audio>`.
"""
from __future__ import annotations

import base64
import os
import struct
import threading

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


def _wrap_wav(pcm: bytes) -> bytes:
    """Wrap raw PCM (24kHz mono 16-bit) in a WAV container."""
    n = len(pcm)
    byte_rate = _SAMPLE_RATE * _CHANNELS * _BITS // 8
    block_align = _CHANNELS * _BITS // 8
    header = b"RIFF" + struct.pack("<I", 36 + n) + b"WAVE"
    header += b"fmt " + struct.pack(
        "<IHHIIHH", 16, 1, _CHANNELS, _SAMPLE_RATE, byte_rate, block_align, _BITS
    )
    header += b"data" + struct.pack("<I", n)
    return header + pcm


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
