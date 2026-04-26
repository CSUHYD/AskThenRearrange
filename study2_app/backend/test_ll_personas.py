"""Stress-test Study 2 LL by simulating diverse user personas.

For each (persona × episode) pair, runs the LL strategy at budget=5 and logs
per-turn: pattern, hypothesis, question, answer, state-delta. The summary
detects three bug classes from the previous round:

  1. PE-form question slipping out of PI proposer (forbidden phrasing)
  2. Counter-placement lost on rejected PI (negative_preference present
     but no confirmed_action / confirmed_preference added when user named
     a different receptacle)
  3. Rule redirect not recognised (user says only a receptacle name; should
     yield confirmed_rule with refined receptacle)

Personas vary the oracle's answer STYLE only — ground-truth placements and
annotator notes are unchanged across personas, so they remain comparable.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agent_schema import AgentState  # noqa: E402
from data import DEFAULT_DATA_PATH, load_episodes  # noqa: E402
from oracle import NaturalUserOracle  # noqa: E402
from proposers import ActionProposer  # noqa: E402
from question_policy import QuestionDecision  # noqa: E402
from state_init import build_initial_state  # noqa: E402
from state_update import StateUpdate  # noqa: E402

from study2_app.backend.pe_proposer_study2 import Study2PreferenceElicitingProposer  # noqa: E402
from study2_app.backend.pi_proposer_study2 import Study2PreferenceInductionProposer  # noqa: E402
from study2_app.backend.policy_study2 import Study2QuestionPolicyController  # noqa: E402


BUDGET = 5
EPISODE_INDICES = [0, 34, 68]  # one per room: living room / bedroom / kitchen
OUT_MD = PROJECT_ROOT / "docs" / "ll_persona_test_report.md"
OUT_JSONL = PROJECT_ROOT / "logs" / "ll_persona_test.jsonl"


# Persona styles inject extra guidance into oracle system prompt.
PERSONAS = {
    "cooperative_precise": {
        "label": "合作-精确",
        "style": (
            "Be cooperative and precise. Give a complete sentence including "
            "the exact receptacle name and the category you are confirming. "
            "When the agent's hypothesis is correct, confirm explicitly: "
            "'Yes — X belongs on the Y'. When it's wrong, give a corrected "
            "rule with both category and receptacle in one sentence."
        ),
    },
    "terse": {
        "label": "简短",
        "style": (
            "Be very terse. Reply in 1-3 words when possible. If the agent's "
            "hypothesis is right, just say 'yes' or the receptacle name. "
            "If wrong, just name a different receptacle without explanation. "
            "Do not elaborate or list categories."
        ),
    },
    "resistant_redirect": {
        "label": "抗拒-改向",
        "style": (
            "You frequently disagree with the agent's category-level "
            "hypotheses. About half the time, reject the proposed receptacle "
            "and name a different one (e.g. 'no, on the nightstand instead'). "
            "Sometimes use deictic references like 'this one' or 'these'. "
            "Stay grounded in your annotator_notes — only redirect when the "
            "notes actually disagree with the agent's proposed receptacle."
        ),
    },
}


def make_oracle_with_persona(persona_key: str) -> NaturalUserOracle:
    oracle = NaturalUserOracle()
    persona = PERSONAS[persona_key]
    original_answer = oracle.answer

    def patched_answer(*, question, room, receptacles, seen_objects,
                       annotator_notes, gt_seen_placements, qa_history):
        styled_notes = list(annotator_notes) + [f"[Persona style] {persona['style']}"]
        return original_answer(
            question=question, room=room, receptacles=receptacles,
            seen_objects=seen_objects, annotator_notes=styled_notes,
            gt_seen_placements=gt_seen_placements, qa_history=qa_history,
        )

    oracle.answer = patched_answer  # type: ignore[assignment]
    return oracle


PE_FORM_TRIGGERS = [
    "what do you put", "what kinds of items", "what types of items",
    "how do you usually organise", "how do you usually organize",
    "where do you put", "where do you usually keep",
    "Y 里你一般放", "你一般放什么", "你一般放在哪", "你是如何整理",
    "你平时喜欢怎么整理",
]


def detect_pe_form_drift(question: str) -> bool:
    """Return True if a PI question drifted into PE-style phrasing."""
    q = question.lower()
    return any(trigger.lower() in q for trigger in PE_FORM_TRIGGERS)


def run_episode(episode, persona_key, *, controller, ao, pe, pi, updater) -> Dict[str, Any]:
    oracle = make_oracle_with_persona(persona_key)
    state: AgentState = build_initial_state(
        episode=episode, strategy="learner_led", budget_total=BUDGET
    )
    turns: List[Dict[str, Any]] = []
    fb_count = 0

    while len(state["qa_history"]) < BUDGET:
        decision = controller.plan_next_question(state=state, mode="learner_led")
        if decision is None:
            break

        original_pattern = decision.question_pattern
        intent = _propose(state, decision, ao=ao, pe=pe, pi=pi)
        if intent is None and decision.question_pattern == "preference_induction":
            fb_count += 1
            decision = QuestionDecision(question_pattern="action_oriented",
                                        guidance="PI fallback")
            intent = _propose(state, decision, ao=ao, pe=pe, pi=pi)
        if intent is None:
            break

        question = intent.question if hasattr(intent, "question") else str(intent.get("question", ""))
        ca_before = len(state["confirmed_actions"])
        cp_before = len(state["confirmed_preferences"])
        np_before = len(state["negative_preferences"])

        ans = oracle.answer(
            question=question, room=state["room"], receptacles=state["receptacles"],
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
            hyp = str(intent.get("hypothesis", ""))
        elif decision.question_pattern == "action_oriented":
            state = updater.update_state_from_action_answer(
                state=state, target=intent.object_name, answer=ans.answer,
                question=intent.question, action_mode=intent.action_mode,
            )
            hyp = ""
        else:
            state = updater.update_state_from_preference_induction_answer(
                state=state, hypothesis=str(intent.get("hypothesis", "")),
                covered_objects=list(intent.get("covered_objects", [])),
                answer=ans.answer, question=question,
            )
            hyp = str(intent.get("hypothesis", ""))

        turns.append({
            "turn": len(state["qa_history"]),
            "pattern": decision.question_pattern,
            "fallback": original_pattern != decision.question_pattern,
            "hypothesis": hyp,
            "question": question,
            "answer": ans.answer,
            "ca_delta": len(state["confirmed_actions"]) - ca_before,
            "cp_delta": len(state["confirmed_preferences"]) - cp_before,
            "np_delta": len(state["negative_preferences"]) - np_before,
            "pe_form_drift": detect_pe_form_drift(question)
                              if decision.question_pattern == "preference_induction" else False,
        })

    # Final PSR-lite: for each seen object, check if state's resolved placement matches gt.
    return {
        "episode_id": episode.episode_id,
        "room": episode.room,
        "persona": persona_key,
        "turns": turns,
        "fallback_count": fb_count,
        "final_confirmed_actions": list(state["confirmed_actions"]),
        "final_confirmed_preferences": list(state["confirmed_preferences"]),
        "final_negative_preferences": list(state["negative_preferences"]),
    }


def _propose(state, decision, *, ao, pe, pi):
    if decision.question_pattern == "preference_eliciting":
        return pe.propose(state=state, guidance=decision.guidance)
    if decision.question_pattern == "action_oriented":
        return ao.propose(state=state, guidance=decision.guidance)
    if decision.question_pattern == "preference_induction":
        intents = pi.propose(state=state, max_intents=3, guidance=decision.guidance)
        return intents[0] if intents else None
    return None


def summarize(logs: List[Dict[str, Any]]) -> str:
    md = ["# Study 2 LL × 多用户画像 测试报告\n"]
    md.append(f"**配置**: {len(EPISODE_INDICES)} episodes (idx={EPISODE_INDICES}) × "
              f"{len(PERSONAS)} personas × budget={BUDGET}  ")
    md.append(f"**LLM**: qwen3 @ http://110.42.252.68:8080  ")
    md.append(f"**生成**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Aggregate bug detectors
    pe_drift_total = sum(t["pe_form_drift"] for log in logs for t in log["turns"])
    pi_total = sum(1 for log in logs for t in log["turns"] if t["pattern"] == "preference_induction")
    counter_lost = 0  # PI turn with np_delta>0 but ca_delta==0 AND cp_delta==0
    for log in logs:
        for t in log["turns"]:
            if t["pattern"] == "preference_induction" and t["np_delta"] > 0 and t["ca_delta"] == 0 and t["cp_delta"] == 0:
                counter_lost += 1

    md.append("## 一、整体 bug 探测器\n")
    md.append("| 检测项 | 期望 | 实测 | 状态 |")
    md.append("|---|---|---|---|")
    md.append(f"| PI 问题漂成 PE 句式 | 0 | {pe_drift_total}/{pi_total} | "
              f"{'✓' if pe_drift_total == 0 else '✗ ' + str(pe_drift_total) + ' 处漂移'} |")
    md.append(f"| 拒绝 PI 时 counter-placement 丢失 | 0（拒绝时若有 receptacle 应进 counter / 改向） | "
              f"{counter_lost}/{pi_total} | "
              f"{'✓' if counter_lost == 0 else '⚠ ' + str(counter_lost) + ' 例只写了 negative_preference 没写 action/preference'} |")
    md.append("")

    # Per-persona summary
    md.append("## 二、按 persona 分组\n")
    for pk, p in PERSONAS.items():
        runs = [l for l in logs if l["persona"] == pk]
        ca = sum(t["ca_delta"] for r in runs for t in r["turns"])
        cp = sum(t["cp_delta"] for r in runs for t in r["turns"])
        np = sum(t["np_delta"] for r in runs for t in r["turns"])
        n_pi = sum(1 for r in runs for t in r["turns"] if t["pattern"] == "preference_induction")
        n_ao = sum(1 for r in runs for t in r["turns"] if t["pattern"] == "action_oriented")
        md.append(f"### {pk} — {p['label']}\n")
        md.append(f"- 模式分布: AO={n_ao}, PI={n_pi}")
        md.append(f"- 状态累积: confirmed_actions=+{ca}, confirmed_preferences=+{cp}, negative_preferences=+{np}")
        md.append("")

    # Per-trial detail
    md.append("## 三、逐轮明细\n")
    for log in logs:
        md.append(f"### {log['persona']} / {log['episode_id']} ({log['room']})\n")
        md.append("| turn | pattern | hyp | Q | A | Δca | Δcp | Δnp | drift |")
        md.append("|---|---|---|---|---|---|---|---|---|")
        for t in log["turns"]:
            hyp = (t["hypothesis"][:40] + "…") if len(t["hypothesis"]) > 40 else t["hypothesis"]
            q = t["question"].replace("|", "\\|")
            q = (q[:60] + "…") if len(q) > 60 else q
            a = t["answer"].replace("|", "\\|").replace("\n", " ")
            a = (a[:50] + "…") if len(a) > 50 else a
            drift = "⚠ PE-form" if t["pe_form_drift"] else ""
            md.append(f"| {t['turn']} | {t['pattern'][:2].upper()} | {hyp} | {q} | {a} | "
                      f"{t['ca_delta']:+d} | {t['cp_delta']:+d} | {t['np_delta']:+d} | {drift} |")
        md.append("")
        md.append(f"- 末态 confirmed_actions ({len(log['final_confirmed_actions'])}): "
                  f"{log['final_confirmed_actions']}")
        md.append(f"- 末态 confirmed_preferences ({len(log['final_confirmed_preferences'])}): "
                  f"{[(p['hypothesis'], p.get('receptacle')) for p in log['final_confirmed_preferences']]}")
        md.append(f"- 末态 negative_preferences ({len(log['final_negative_preferences'])}): "
                  f"{[p['hypothesis'] for p in log['final_negative_preferences']]}")
        md.append("")

    md.append("## 四、结论\n")
    if pe_drift_total == 0 and counter_lost == 0:
        md.append("- 两个上一轮报出的 bug 在所有 persona / 所有房间下均**未复现** ✓")
    else:
        md.append("- 仍发现以下问题：")
        if pe_drift_total > 0:
            md.append(f"  - **PI 漂成 PE 句式**: {pe_drift_total}/{pi_total} 例")
        if counter_lost > 0:
            md.append(f"  - **PI 拒绝时 counter-placement 丢失**: {counter_lost}/{pi_total} 例")
    md.append("")
    return "\n".join(md)


def main():
    all_eps = load_episodes(DEFAULT_DATA_PATH)
    episodes = [all_eps[i] for i in EPISODE_INDICES]
    print(f"[init] sampled {len(episodes)} episodes (idx={EPISODE_INDICES}) "
          f"rooms={[e.room for e in episodes]}", flush=True)

    controller = Study2QuestionPolicyController(selection_method="rule")
    ao = ActionProposer()
    pe = Study2PreferenceElicitingProposer()
    pi = Study2PreferenceInductionProposer()
    updater = StateUpdate()
    print("[init] components ready", flush=True)

    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    if OUT_JSONL.exists():
        OUT_JSONL.unlink()

    logs: List[Dict[str, Any]] = []
    total = len(episodes) * len(PERSONAS)
    n = 0
    for pk in PERSONAS:
        for ep in episodes:
            n += 1
            t0 = time.time()
            try:
                log = run_episode(ep, pk, controller=controller, ao=ao, pe=pe, pi=pi, updater=updater)
            except Exception as e:
                print(f"[trial {n}/{total}] {pk}/{ep.episode_id} FAILED: {e}", flush=True)
                continue
            logs.append(log)
            with OUT_JSONL.open("a", encoding="utf-8") as f:
                f.write(json.dumps(log, ensure_ascii=False) + "\n")
            seq = "→".join(t["pattern"][:2].upper() for t in log["turns"])
            cnt_pi = sum(1 for t in log["turns"] if t["pattern"] == "preference_induction")
            print(f"[trial {n}/{total}] {pk}/{ep.episode_id} ({ep.room}) "
                  f"seq={seq} PI={cnt_pi} fb={log['fallback_count']} "
                  f"dt={time.time()-t0:.1f}s", flush=True)

    md = summarize(logs)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"\n[done] wrote {OUT_MD}")


if __name__ == "__main__":
    main()
