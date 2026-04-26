"""Run UL on GPT-5-Chat with full QA logging.

UL = User-Led: PE proposer dominates, AO for boundary cases.
Uses Study 2 PE proposer (debiased, no RC-first preference) but parent class
QuestionPolicyController + parent _rule_user_led for selection.

5 episodes × budgets [1, 3, 5, 10].
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ["LLM_BACKEND"] = "openai"
os.environ["LLM_MODEL"] = "gpt-5-chat"
os.environ["LLM_BASE_URL"] = "https://api.gptsapi.net/v1"
os.environ["LLM_API_KEY"] = "sk-SBW375246ecb7151533516297e5c382b866154a68fdfd9uZ"
for v in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
          "all_proxy", "ALL_PROXY"):
    os.environ.pop(v, None)
os.environ["NO_PROXY"] = "localhost,127.0.0.1,api.gptsapi.net"
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

SAMPLE_INDICES = [0, 17, 34, 51, 68]
BUDGETS = [1, 3, 5, 10]
MODE = "user_led"
LOG_PATH = PROJECT_ROOT / "logs" / "ul_gpt5chat_5ep_b1-3-5-10.jsonl"
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


def _propose(state, decision, *, ao, pe, pi):
    if decision.question_pattern == "preference_eliciting":
        return pe.propose(state=state, guidance=decision.guidance)
    if decision.question_pattern == "action_oriented":
        return ao.propose(state=state, guidance=decision.guidance)
    if decision.question_pattern == "preference_induction":
        intents = pi.propose(state=state, max_intents=3, guidance=decision.guidance)
        return intents[0] if intents else None
    return None


def run_one(episode, *, controller, ao, pe, pi, updater, oracle, planner):
    state: AgentState = build_initial_state(
        episode=episode, strategy="user_led", budget_total=max(BUDGETS),
    )
    eval_set = set(BUDGETS)
    results = {}
    fb_count = 0
    while len(state["qa_history"]) < max(BUDGETS):
        decision = controller.plan_next_question(state=state, mode=MODE)
        if decision is None:
            break
        intent = _propose(state, decision, ao=ao, pe=pe, pi=pi)
        if intent is None and decision.question_pattern == "preference_eliciting":
            fb_count += 1
            decision = QuestionDecision(question_pattern="action_oriented",
                                        guidance="PE fallback.")
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
    return results, fb_count


def run_episode_with_retry(index, *, components):
    episode = get_episode(DATA_PATH, index)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        started = time.perf_counter()
        try:
            results, fb = run_one(episode, **components)
            elapsed = time.perf_counter() - started
            for b in BUDGETS:
                ev = results[b]
                _append({
                    "event": "episode_finished",
                    "mode": MODE,
                    "budget": b,
                    "episode_index": index,
                    "episode_id": episode.episode_id,
                    "room": episode.room,
                    "elapsed_sec": elapsed,
                    "fallback_count": fb,
                    "seen_accuracy": float(ev["seen_accuracy"]),
                    "unseen_accuracy": float(ev["unseen_accuracy"]),
                    "qa_history": ev.get("qa_history", []),
                    "confirmed_actions": ev.get("confirmed_actions", []),
                    "confirmed_preferences": ev.get("confirmed_preferences", []),
                })
            print(f"[ep_idx={index}] DONE ({elapsed:.0f}s, attempt={attempt}, fb={fb}) "
                  + " ".join(f"u@{b}={results[b]['unseen_accuracy']*100:.0f}" for b in BUDGETS),
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


def _append(obj):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def main():
    print(f"[init] backend={DEFAULT_MODEL} @ {DEFAULT_BASE_URL}", flush=True)
    if not LOG_PATH.exists():
        _append({
            "event": "ablation_started",
            "sample_indices": SAMPLE_INDICES,
            "budgets": BUDGETS,
            "mode": MODE,
            "controller": "QuestionPolicyController (parent, UL via _rule_user_led)",
            "pe_proposer": "Study2PreferenceElicitingProposer",
            "model": DEFAULT_MODEL,
        })
    components = {
        "controller": QuestionPolicyController(selection_method="rule"),
        "ao": ActionProposer(),
        "pe": Study2PreferenceElicitingProposer(),
        "pi": PreferenceInductionProposer(),  # unused in UL but harmless
        "updater": StateUpdate(),
        "oracle": NaturalUserOracle(),
        "planner": FinalPlacementPlanner(),
    }
    done = already_done()
    todo = [i for i in SAMPLE_INDICES if i not in done]
    print(f"[init] done={sorted(done)} todo={todo}", flush=True)
    failed = []
    for i, idx in enumerate(todo):
        print(f"\n[{i+1}/{len(todo)}] starting ep_idx={idx}", flush=True)
        ok = run_episode_with_retry(idx, components=components)
        if not ok:
            failed.append(idx)
    print(f"\n[done] failed={failed}", flush=True)


if __name__ == "__main__":
    main()
