"""Simulate 5 participants going through the full Study 2 frontend flow.

Hits every endpoint the React frontend exercises so any contract / state-
machine bug surfaces. Captures errors per participant + step.
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback
from pathlib import Path

import requests

for v in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
          "all_proxy", "ALL_PROXY"):
    os.environ.pop(v, None)

BACKEND = "http://127.0.0.1:8000"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TIMEOUT = 60

PARTICIPANTS = ["P01", "P05", "P09", "P13", "P17"]  # one per Latin row 1-5


def post(path: str, json_body: dict | None = None, *, expect: int = 200) -> dict:
    r = requests.post(f"{BACKEND}{path}", json=json_body or {}, timeout=TIMEOUT)
    if r.status_code != expect:
        raise RuntimeError(f"POST {path} → {r.status_code}: {r.text[:200]}")
    return r.json() if r.content else {}


def get(path: str, *, expect: int = 200) -> dict:
    r = requests.get(f"{BACKEND}{path}", timeout=TIMEOUT)
    if r.status_code != expect:
        raise RuntimeError(f"GET {path} → {r.status_code}: {r.text[:200]}")
    return r.json() if r.content else {}


def fake_answer_for(question: str, receptacles: list[str], seen_objects: list[str]) -> str:
    """Return a plausible Chinese-ish answer that mentions one receptacle."""
    rec = receptacles[0] if receptacles else "桌面"
    obj = seen_objects[0] if seen_objects else "物品"
    if "?" in question or "？" in question:
        # Simulate a confirming/redirecting answer.
        return f"我一般把这类东西放在{rec}里。"
    return f"我会把{obj}放在{rec}里。"


def run_participant(pid: str) -> dict:
    issues: list[dict] = []
    t0 = time.perf_counter()
    log = {"participant_id": pid, "issues": issues}

    # 1. Create session
    s = post("/sessions", {"participant_id": pid, "notes": "e2e"})
    sid = s["session_id"]
    log["session_id"] = sid
    log["latin_square_row"] = s["latin_square_row"]
    log["trial_order"] = s["trial_order"]

    # 2. Three trials
    for trial_idx in range(3):
        config = s["trial_order"][trial_idx]
        room = config["room_type"]
        strategy = config["strategy"]
        try:
            # 2a. Load scene (episode_index 0)
            s = post(f"/sessions/{sid}/trial",
                     {"room_type": room, "episode_index": 0})
            trial = s["trials"][trial_idx]

            # 2b. Start dialogue → first question
            q = post(f"/dialogue/{sid}/start")
            turn = 0

            # 2c. Answer loop (cap 999 = effectively no cap; safety net only).
            while not q.get("dialogue_complete") and turn < 999:
                turn += 1
                ans = fake_answer_for(
                    q.get("question", ""),
                    trial["receptacles"],
                    trial["seen_objects"],
                )
                q = post(f"/dialogue/{sid}/answer", {"answer": ans})

            # 2d. Stop dialogue (mimic experimenter's "结束对话" button)
            if not q.get("dialogue_complete"):
                s = post(f"/dialogue/{sid}/stop")
            else:
                s = get(f"/sessions/{sid}")

            # 2e. Submit preference form — assign every object to first receptacle
            trial = s["trials"][trial_idx]
            assignments = {
                obj: trial["receptacles"][0]
                for obj in (trial["seen_objects"] + trial["unseen_objects"])
            }
            s = post(f"/sessions/{sid}/preference_form",
                     {"assignments": assignments})

            # 2f. Compute score
            score = post(f"/sessions/{sid}/score")
            s = get(f"/sessions/{sid}")
            log.setdefault("trial_results", []).append({
                "trial": trial_idx + 1,
                "room": room,
                "strategy": strategy,
                "turns": turn,
                "seen_psr": score["seen_psr"],
                "unseen_psr": score["unseen_psr"],
                "total_psr": score["total_psr"],
            })
        except Exception as e:
            issues.append({
                "trial": trial_idx + 1,
                "room": room,
                "strategy": strategy,
                "where": "dialogue/score",
                "error": str(e),
                "trace": traceback.format_exc(),
            })

    # 3. Final ranking
    try:
        s = post(f"/sessions/{sid}/final_ranking",
                 {"strategy_ranking": ["UL", "TO", "LL"], "comment": "e2e test"})
        log["final_phase"] = s.get("phase")
    except Exception as e:
        issues.append({"where": "final_ranking", "error": str(e)})

    log["elapsed_sec"] = time.perf_counter() - t0
    return log


def main():
    print(f"[e2e] backend={BACKEND}", flush=True)
    h = get("/health")
    print(f"[e2e] /health → {h}", flush=True)
    results = []
    for pid in PARTICIPANTS:
        print(f"\n[e2e] === {pid} ===", flush=True)
        try:
            log = run_participant(pid)
        except Exception as e:
            log = {"participant_id": pid,
                   "issues": [{"where": "session_create",
                               "error": str(e),
                               "trace": traceback.format_exc()}]}
        results.append(log)
        n_issues = len(log.get("issues", []))
        print(f"[e2e] {pid} done in {log.get('elapsed_sec', 0):.0f}s, "
              f"issues={n_issues}", flush=True)
        for it in log.get("issues", []):
            print(f"      - {it.get('where')}: {it.get('error', '')[:200]}",
                  flush=True)
        for tr in log.get("trial_results", []):
            print(f"      - trial {tr['trial']} ({tr['strategy']}/{tr['room']}): "
                  f"turns={tr['turns']} u={tr['unseen_psr']*100:.0f}% "
                  f"s={tr['seen_psr']*100:.0f}%", flush=True)

    out = PROJECT_ROOT / "logs" / "e2e_5_participants.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"\n[e2e] wrote {out}", flush=True)

    total_issues = sum(len(r.get("issues", [])) for r in results)
    print(f"[e2e] total issues across {len(results)} participants: {total_issues}",
          flush=True)


if __name__ == "__main__":
    main()
