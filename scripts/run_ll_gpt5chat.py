"""Run new-version Study 1 LL on GPT-5-Chat with full QA logging.

Records per-turn (pattern, hypothesis, question, answer) and per-budget state
snapshot (confirmed_actions, confirmed_preferences) so we can analyse the
dialogue qualitatively in addition to the PSR table.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Hardcode env BEFORE importing llm_factory so DEFAULT_* picks them up.
os.environ["LLM_BACKEND"] = "openai"
os.environ["LLM_MODEL"] = "gpt-5-chat"
os.environ["LLM_BASE_URL"] = "https://api.gptsapi.net/v1"
os.environ["LLM_API_KEY"] = "sk-SBW375246ecb7151533516297e5c382b866154a68fdfd9uZ"
for v in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
          "all_proxy", "ALL_PROXY"):
    os.environ.pop(v, None)
os.environ["NO_PROXY"] = "localhost,127.0.0.1,api.gptsapi.net"
os.environ["no_proxy"] = os.environ["NO_PROXY"]

from llm_factory import DEFAULT_MODEL, DEFAULT_BASE_URL  # noqa: E402
from data import get_episode  # noqa: E402
from test_policy_loop import run_policy_episode, _append_jsonl  # noqa: E402

# 10 episodes spread across rooms (4 living + 3 bedroom + 3 kitchen)
SAMPLE_INDICES = [0, 7, 14, 21, 34, 41, 48, 68, 75, 82]
BUDGETS = [1, 3, 10]
MODE = "learner_led"
LOG_PATH = PROJECT_ROOT / "logs" / "ll_gpt5chat_10ep.jsonl"
DATA_PATH = PROJECT_ROOT / "data" / "scenarios_three_rooms_102.json"

MAX_ATTEMPTS = 6
BACKOFF_BASE = 4


def is_transient(exc: BaseException) -> bool:
    name = type(exc).__name__
    msg = str(exc).lower()
    return any(s in name for s in ("ConnectError", "RemoteProtocolError",
                                    "ReadError", "ResponseError", "Timeout",
                                    "APIConnectionError", "RateLimit"))\
        or "connection" in msg or "remote" in msg or "timeout" in msg \
        or "rate limit" in msg or "502" in msg or "503" in msg or "504" in msg


def already_done() -> set:
    if not LOG_PATH.exists():
        return set()
    counts = {}
    with LOG_PATH.open() as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("event") == "episode_finished" and rec.get("mode") == MODE:
                idx = rec.get("episode_index")
                counts[idx] = counts.get(idx, 0) + 1
    return {idx for idx, n in counts.items() if n >= len(BUDGETS)}


def run_one(index: int) -> bool:
    episode = get_episode(DATA_PATH, index)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        started = time.perf_counter()
        try:
            _, results = run_policy_episode(
                episode=episode, budget=max(BUDGETS), mode=MODE,
                proposer_model=DEFAULT_MODEL, oracle_model=DEFAULT_MODEL,
                updater_model=DEFAULT_MODEL, evaluation_model=DEFAULT_MODEL,
                base_url=DEFAULT_BASE_URL, verbose=False,
                selection_method="rule", eval_budgets=BUDGETS,
            )
            elapsed = time.perf_counter() - started
            for b in BUDGETS:
                ev = results[b]
                _append_jsonl(LOG_PATH, {
                    "event": "episode_finished",
                    "mode": MODE,
                    "budget": b,
                    "episode_index": index,
                    "episode_id": episode.episode_id,
                    "room": episode.room,
                    "elapsed_sec": elapsed,
                    "seen_accuracy": float(ev["seen_accuracy"]),
                    "unseen_accuracy": float(ev["unseen_accuracy"]),
                    "qa_history": ev.get("qa_history", []),
                    "confirmed_actions": ev.get("confirmed_actions", []),
                    "confirmed_preferences": ev.get("confirmed_preferences", []),
                })
            print(f"[ep_idx={index}] DONE ({elapsed:.0f}s, attempt={attempt}) "
                  f"PSR@1=u{results[1]['unseen_accuracy']*100:.0f} "
                  f"@3=u{results[3]['unseen_accuracy']*100:.0f} "
                  f"@10=u{results[10]['unseen_accuracy']*100:.0f}",
                  flush=True)
            return True
        except Exception as e:
            if not is_transient(e) or attempt == MAX_ATTEMPTS:
                print(f"[ep_idx={index}] FAILED attempt {attempt}/{MAX_ATTEMPTS}: "
                      f"{type(e).__name__}: {str(e)[:200]}", flush=True)
                if attempt == MAX_ATTEMPTS:
                    return False
                raise
            wait = BACKOFF_BASE * (2 ** (attempt - 1))
            print(f"[ep_idx={index}] transient {type(e).__name__} attempt "
                  f"{attempt}, sleep {wait}s ...", flush=True)
            time.sleep(wait)
    return False


def main():
    print(f"[init] backend={DEFAULT_MODEL} @ {DEFAULT_BASE_URL}", flush=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        _append_jsonl(LOG_PATH, {
            "event": "ablation_started",
            "sample_indices": SAMPLE_INDICES,
            "budgets": BUDGETS,
            "mode": MODE,
            "model": DEFAULT_MODEL,
            "base_url": DEFAULT_BASE_URL,
        })
    done = already_done()
    todo = [i for i in SAMPLE_INDICES if i not in done]
    print(f"[init] done={sorted(done)} todo={todo}", flush=True)
    failed = []
    for i, idx in enumerate(todo):
        print(f"\n[{i+1}/{len(todo)}] starting ep_idx={idx}", flush=True)
        ok = run_one(idx)
        if not ok:
            failed.append(idx)
    print(f"\n[done] failed={failed}", flush=True)


if __name__ == "__main__":
    main()
