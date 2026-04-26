# AGENTS.md - AskThenRearrange / PrefQuest

This file migrates the project memory from `CLAUDE.md` and Claude project memory into Codex project instructions.

## Project Identity

**PrefQuest** is a preference-learning framework for household rearrangement. The core research question is:

> How can an agent choose questioning strategies under a limited question budget to maximize preference generalization to unseen items?

Target journal: **IJHCS** (International Journal of Human-Computer Studies, Elsevier).

Current paper file: `paper_draft_v1/main.tex` (currently ACM template; to be migrated to Elsevier `elsarticle`).

The user is working on two related directions:
- B-direction, primary: IJHCS evaluation paper on questioning strategies and user experience.
- A-direction, possible spinoff: CoRL technical paper on robot learning / active preference learning.

## Collaboration Preferences

- The user communicates in Chinese. Technical content may be in English or Chinese.
- Keep responses concise. Do not explain every implementation detail unless the user asks.
- The user delegates implementation decisions but stays involved in research direction and paper framing.
- Respect prioritization cues such as "先做 X" and "先放一放".
- If the user says "中间的需要我确认的步骤一律确认", skip intermediate confirmation steps.
- The user is comfortable with Python, LLMs, Pydantic, evaluation pipelines, LaTeX, HCI methodology, within-subject studies, and mediation analysis.

## Mandatory Writing Protocol

Before polishing, expanding, or writing any section of `paper_draft_v1/main.tex`, read these files in order:

1. `docs/writing_style_guide.md` - IJHCS format, statistics, terminology.
2. `docs/writing_logic_guide.md` - argument structure and narrative logic.

Do not edit paper text before reading both guides.

## Terminology Rules

Keep coding levels strictly separate:

| Level | Content | Correct English | Correct Chinese |
|---|---|---|---|
| Intent level, secondary | AO / PE / PI | **questioning modes** | 问题模式 |
| Strategy level, tertiary | TO / UL / LL / HYB | **questioning strategies** | 提问策略 |

Questioning modes:

| Mode | Full name | Epistemic role | Forbidden wording |
|---|---|---|---|
| **AO** | Action-Oriented | Executor | - |
| **PE** | Preference-Eliciting | Receiver | Do not write "PE strategy" |
| **PI** | Preference-Induction | Active Constructor | Do not write "PS" |

Questioning strategies:

| Strategy | Full name | Mode composition | Epistemic role | Forbidden old name |
|---|---|---|---|---|
| **TO** | Task-Only | AO only | Executor | DQ |
| **UL** | User-Led | PE -> AO | Receiver | UPF |
| **LL** | Learner-Led | AO <-> PI | Active Constructor | PAR |
| **HYB** | Hybrid-All | Adaptive mix | - | HA |

Other terminology:

| Concept | Correct wording | Forbidden wording |
|---|---|---|
| Primary metric | **unseen PSR** (Preference Satisfaction Rate) | unseen accuracy |
| Budget | **$B$** in math mode | budget B in prose |
| p-value format | **p = .001** | p = 0.001 |

## Authoritative Experimental Results

These are the authoritative GPT-5-Chat full-experiment numbers for the Abstract and Results (n = 102 episodes):

- UL unseen PSR @ B=5: **85.2%** +/- 1.6 SE.
- TO unseen PSR @ B=5: **72.7%** +/- 2.1 SE.
- Difference: **+12.5 pp**, Wilcoxon W = 94, p < .001.
- HYB vs UL @ B=5: p = .085, not significant.
- HYB vs UL @ B=10: p = .796, not significant.

Qwen3-8B numbers (UL 69.8% / TO 58.7%) are Appendix C only. Do not use them in the main text.

## Section 3.3 Coding Framework Decisions

The following decisions are final and must not be reverted in writing:

- Use Route B: three-level hierarchical coding: a priori analytical dimensions (§3.3.1) -> intent-level coding (§3.3.2) -> strategy identification (§3.3.3).
- The two analytical dimensions emerged from iterative coding. Theoretical frameworks (Levinson 1983; Furnkranz & Hullermeier 2010) are used for post hoc validation, not as deductive sources.
- K-type (Shin et al., 2023) may be mentioned as a coding aid, but not as the source of the framework.
- Wilson (1999) has been fully removed. Do not reintroduce it.

IRR data, four coders, N = 139 questions:

- Intent level: Cohen's kappa_1 = .870 (HCI coders A x B, maximum-disagreement pair); Krippendorff's alpha_1 = .927 (all four coders).
- Strategy level: Cohen's kappa_2 = 1.000 (perfect agreement).
- Seven disagreements fall across three dimension boundaries: AO<->PE 3, AO<->PI 3, PE<->PI 1. Treat this as independent support for the dimensions.
- HHI strategy distribution: TO = 4 (28.6%), UL = 7 (50.0%), LL = 3 (21.4%), HYB-HHI = 0 (not observed).

Authoritative Chinese draft: `docs/section_3_3_draft_zh.md` (v3).

## Study 2 WoZ Validity Framing

When writing Study 2 design, apparatus, limitations, or reviewer responses about the WoZ robot-assisted manipulation setup, frame the defense as an **internal vs. external validity tradeoff**.

Core argument:

- **Internal validity is maximized**: WoZ removes manipulation noise such as grasping failures, motion-planning errors, and perception drift, so variance in unseen PSR and subjective measures is attributable to the questioning strategy, which is what RQ2/RQ4/H1-H3 test.
- **External validity is bounded but not broken**: the construct of interest is the dialogue policy, not the gripper. Questioning behaviors transfer to embodied platforms as long as the question-answer channel is preserved.
- **Future work**: a full embodied replication with a real robot belongs in §7.

Application guidance:

- §6.1 opening: add one sentence framing Study 2 as prioritizing internal validity over ecological realism by holding manipulation constant.
- §6.5 Apparatus / WoZ rationale: include a short paragraph naming the internal/external validity tradeoff and the confounds removed by WoZ.
- §7 Discussion / limitations: acknowledge the external-validity cost and point to embodied replication as future work.
- Do not bury this in a footnote. Reviewers search for "validity" explicitly in methods sections.

## Key Files

```text
AskThenRearrange/
├── AGENTS.md                          <- Codex project instructions
├── CLAUDE.md                          <- Original Claude project instructions
├── README.md                          <- Project overview
├── paper_draft_v1/
│   └── main.tex                       <- Paper main file, authoritative
├── docs/
│   ├── writing_style_guide.md         <- IJHCS format/statistics/terminology
│   ├── writing_logic_guide.md         <- Argument structure and narrative logic
│   ├── system_overview.md             <- PrefQuest technical architecture
│   ├── study2_frontend_PRD.md         <- Study 2 frontend PRD
│   ├── study2_session_sop.md          <- Study 2 experimenter SOP and questionnaire
│   └── section_3_3_draft_zh.md        <- §3.3 Chinese draft v3
├── logs/
│   └── ablation_full_qwen3.jsonl
└── plots/
    └── ablation_full_qwen3.png
```

## Code Task Protocol

Before code tasks, read `docs/system_overview.md` to understand module structure.

Runtime environment: conda `behavior`.

```bash
conda activate behavior

# LLM backend option 1
export LLM_BACKEND=openai
export LLM_MODEL=gpt-5-chat
export LLM_API_KEY=YOUR_KEY
export LLM_BASE_URL=https://your-endpoint/v1

# LLM backend option 2
export LLM_BACKEND=ollama
export LLM_MODEL=qwen3
export LLM_BASE_URL=http://127.0.0.1:11434
```

Main entry points:

- Strategy experiment: `python test_policy_loop.py`
- Raw LLM baseline: `python test_raw_llm.py`
- Study 2 frontend backend: `study2_app/backend/main.py`
