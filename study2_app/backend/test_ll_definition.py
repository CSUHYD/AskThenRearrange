"""Run Study2 LL on N episodes and check compliance with §3 LL definition.

§3 (HHI) defines LL as:
  - Strategy = AO + PI only (no PE)
  - PI count > PE count (PI dominates)
  - PI hypothesis source: prior knowledge, intuitive judgment, or accumulated observations

This script runs Study2QuestionPolicyController + Study2PreferenceInductionProposer
on 10 episodes (budget=5), records each turn, and writes a markdown summary.
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
from proposers import ActionProposer, PreferenceElicitingProposer  # noqa: E402
from question_policy import QuestionDecision  # noqa: E402
from state_init import build_initial_state  # noqa: E402
from state_update import StateUpdate  # noqa: E402

from study2_app.backend.pe_proposer_study2 import Study2PreferenceElicitingProposer  # noqa: E402
from study2_app.backend.pi_proposer_study2 import Study2PreferenceInductionProposer  # noqa: E402
from study2_app.backend.policy_study2 import Study2QuestionPolicyController  # noqa: E402


N_EPISODES = 5
BUDGET = 5
OUT_MD = PROJECT_ROOT / "docs" / "ll_definition_compliance_report.md"
OUT_JSONL = PROJECT_ROOT / "logs" / "ll_definition_test.jsonl"


def run_ll_episode(episode, *, controller, ao, pe, pi, updater, oracle) -> Dict[str, Any]:
    state: AgentState = build_initial_state(
        episode=episode, strategy="learner_led", budget_total=BUDGET
    )
    turns: List[Dict[str, Any]] = []
    fallback_count = 0

    while len(state["qa_history"]) < BUDGET:
        decision = controller.plan_next_question(state=state, mode="learner_led")
        if decision is None:
            break

        original_pattern = decision.question_pattern
        intent = _propose(state, decision, ao=ao, pe=pe, pi=pi)

        if intent is None and decision.question_pattern == "preference_induction":
            fallback_count += 1
            decision = QuestionDecision(
                question_pattern="action_oriented",
                guidance="PI proposer returned None; fall back to AO.",
            )
            intent = _propose(state, decision, ao=ao, pe=pe, pi=pi)
        if intent is None:
            break

        question = intent.question if hasattr(intent, "question") else str(intent.get("question", ""))
        ans = oracle.answer(
            question=question,
            room=state["room"],
            receptacles=state["receptacles"],
            seen_objects=state["seen_objects"],
            annotator_notes=episode.annotator_notes,
            gt_seen_placements=episode.seen_placements,
            qa_history=state["qa_history"],
        )

        if decision.question_pattern == "preference_eliciting":
            state = updater.update_state_from_preference_eliciting_answer(
                state=state,
                hypothesis=str(intent.get("hypothesis", "")),
                covered_objects=list(intent.get("covered_objects", [])),
                answer=ans.answer,
                question=question,
                oracle_receptacle=ans.referenced_receptacle,
            )
            hyp = str(intent.get("hypothesis", ""))
        elif decision.question_pattern == "action_oriented":
            state = updater.update_state_from_action_answer(
                state=state,
                target=intent.object_name,
                answer=ans.answer,
                question=intent.question,
                action_mode=intent.action_mode,
            )
            hyp = ""
        elif decision.question_pattern == "preference_induction":
            state = updater.update_state_from_preference_induction_answer(
                state=state,
                hypothesis=str(intent.get("hypothesis", "")),
                covered_objects=list(intent.get("covered_objects", [])),
                answer=ans.answer,
                question=question,
            )
            hyp = str(intent.get("hypothesis", ""))
        else:
            break

        turn_idx = len(state["qa_history"])
        turns.append({
            "turn": turn_idx,
            "original_pattern": original_pattern,
            "executed_pattern": decision.question_pattern,
            "fallback": original_pattern != decision.question_pattern,
            "hypothesis": hyp,
            "question": question,
            "answer": ans.answer,
            "ca_count_after": len(state["confirmed_actions"]),
            "cp_count_after": len(state["confirmed_preferences"]),
        })

    return {
        "episode_id": episode.episode_id,
        "room": episode.room,
        "n_seen": len(episode.seen_objects),
        "n_recs": len(episode.receptacles),
        "turns": turns,
        "fallback_count": fallback_count,
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


def summarize(episodes_log: List[Dict[str, Any]]) -> str:
    n_ep = len(episodes_log)
    pe_total = pi_total = ao_total = fb_total = 0
    pi_with_zero_actions = 0
    pi_first_turn = 0
    examples: List[Dict[str, Any]] = []
    per_ep_rows: List[str] = []

    for ep in episodes_log:
        pe_n = sum(1 for t in ep["turns"] if t["executed_pattern"] == "preference_eliciting")
        pi_n = sum(1 for t in ep["turns"] if t["executed_pattern"] == "preference_induction")
        ao_n = sum(1 for t in ep["turns"] if t["executed_pattern"] == "action_oriented")
        pe_total += pe_n
        pi_total += pi_n
        ao_total += ao_n
        fb_total += ep["fallback_count"]

        for t in ep["turns"]:
            if t["original_pattern"] == "preference_induction":
                if t["ca_count_after"] - (1 if t["executed_pattern"] == "action_oriented" else 0) <= 0:
                    pi_with_zero_actions += 1
                if t["turn"] == 1:
                    pi_first_turn += 1

        seq = "→".join(t["executed_pattern"][:2].upper() for t in ep["turns"])
        rule_compliant = (pe_n == 0) and (pi_n > 0)
        per_ep_rows.append(
            f"| {ep['episode_id']} | {ep['room']} | {seq} | AO={ao_n} PE={pe_n} PI={pi_n} | "
            f"{'✓' if rule_compliant else '✗'} | {ep['fallback_count']} |"
        )

        for t in ep["turns"][:3]:
            if t["executed_pattern"] == "preference_induction":
                examples.append({
                    "ep": ep["episode_id"],
                    "turn": t["turn"],
                    "hyp": t["hypothesis"],
                    "q": t["question"],
                })

    total_turns = pe_total + pi_total + ao_total
    pct = lambda n: f"{100.0 * n / max(total_turns, 1):.1f}%"

    md = []
    md.append("# Study 2 LL 策略与 §3 定义合规性测试报告\n")
    md.append(f"**测试规模**: {n_ep} episodes × budget={BUDGET}（共 {total_turns} 轮问答）  ")
    md.append(f"**LLM**: qwen3 @ http://110.42.252.68:8080  ")
    md.append(f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    md.append("## §3 LL 定义复核（核对项）\n")
    md.append("| 定义维度 | §3 要求 | 实测 | 通过 |")
    md.append("|---|---|---|---|")
    md.append(f"| 策略组成 | 仅 AO + PI（无 PE） | PE={pe_total} ({pct(pe_total)}) | "
              f"{'✓' if pe_total == 0 else '✗'} |")
    md.append(f"| PI > PE（计数主导） | PI 数 > PE 数 | PI={pi_total}, PE={pe_total} | "
              f"{'✓' if pi_total > pe_total else '✗'} |")
    md.append(f"| PI 假设来源 | 允许 prior knowledge / common sense | "
              f"{pi_with_zero_actions}/{pi_total} 轮在零 confirmed_actions 状态下提出 PI（即纯 common sense）| "
              f"{'✓' if pi_with_zero_actions > 0 else 'N/A（未观察到，可能样本太小）'} |")
    md.append(f"| 实现细节：turn 1 即 PI | Study2 设计要求 turn 1 起触发 PI | "
              f"{pi_first_turn}/{n_ep} episodes 在 turn 1 出 PI | "
              f"{'✓' if pi_first_turn >= n_ep // 2 else '⚠'} |")
    md.append(f"| AO/PI fallback 率 | PI 提不出假设时回退 AO | {fb_total}/{total_turns} 次回退 | "
              f"{'✓' if fb_total < total_turns / 2 else '⚠ 频繁回退'} |\n")

    md.append("## 各 episode 序列\n")
    md.append("| episode | room | 模式序列 | 计数 | PI>PE & PE=0 | fallback |")
    md.append("|---|---|---|---|---|---|")
    md.extend(per_ep_rows)
    md.append("")

    md.append("## PI 问题样例（前 10 条）\n")
    for ex in examples[:10]:
        md.append(f"- **{ex['ep']} turn {ex['turn']}** ")
        md.append(f"  - 假设: *{ex['hyp']}*")
        md.append(f"  - 问题: \"{ex['q']}\"")
    md.append("")

    md.append("## 结论\n")
    rule1 = pe_total == 0
    rule2 = pi_total > pe_total
    rule3 = pi_with_zero_actions > 0
    if rule1 and rule2:
        md.append("- §3 LL 强约束（PE=0、PI>PE）**全部通过** ✓")
    else:
        md.append("- §3 LL 强约束**未完全通过**：")
        if not rule1:
            md.append(f"  - PE 仍出现 {pe_total} 次 — 与 LL 仅含 AO+PI 的定义冲突")
        if not rule2:
            md.append(f"  - PI ({pi_total}) 未严格大于 PE ({pe_total}) — 不满足 LL 分类规则")
    if rule3:
        md.append(f"- PI 假设来源已超越 §3.3.1 的传统"
                  f"\"accumulated observations\"，{pi_with_zero_actions} 轮在零 actions 时即提出假设，"
                  f"与 Study 2 设计的 common-sense 路径一致 ✓")
    md.append("")
    return "\n".join(md)


def main():
    all_eps = load_episodes(DEFAULT_DATA_PATH)
    # Sample across rooms (dataset is grouped: 34 living room, 34 bedroom, 34 kitchen).
    sample_indices = [0, 17, 34, 51, 68][:N_EPISODES]
    episodes = [all_eps[i] for i in sample_indices]
    print(f"[init] sampled {len(episodes)} episodes (indices={sample_indices}) "
          f"rooms={[e.room for e in episodes]}", flush=True)

    controller = Study2QuestionPolicyController(selection_method="rule")
    ao = ActionProposer()
    pe = Study2PreferenceElicitingProposer()
    pi = Study2PreferenceInductionProposer()
    updater = StateUpdate()
    oracle = NaturalUserOracle()
    print("[init] components ready", flush=True)

    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    if OUT_JSONL.exists():
        OUT_JSONL.unlink()

    logs: List[Dict[str, Any]] = []
    for i, ep in enumerate(episodes):
        t0 = time.time()
        try:
            log = run_ll_episode(ep, controller=controller, ao=ao, pe=pe, pi=pi,
                                 updater=updater, oracle=oracle)
        except Exception as e:
            print(f"[ep {i+1}/{N_EPISODES}] {ep.episode_id} FAILED: {e}", flush=True)
            continue
        logs.append(log)
        with OUT_JSONL.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")
        seq = "→".join(t["executed_pattern"][:2].upper() for t in log["turns"])
        print(f"[ep {i+1}/{N_EPISODES}] {ep.episode_id} ({ep.room}) "
              f"seq={seq} fb={log['fallback_count']} dt={time.time()-t0:.1f}s", flush=True)

    md = summarize(logs)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"\n[done] wrote {OUT_MD}")


if __name__ == "__main__":
    main()
