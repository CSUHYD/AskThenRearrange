"""Simulation comparing Study 2 UL and LL on Qwen3.

10 episodes (sampled from data/scenarios_three_rooms_102.json so we have
ground-truth placements + annotator notes for the oracle) × budgets
[1, 3, 5, 10] × {UL, LL}. UL turn-0 hardcoded probe is disabled so we
measure the natural candidate-selection path without info-dump artefact.
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

# Env BEFORE llm_factory import
os.environ.setdefault("LLM_BACKEND", "ollama")
os.environ.setdefault("LLM_MODEL", "qwen3")
os.environ["LLM_BASE_URL"] = "http://110.42.252.68:8080"
os.environ["OLLAMA_HOST"] = "http://110.42.252.68:8080"
for v in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
          "all_proxy", "ALL_PROXY"):
    os.environ.pop(v, None)
os.environ["NO_PROXY"] = "localhost,127.0.0.1,110.42.252.68"
os.environ["no_proxy"] = os.environ["NO_PROXY"]

from agent_schema import AgentState  # noqa: E402
from data import get_episode  # noqa: E402
from evaluation import FinalPlacementPlanner, evaluate_episode_state  # noqa: E402
from llm_factory import DEFAULT_MODEL, DEFAULT_BASE_URL  # noqa: E402
from oracle import NaturalUserOracle  # noqa: E402
from proposers import ActionProposer, PreferenceInductionProposer  # noqa: E402
from question_policy import QuestionDecision, QuestionPolicyController  # noqa: E402
from state_init import build_initial_state  # noqa: E402
from state_update import StateUpdate  # noqa: E402
from study2_app.backend.pe_proposer_study2 import Study2PreferenceElicitingProposer  # noqa: E402
from study2_app.backend.pi_proposer_study2 import Study2PreferenceInductionProposer  # noqa: E402
from study2_app.backend.policy_study2 import Study2QuestionPolicyController  # noqa: E402

# Use the simulation-grade dataset (102 episodes with placements + notes).
DATA_PATH = PROJECT_ROOT / "data" / "scenarios_three_rooms_102.json"
SAMPLE_INDICES = [0, 7, 14, 21, 28, 34, 41, 48, 68, 75]  # 4 living + 3 bedroom + 3 kitchen
BUDGETS = [1, 3, 5, 10]
LOG_PATH = PROJECT_ROOT / "logs" / "sim_ul_vs_ll_qwen3.jsonl"

MAX_ATTEMPTS = 6
BACKOFF_BASE = 4


def is_transient(exc: BaseException) -> bool:
    name = type(exc).__name__
    msg = str(exc).lower()
    return any(s in name for s in ("ConnectError", "RemoteProtocolError",
                                    "ReadError", "ResponseError", "Timeout",
                                    "APIConnectionError"))\
        or "connection" in msg or "remote" in msg or "timeout" in msg \
        or "502" in msg or "503" in msg or "504" in msg


def _propose(state, decision, *, ao, pe, pi):
    if decision.question_pattern == "preference_eliciting":
        return pe.propose(state=state, guidance=decision.guidance)
    if decision.question_pattern == "action_oriented":
        return ao.propose(state=state, guidance=decision.guidance)
    if decision.question_pattern == "preference_induction":
        intents = pi.propose(state=state, max_intents=3, guidance=decision.guidance)
        return intents[0] if intents else None
    return None


def run_one(*, episode, mode, controller, ao, pe, pi, updater, oracle, planner):
    state: AgentState = build_initial_state(
        episode=episode, strategy=mode, budget_total=max(BUDGETS),
    )
    eval_set = set(BUDGETS)
    results = {}
    fb = 0
    while len(state["qa_history"]) < max(BUDGETS):
        decision = controller.plan_next_question(state=state, mode=mode)
        if decision is None:
            break
        intent = _propose(state, decision, ao=ao, pe=pe, pi=pi)
        if intent is None and decision.question_pattern in ("preference_induction", "preference_eliciting"):
            fb += 1
            decision = QuestionDecision(question_pattern="action_oriented",
                                        guidance="fallback")
            intent = _propose(state, decision, ao=ao, pe=pe, pi=pi)
        if intent is None:
            break
        question = intent.question if hasattr(intent, "question") else str(intent.get("question", ""))
        ans = oracle.answer(
            question=question, room=state["room"],
            receptacles=state["receptacles"],
            seen_objects=state["seen_objects"],
            annotator_notes=episode.annotator_notes,
            gt_seen_placements=episode.seen_placements,
            qa_history=state["qa_history"],
        )
        if decision.question_pattern == "preference_eliciting":
            state = updater.update_state_from_preference_eliciting_answer(
                state=state, hypothesis=str(intent.get("hypothesis", "")),
                covered_objects=list(intent.get("covered_objects", [])),
                answer=ans.answer, question=question,
                oracle_receptacle=ans.referenced_receptacle,
            )
        elif decision.question_pattern == "action_oriented":
            state = updater.update_state_from_action_answer(
                state=state, target=intent.object_name,
                answer=ans.answer, question=intent.question,
                action_mode=intent.action_mode,
            )
        elif decision.question_pattern == "preference_induction":
            state = updater.update_state_from_preference_induction_answer(
                state=state, hypothesis=str(intent.get("hypothesis", "")),
                covered_objects=list(intent.get("covered_objects", [])),
                answer=ans.answer, question=question,
            )
        b = len(state["qa_history"])
        if b in eval_set:
            ev = evaluate_episode_state(episode, state, planner=planner)
            ev["qa_history"] = list(state["qa_history"])
            ev["confirmed_actions"] = list(state["confirmed_actions"])
            ev["confirmed_preferences"] = list(state["confirmed_preferences"])
            results[b] = ev
    for b in BUDGETS:
        if b not in results:
            ev = evaluate_episode_state(episode, state, planner=planner)
            ev["qa_history"] = list(state["qa_history"])
            ev["confirmed_actions"] = list(state["confirmed_actions"])
            ev["confirmed_preferences"] = list(state["confirmed_preferences"])
            results[b] = ev
    return results, fb


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
            if rec.get("event") == "episode_finished":
                key = (rec["mode"], rec["episode_index"])
                counts[key] = counts.get(key, 0) + 1
    # require all budgets present per (mode, ep)
    return {key for key, n in counts.items() if n >= len(BUDGETS)}


def _append(obj):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def run_pair(idx: int, mode: str, *, components):
    episode = get_episode(DATA_PATH, idx)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        t0 = time.perf_counter()
        try:
            results, fb = run_one(episode=episode, mode=mode, **components)
            elapsed = time.perf_counter() - t0
            for b in BUDGETS:
                ev = results[b]
                _append({
                    "event": "episode_finished",
                    "mode": mode,
                    "budget": b,
                    "episode_index": idx,
                    "episode_id": episode.episode_id,
                    "room": episode.room,
                    "elapsed_sec": elapsed,
                    "fallback_count": fb,
                    "seen_accuracy": float(ev["seen_accuracy"]),
                    "unseen_accuracy": float(ev["unseen_accuracy"]),
                    "qa_history": ev.get("qa_history", []),
                })
            print(f"[{mode}/ep_{idx}] DONE ({elapsed:.0f}s, attempt={attempt}, fb={fb}) "
                  + " ".join(f"u@{b}={results[b]['unseen_accuracy']*100:.0f}" for b in BUDGETS),
                  flush=True)
            return True
        except Exception as e:
            if not is_transient(e) or attempt == MAX_ATTEMPTS:
                print(f"[{mode}/ep_{idx}] FAILED {type(e).__name__}: {str(e)[:150]}", flush=True)
                if attempt == MAX_ATTEMPTS:
                    return False
                raise
            wait = BACKOFF_BASE * (2 ** (attempt - 1))
            print(f"[{mode}/ep_{idx}] transient {type(e).__name__} attempt {attempt}, "
                  f"sleep {wait}s ...", flush=True)
            time.sleep(wait)
    return False


def main():
    print(f"[init] backend={DEFAULT_MODEL} @ {DEFAULT_BASE_URL}", flush=True)
    print(f"[init] data={DATA_PATH}", flush=True)
    if not LOG_PATH.exists():
        _append({
            "event": "ablation_started",
            "sample_indices": SAMPLE_INDICES,
            "budgets": BUDGETS,
            "modes": ["user_led", "learner_led"],
            "model": DEFAULT_MODEL,
            "skip_turn0_probe": True,
        })

    # Components — Study 2 controllers/proposers, UL skips turn-0 probe.
    components = {
        "controller": Study2QuestionPolicyController(selection_method="rule"),
        "ao": ActionProposer(),
        "pe": Study2PreferenceElicitingProposer(skip_turn0_probe=True),
        "pi": Study2PreferenceInductionProposer(),
        "updater": StateUpdate(),
        "oracle": NaturalUserOracle(),
        "planner": FinalPlacementPlanner(),
    }
    # UL needs parent class controller for _rule_user_led; LL needs Study 2 ctrl.
    parent_controller = QuestionPolicyController(selection_method="rule")

    done = already_done()
    print(f"[init] done={len(done)} pairs", flush=True)
    todo: List[tuple] = [(m, i) for m in ("user_led", "learner_led")
                                for i in SAMPLE_INDICES
                                if (m, i) not in done]
    print(f"[init] todo={len(todo)} pairs", flush=True)

    for mode, idx in todo:
        # Use parent controller for UL, Study 2 controller for LL.
        comps = dict(components)
        comps["controller"] = parent_controller if mode == "user_led" else components["controller"]
        run_pair(idx, mode, components=comps)

    print(f"\n[done] log={LOG_PATH}", flush=True)


if __name__ == "__main__":
    main()
