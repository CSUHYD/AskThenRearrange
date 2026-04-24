# CLAUDE.md — AskThenRearrange / PrefQuest

本文件是给 Claude 的项目操作手册。每次对话开始时自动生效。

---

## 项目身份

**PrefQuest** 是一个面向家居整理的偏好学习框架，核心问题是：
> 智能体在有限提问预算内，如何通过提问策略的选择最大化对未见物品的偏好泛化能力？

目标期刊：**IJHCS**（International Journal of Human-Computer Studies，Elsevier）  
当前论文文件：`paper_draft_v1/main.tex`（ACM 模板，待迁移至 Elsevier elsarticle）

---

## 写作任务规范（必须执行）

**每次润色、扩写、新写 main.tex 任何部分之前**，必须按顺序读取：

1. `docs/writing_style_guide.md` — IJHCS 格式、统计、术语规范
2. `docs/writing_logic_guide.md` — 论证结构与叙事逻辑规范

不读这两个文件直接写作会产生格式错误和论证漏洞。

---

## 术语红线（不查文件也必须记住）

### 编码层级：模式 vs 策略

两个层级必须严格区分，不得混用：

| 层级 | 内容 | 正确英文术语 | 正确中文 |
|---|---|---|---|
| 意图级（二级）| AO / PE / PI | **questioning modes** | 问题模式 |
| 策略级（三级）| TO / UL / LL / HYB | **questioning strategies** | 提问策略 |

### 问题模式（questioning modes）

| 模式 | 全称 | 认识论角色 | 禁止写法 |
|---|---|---|---|
| **AO** | Action-Oriented | Executor（执行者）| — |
| **PE** | Preference-Eliciting | Receiver（接收者）| ~~PE strategy~~（PE 是模式不是策略）|
| **PI** | Preference-Induction | Active Constructor（主动建构者）| ~~PS~~（旧术语，已废弃）|

### 提问策略（questioning strategies）

| 策略 | 全称 | 模式组合 | 认识论角色 | 旧名（禁止）|
|---|---|---|---|---|
| **TO** | Task-Only | AO only | Executor | ~~DQ~~ |
| **UL** | User-Led | PE → AO | Receiver | ~~UPF~~ |
| **LL** | Learner-Led | AO ↔ PI | Active Constructor | ~~PAR~~ |
| **HYB** | Hybrid-All | 自适应组合 | — | ~~HA~~ |

### 其他术语

| 概念 | 正确写法 | 禁止写法 |
|---|---|---|
| 主指标 | **unseen PSR**（Preference Satisfaction Rate）| ~~unseen accuracy~~ |
| 预算 | **$B$**（数学模式）| ~~budget B~~（非数学模式）|
| p 值格式 | **p = .001**（无前导零）| ~~p = 0.001~~ |

---

## 关键实验结论（不得引用错误数字）

以下数字来自 GPT-5-Chat 全量实验（n = 102 episodes），是论文 Abstract 和 Results 的权威数字：

- UL unseen PSR @ B=5：**85.2%** ± 1.6 SE
- TO unseen PSR @ B=5：**72.7%** ± 2.1 SE
- 差值：**+12.5 pp**，Wilcoxon W = 94，p < .001
- HYB vs UL @ B=5：p = .085（不显著）
- HYB vs UL @ B=10：p = .796（不显著）

Qwen3-8B 的数字（UL 69.8% / TO 58.7%）仅用于 Appendix C，不得出现在主文。

---

## §3.3 编码框架核心决策（已定稿）

以下决策已通过充分讨论确认，不得在写作中回退：

**框架结构（Route B）**
- 三级层次编码：先验分析维度（§3.3.1）→ 意图级编码（§3.3.2）→ 策略识别（§3.3.3）
- 两个分析维度从迭代编码中归纳涌现，理论框架（Levinson 1983；Fürnkranz & Hüllermeier 2010）作为事后验证，而非推导来源
- K-type（Shin et al., 2023）作为编码辅助工具提一句，不构成框架的推导来源
- Wilson（1999）已完全删除，不得引回

**IRR 数据**（四编码者，N = 139 问题）
- 意图级：Cohen's κ₁ = .870（HCI 编码者 A×B，差异最大配对），Krippendorff's α₁ = .927（四编码者联合）
- 策略级：Cohen's κ₂ = 1.000（完美一致）
- 7 处分歧分布于三条维度边界（AO↔PE 3处，AO↔PI 3处，PE↔PI 1处），作为维度数据来源的独立佐证
- HHI 策略分布：TO = 4（28.6%），UL = 7（50.0%），LL = 3（21.4%），HYB-HHI = 0（未观察到）

**中文草稿**：`docs/section_3_3_draft_zh.md`（v3，当前权威版本）

---

## 关键文件地图

```
AskThenRearrange/
├── CLAUDE.md                          ← 本文件
├── README.md                          ← 项目说明（人类读者）
├── paper_draft_v1/
│   └── main.tex                       ← 论文主文件（唯一权威版本）
├── docs/
│   ├── writing_style_guide.md         ← IJHCS 格式/统计/术语规范
│   ├── writing_logic_guide.md         ← 论证结构与叙事逻辑规范
│   ├── system_overview.md             ← PrefQuest 技术架构说明
│   ├── study2_frontend_PRD.md         ← Study 2 前端系统需求文档（给开发者）
│   ├── study2_session_sop.md          ← Study 2 实验员操作 SOP（给实验员，含问卷题目）
│   └── section_3_3_draft_zh.md        ← §3.3 中文草稿 v3（当前权威，待翻译入 main.tex）
├── logs/
│   └── ablation_full_qwen3.jsonl      ← Qwen3 全量实验日志
└── plots/
    └── ablation_full_qwen3.png        ← 消融实验图
```

---

## 代码任务规范

**代码任务前**先读 `docs/system_overview.md` 了解模块结构。

**运行环境**：conda `behavior`

```bash
conda activate behavior

# LLM 后端配置（二选一）
export LLM_BACKEND=openai
export LLM_MODEL=gpt-5-chat
export LLM_API_KEY=YOUR_KEY
export LLM_BASE_URL=https://your-endpoint/v1

# 或 Ollama
export LLM_BACKEND=ollama
export LLM_MODEL=qwen3
export LLM_BASE_URL=http://127.0.0.1:11434
```

**主要入口**：
- 策略实验：`python test_policy_loop.py`
- Raw LLM baseline：`python test_raw_llm.py`
- Study 2 前端：`study2_app/backend/main.py`
