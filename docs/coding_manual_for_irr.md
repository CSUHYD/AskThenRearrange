# Coding Manual — Independent Rater Version
## E1 HHI Hierarchical Coding Framework

**Version**: 1.0  
**Task**: Code each learner question in `e1_questions_for_coding.json` with:
1. A **Level 1 intent label** (AO / PE / PI) for each question
2. A **Level 2 pattern label** (DQ / UPF / PAR) for each dyad

Do NOT reference any pre-existing labels. Code independently from first principles using only this manual.

---

## Context

These are transcripts from Human-Human Interaction (HHI) studies in which a **robot learner** (Learner) organises a refrigerator by asking questions to the **homeowner** (User). Your task is to classify each of the Learner's questions.

The learner is trying to figure out where to put items. The key question for coding is: **what epistemic role does this question play?**

---

## Level 1 — Intent Coding

Assign one of three labels to each question:

---

### AO — Action-Oriented

**Definition:** An AO question targets a single, concrete placement or handling decision for a specific item or zone. Its answer resolves one action step; it does not invite the user to articulate any general organising principle.

**Core criterion:**
- The answer's applicability is **limited to the specific item(s) or zone mentioned**
- No generalizable organising rule is proposed or elicited

**Epistemic role:** No preference model is being built — the Learner is requesting permission or confirmation for one action.

**Typical examples:**
- "牛奶放不下了，放这里是不是好一些" → AO (single placement proposal)
- "水果的话放在上面还是下面呢" → AO (single item placement)
- "这是什么？" → AO (identity check serving next action)
- "这放饮料可以吗" → AO (slot confirmation)
- "放不下怎么办" → AO (operational problem)

**Multi-item AO:** If a question mentions 2–3 specific items but proposes only their concrete positions without forming a generalizable rule, it is still **AO** (bundled placement confirmation). Example: "把这个放下面，这个放上面，怎么样" → AO (two specific items, no generalizable rule).

---

### PE — Preference-Eliciting

**Definition:** A PE question invites the User to articulate a general organising preference or principle. Its answer is expected to apply across multiple items or future decisions. The **User** is the originator of the preference content; the Learner is a passive receiver.

**Core criteria:**
- The answer has potential coverage across **a category or general strategy** (≥ 2 items)
- The question does **not** contain any arrangement hypothesis proposed by the Learner
- The **User** generates the preference content

**Epistemic role:** The User builds the preference framework; the Learner receives it.

**Typical examples:**
- "你希望这个冰箱怎么整理排列" → PE
- "你一般喜欢所有东西按照种类放吗" → PE
- "你会把食品和饮料摆放在一起吗" → PE (asks about the user's general separation principle)
- "你希望按品类整理吗？比如这里放牛奶，这里放酸奶" → PE (the examples are illustrations, not proposals)

**Key distinction from AO:** Does the answer generalize beyond a single item? 
- "牛奶放哪里" → AO (one item)
- "你一般把饮料怎么整理" → PE (general category principle)

**Key distinction from PI:** Who generates the preference content?
- PE: "你希望如何整理冰箱？" → User generates the answer
- PI: "我打算把饮料放侧面，食品放中间，对吗？" → Learner proposes, User validates

---

### PI — Preference-Induction

**Definition:** A PI question presents a preference hypothesis that the **Learner** has inferred from scene observations or accumulated actions, and asks the User to validate or correct it. The Learner is the hypothesis generator; the User is the validator.

**Core criteria:**
- The question **explicitly or implicitly** contains a generalizable hypothesis proposed by the Learner
- The hypothesis covers ≥ 2 items or an entire zone/category
- The hypothesis is **inferred by the Learner** (not proposed by the User in a prior turn)

**Epistemic role:** The Learner actively builds the preference model; the User validates/corrects.

**Typical examples:**
- "我整理的话，会把牛奶放这里，饮料放这里，水果放这里……你觉得怎么样？" → PI (Learner proposes full layout)
- "只要开封了我就放第一层，可以吧" → PI candidate (Learner infers a rule about opened items)
- "所以所有开封的都放这层，对吗" → PI (Learner induces a rule from observed patterns)

**Critical boundary with AO:**
- PI requires the hypothesis to be a **generalizable rule** — if confirmed, it should apply to items not yet mentioned.
- Multi-item proposals covering only specific named items (without a generalizable rule) are **AO**, not PI.

**Critical boundary with PE:**
- PE: "你一般把开封的食品放哪里？" → User generates the answer from scratch
- PI: "我打算把所有开封的食品放第一层——这样对吗？" → Learner proposes; User validates

---

## Decision Aid — Quick Reference

| Question pattern | Likely label |
|---|---|
| "XX放在哪里？" (single item) | AO |
| "XX放这里可以吗？" (single placement) | AO |
| "这是什么？" / "XX算YY吗？" | AO |
| "怎么办？" (operational problem) | AO |
| "你希望/喜欢/一般怎么整理冰箱/饮料/水果…？" | PE |
| "你会把A和B分开吗？" (general principle) | PE |
| "按XX方式还是YY方式整理？" (general) | PE |
| "我打算把牛奶放X，饮料放Y，水果放Z——对吗？" | PI |
| "所以所有XX都放第一层，对吗？" (inferred rule) | PI |
| Summary check of inferred rules | PI |

---

## Borderline Cases

**K11/user questions coded C1 (not C4):**  
Some questions about user habits (K11) are coded as C1/Q2 rather than C4/Q14 in the original data. Apply your semantic judgment: if the question is asking for the user's general organising preference, label it PE regardless of the C/Q raw codes.

**Summary verification after multiple AOs:**  
If the Learner has placed several items and then says "总结一下，XX放这里，YY放那里……对吗？"  — this is a **PI** if it proposes a generalizable rule. If it merely recites specific item positions already confirmed, it is **AO**.

**Single-item questions with "你希望":**  
"你希望牛奶横着摆放还是竖着" — despite using 你希望 (preference language), this concerns a single item's orientation. → **AO**.

**Questions about item identity/classification:**  
"椰奶也算奶吗？" / "这是茶叶吗？" — these seek factual/classification answers to support placement decisions. → **AO**.

---

## Level 2 — Pattern Classification

After coding all questions in a dyad, assign one of three pattern labels to the **entire dyad** based on the intent sequence:

---

### Classification Rule (apply in order of priority)

**Rule 1 — PAR:**  
If the **first preference-seeking question** (first PE or PI in the sequence) is a **PI** → classify as **PAR**

**Rule 2 — UPF:**  
If the **first preference-seeking question** is a **PE** → classify as **UPF**

**Rule 3 — DQ:**  
If there are **no PE or PI questions** at all → classify as **DQ**

---

### Pattern Definitions

**DQ (Direct Query):**  
The Learner has no preference-acquisition strategy. All questions are AO. The Learner works through items one by one without attempting to build a preference model.

*Epistemic role:* Learner = passive executor; no preference model built.

**UPF (User Preference First):**  
The Learner opens with a PE question, inviting the User to articulate organising principles before beginning execution. The User's answer provides the framework; the Learner then executes with AO questions.

*Epistemic role:* User builds the preference framework; Learner receives and executes.

**PAR (Parallel Active Reasoning):**  
The Learner opens with a PI question — proposing a hypothesis derived from scene observation or reasoning — and asks the User to validate it. The Learner is the active constructor of the preference model.

*Epistemic role:* Learner builds the preference model; User validates/corrects.

---

### Pattern Notes

- **PAR vs UPF:** If a dyad has both PE and PI questions, the pattern is determined by which type appears **first** in the sequence.
- **UPF with late PI:** A single PI question appearing after several AO questions does NOT change the pattern from UPF if the first preference question was a PE.
- **DQ is the residual category:** if no preference-seeking question appears, classify as DQ regardless of question content.

---

## Output Format

For each dyad, produce two outputs:

1. **Level 1 table** — one row per question:

| id | text (abbreviated) | intent_label |
|---|---|---|
| GH010044_Q01 | 请问你一般把牛奶放在那 | AO |
| ... | ... | ... |

2. **Level 2 classification** — one line per dyad:

```
GH010044: DQ
GH010044!!: UPF
...
```

---

## Important Notes

- Code based on question **function and semantics**, not surface form alone.
- The K/C/Q raw codes in the JSON are reference data but your intent label must reflect the question's actual semantic role in context.
- Mark any question you find genuinely ambiguous with a `?` suffix on the label (e.g., `AO?`) and briefly note why.
- Work systematically dyad by dyad, in the order given.
