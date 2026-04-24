# Inter-Rater Reliability Results — E1 HHI Coding

**Date**: 2026-04-22  
**Coders**: A (HCI researcher) × B (dialogue linguistics expert) — independent, no prior communication  
**Data**: 14 E1 dyads, 129 questions total  

---

## Summary

| Level | Unit | Metric | Value | Interpretation |
|---|---|---|---|---|
| Level 1 | Question intent (AO/PE/PI) | Cohen's κ₁ | **0.871** | Almost perfect |
| Level 1 | Question intent (AO/PE/PI) | Krippendorff's α₁ | **0.870** | Almost perfect |
| Level 2 | Dyad pattern (DQ/UPF/PAR) | Cohen's κ₂ | **1.000** | Perfect |

---

## Level 1 — Question Intent Coding

**N = 129 questions, 7 disagreements (5.4%)**

### Confusion matrix (A rows, B columns)

|       | AO | PE | PI |
|------|-----|-----|-----|
| **AO** | 92 | 3 | 3 |
| **PE** | 0 | 21 | 1 |
| **PI** | 0 | 0 | 9 |

- Observed agreement P_o = 0.9457
- Expected agreement P_e = 0.5806
- Cohen's κ₁ = **0.871**
- Krippendorff's α₁ = **0.870**

### Disagreements by type

**AO↔PE (3 cases):**
- `GH010044!!_Q06`: "那已经开封的食品放在哪里呢" — Coder A: AO (category query, specific zone decision); Coder B: PE? (answer generalises to all opened items as a category principle)
- `GH010048_Q05`: "那些已经开封的食品放在哪里" — Same pattern as above
- `GH010052_Q17`: "水果应该放在哪里" — Coder A: AO (category placement, one zone decision); Coder B: PE? (whole-category referent)

**Resolution**: All three questions ask **where a named category goes**, without any Learner hypothesis. The answer is indeed generalizable across items in that category, but no organising *principle* is elicited — the question is operational (where do I put this group?). **→ Code AO.** The distinguishing criterion: PE requires that the User's answer constitute a generalizable *organising strategy*, not just a zone assignment for a named category.

**AO↔PI (3 cases):**
- `GH010044!!_Q08`: "冰箱两侧放酒跟饮料，下面的话我尽量给你码得整齐一点" — Coder A: AO?; Coder B: PI? (declarative plan with layout rule)
- `GH010048_Q08`: "这两边放酒和饮料，下面我也尽量给你摆放的整齐一些" — same pattern
- `GH010067_Q02`: "这一层比较隔离，适合放水果对么？" — Coder A: AO; Coder B: AO (but with reasoning)

**Resolution**: 
- Q08 pairs in GH010044!! and GH010048 are **declarative statements** (not interrogatives), with no explicit validation request. These rows appear in the coding table but lack interrogative force. **→ Code AO** (operational plan announcement, not preference validation).
- GH010067_Q02: Despite Learner reasoning ("this layer is isolated"), it resolves **one specific category's placement**. No generalizable multi-category rule proposed. **→ Code AO.**

**PE↔PI (1 case):**
- `GH010058_Q04`: "基本规则是上面摆放的浅下面深吗？还是你更希望按照个人习惯" — Coder A: PE; Coder B: PI? (Learner's depth rule hypothesis foregrounded)

**Resolution**: This question explicitly foregrounds a Learner-generated hypothesis (shallow items on top, deep below) and asks for validation or override. The Learner is proposing a generalizable organisational rule. **→ Code PI.** (Note: does not change the dyad pattern for GH010058, since earlier PE questions already establish UPF.)

---

## Level 2 — Dyad Pattern Classification

**N = 14 dyads, 0 disagreements (100% agreement)**

| Dyad | A | B | Match |
|---|---|---|---|
| GH010044 | DQ | DQ | ✓ |
| GH010044!! | UPF | UPF | ✓ |
| GH010046 | DQ | DQ | ✓ |
| GH010048 | UPF | UPF | ✓ |
| GH010050 | UPF | UPF | ✓ |
| GH010052 | UPF | UPF | ✓ |
| GH010054 | UPF | UPF | ✓ |
| GH010056 | UPF | UPF | ✓ |
| GH010058 | UPF | UPF | ✓ |
| GH010060 | DQ | DQ | ✓ |
| GH010062 | UPF | UPF | ✓ |
| GH010064 | UPF | UPF | ✓ |
| GH010067 | PAR | PAR | ✓ |
| GH010069 | UPF | UPF | ✓ |

**Distribution: DQ = 3 (21%), UPF = 10 (71%), PAR = 1 (7%)**

---

## For §3 of main.tex

### Reporting text (template)

> Two coders independently applied the coding scheme to all 14 E1 dyads (129 Learner questions total). At Level 1 (question intent), inter-rater agreement was *substantial to almost perfect* (Cohen's κ₁ = .871, Krippendorff's α₁ = .870; 7 disagreements across 129 items, 5.4%). Disagreements were concentrated in three edge-case types: (a) category-level AO queries that Coder B initially flagged as PE (3 cases), (b) declarative plan utterances with ambiguous interrogative force flagged by Coder B as PI (3 cases), and (c) one question in which a Learner-generated depth-placement hypothesis was foregrounded (1 case). All disagreements were resolved through structured discussion. At Level 2 (dialogue pattern), raters achieved perfect agreement across all 14 dyads (Cohen's κ₂ = 1.000), confirming that the pattern classification rules are unambiguous once Level 1 labels are resolved.

---

## Boundary Rules Confirmed by IRR

Based on the seven disagreement cases, the following rules are now explicitly confirmed:

1. **Category-level "where does X go?" → AO.** Even if the answer generalises to all items in the category, a question that asks about zone assignment for a *named category* without proposing any organising principle is AO, not PE.

2. **Declarative plan utterances → AO.** Rows in the table that lack interrogative force (no "吗", "吧", "呢", "怎么样") and merely announce the Learner's planned action should be coded AO, not PI. PI requires explicit validation-seeking.

3. **Foregrounded Learner hypothesis → PI, regardless of PE elements in the same question.** If the first clause of a question presents the Learner's inferred rule and the second clause offers override, the dominant speech act is PI validation-seeking.
