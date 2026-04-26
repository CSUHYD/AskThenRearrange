# Study 1 LL 重跑结果（qwen3, 15 episodes）

**配置**：Study 1 LL（旧 evidence-gated 实现，`proposers.PreferenceInductionProposer` + `QuestionPolicyController._rule_learner_led`，要求 ≥2 confirmed_actions 同 receptacle 才触发 PI）  
**LLM**：qwen3 @ http://110.42.252.68:8080  
**采样**：15 episodes（5 per room：living=[0,7,14,21,28], bedroom=[34,41,48,55,62], kitchen=[68,75,82,89,96]）  
**Budgets**：1 / 3 / 5 / 10  
**日志**：[logs/study1_ll_rerun.jsonl](../logs/study1_ll_rerun.jsonl)  
**入口**：[scripts/run_study1_ll_resilient.py](../scripts/run_study1_ll_resilient.py)

---

## 一、PSR 主表

| Budget | Seen PSR (M ± SE) | Unseen PSR (M ± SE) |
|---|---|---|
| B=1 | 47.8% ± 3.2 | 47.2% ± 3.7 |
| B=3 | 52.2% ± 3.6 | 55.0% ± 4.8 |
| B=5 | 61.1% ± 1.8 | 61.7% ± 4.5 |
| B=10 | 76.7% ± 3.0 | 73.9% ± 3.0 |

**观察**：随 budget 单调上升，B=10 时 unseen ≈ seen ≈ 75%。从 B=5→10 增益最大（unseen +12.2pp），低 budget 阶段（B=1→3）增益不明显（unseen +7.8pp）—— 与 Study 1 LL "需先攒 ≥2 actions 才触发 PI" 的特性一致：低 budget 时 PI 还来不及发力。

## 二、按房间细分（unseen PSR）

| Budget | living | bedroom | kitchen |
|---|---|---|---|
| B=1 | 48.3% | 51.7% | 41.7% |
| B=3 | 60.0% | 58.3% | 46.7% |
| B=5 | 58.3% | 68.3% | 58.3% |
| B=10 | 70.0% | 71.7% | **80.0%** |

**观察**：kitchen 在低 budget 表现最差（B=1: 41.7%）但 B=10 反超（80.0%），说明 kitchen 物品类别更分散，PI 需要多轮证据归纳；bedroom 在中 budget 最快达到平台（B=5 已达 68.3%）。

## 三、与论文 Abstract / Study 1 §5.2 数字的差异

论文当前权威数字（GPT-5-Chat, 102 episodes）：
- LL @ B=5：71.0% unseen PSR
- LL @ B=10：77.4% unseen PSR

本次 rerun（qwen3, 15 episodes）：
- LL @ B=5：61.7% unseen PSR
- LL @ B=10：73.9% unseen PSR

**差距来源**：
1. **模型差异**：qwen3-8B 的 commonsense 先验弱于 GPT-5-Chat，PI 假设质量与 oracle 注释 grounding 都偏低。这与 [paper_draft_v1/main.tex](../paper_draft_v1/main.tex) Appendix C 报告的 Qwen3-8B 数字趋势一致（Qwen3 LL @ B=5 = 57.2%；本次 61.7% 略高，处于波动范围）。
2. **样本量**：15 episodes vs 102 — SE 较大（3.0–4.8pp），点估计本身偏差较高。
3. **轨迹一致**：相对排序（B=10 > B=5 > B=3 > B=1）和单调增长趋势与论文一致，绝对量级也在 Qwen3 Appendix C 的预期窗口内。

## 四、行为日志摘录（验证 LL gate 仍生效）

每个 episode 的 turn 序列（节选 episode_0）：
```
turn 1: AO  →  turn 2: AO  →  turn 3: PI  →  turn 4: AO  →  turn 5: AO
turn 6: AO  →  turn 7: PI  →  turn 8: AO  →  turn 9: AO  →  turn 10: PI
```

模式：**前 2 轮 AO 攒证据，第 3 轮触发 PI；之后每 ~3 轮再触发一次**。这正是 Study 1 LL 的 evidence gate 行为（`CONSOLIDATE_AFTER=2` + `≥2 unsummarized confirmed_actions`，[question_policy.py:202](../question_policy.py#L202) / [question_policy.py:608-616](../question_policy.py#L608-L616)）。

## 五、结论

- LL 在 qwen3 上从 47%（B=1）单调增长到 74%（B=10），趋势与论文一致。
- 数字偏低是模型差异，不是实现问题。论文 §5 应保留 GPT-5-Chat 主结果，本表可作为 Qwen3 Appendix 的更新数据点（替换或补充 Appendix C 的旧 LL 行）。
- LL 的 evidence-gate 行为（每 3 轮一次 PI）在所有 15 个 episode 中稳定复现，确认 [question_policy.py](../question_policy.py) 的 Study 1 LL 实现未漂移。
