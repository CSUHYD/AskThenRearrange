"""Resilient runner for Study 1 LL ablation.

Wraps test_policy_loop.run_ablation_experiment with:
  - Resume: skips episodes already present in the JSONL log
  - Retry: re-runs an episode on transient connection errors (httpx /
    httpcore / ollama _types.ResponseError); up to 5 attempts with
    exponential backoff.

Usage:
  python scripts/run_study1_ll_resilient.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import test_policy_loop as tpl  # noqa: E402
from test_policy_loop import (  # noqa: E402
    _parse_budget_list, run_policy_episode, _append_jsonl,
)
from data import get_episode  # noqa: E402
from llm_factory import DEFAULT_MODEL, DEFAULT_BASE_URL  # noqa: E402

SAMPLE_INDICES = [0, 7, 14, 21, 28, 34, 41, 48, 55, 62, 68, 75, 82, 89, 96]
BUDGETS = [1, 3, 5, 10]
MODE = "learner_led"
LOG_PATH = PROJECT_ROOT / "logs" / "study1_ll_rerun.jsonl"
DATA_PATH = PROJECT_ROOT / "data" / "scenarios_three_rooms_102.json"

MAX_ATTEMPTS = 6
BACKOFF_BASE = 4  # seconds


def already_done_indices() -> set:
    """Return set of episode indices that have entries for ALL budgets in the log."""
    if not LOG_PATH.exists():
        return set()
    counts: dict = {}
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


def is_transient(exc: BaseException) -> bool:
    name = type(exc).__name__
    msg = str(exc).lower()
    return any(s in name for s in ("ConnectError", "RemoteProtocolError", "ReadError",
                                    "ResponseError", "Timeout"))\
        or "connection refused" in msg or "remoteprotocol" in msg \
        or "server disconnected" in msg or "502" in msg or "503" in msg


def run_one_episode_with_retry(index: int) -> bool:
    episode = get_episode(DATA_PATH, index)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        started = time.perf_counter()
        try:
            _, results_by_budget = run_policy_episode(
                episode=episode,
                budget=max(BUDGETS),
                mode=MODE,
                proposer_model=DEFAULT_MODEL,
                oracle_model=DEFAULT_MODEL,
                updater_model=DEFAULT_MODEL,
                evaluation_model=DEFAULT_MODEL,
                base_url=DEFAULT_BASE_URL,
                verbose=False,
                selection_method="rule",
                eval_budgets=BUDGETS,
            )
            elapsed = time.perf_counter() - started
            for b in BUDGETS:
                ev = results_by_budget[b]
                _append_jsonl(LOG_PATH, {
                    "event": "episode_finished",
                    "mode": MODE,
                    "budget": b,
                    "episode_index": index,
                    "episode_id": episode.episode_id,
                    "elapsed_sec": elapsed,
                    "seen_accuracy": float(ev["seen_accuracy"]),
                    "unseen_accuracy": float(ev["unseen_accuracy"]),
                })
            print(f"[ep_idx={index}] DONE ({elapsed:.0f}s, attempt={attempt})", flush=True)
            return True
        except Exception as e:
            if not is_transient(e) or attempt == MAX_ATTEMPTS:
                print(f"[ep_idx={index}] FAILED attempt {attempt}/{MAX_ATTEMPTS}: "
                      f"{type(e).__name__}: {str(e)[:200]}", flush=True)
                if attempt == MAX_ATTEMPTS:
                    return False
                raise
            wait = BACKOFF_BASE * (2 ** (attempt - 1))
            print(f"[ep_idx={index}] transient {type(e).__name__} on attempt {attempt}, "
                  f"sleeping {wait}s ...", flush=True)
            time.sleep(wait)
    return False


def main():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        _append_jsonl(LOG_PATH, {
            "event": "ablation_started",
            "sample_indices": SAMPLE_INDICES,
            "budgets": BUDGETS,
            "modes": [MODE],
        })

    done = already_done_indices()
    todo = [i for i in SAMPLE_INDICES if i not in done]
    print(f"[init] done={sorted(done)} todo={todo}", flush=True)

    failed = []
    for i, index in enumerate(todo):
        print(f"\n[{i+1}/{len(todo)}] starting ep_idx={index}", flush=True)
        ok = run_one_episode_with_retry(index)
        if not ok:
            failed.append(index)

    print(f"\n[done] failed={failed}", flush=True)


if __name__ == "__main__":
    main()
