"""Study-2-only Question Policy Controller.

Subclasses the Study 1 `QuestionPolicyController`. Two changes:

  1. `_induction_is_available` returns True unconditionally so PI can be
     proposed from turn 1 without the Study 1 evidence gate (≥2 unsummarised
     confirmed_actions). This realises the §3.3.1 PI definition that
     "the source of the hypothesis may be prior knowledge, intuitive
     judgment, OR accumulated dialogue observations".

  2. `_rule_learner_led` is replaced by an LLM-based selection: rather than
     hardcoding turn-by-turn AO/PI choice, we let the model freely choose
     between AO and PI given the current AgentState, guided by a Study 2
     flavoured `_system_prompt` (allows common-sense PI from turn 1, no
     "evidence sparse → must AO" bias).

All other modes (TO, UL, HYB) inherit the parent rule-based behaviour
unchanged.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from question_policy import QuestionPolicyController, QuestionDecision, PolicyMode  # noqa: E402
from agent_schema import AgentState, QuestionPattern  # noqa: E402


_STUDY2_LL_PROMPT = """
Strategy: Learner-Led (LL) — Study 2.
- Two roles are available: action_oriented (AO) and preference_induction (PI).
  Both are valid at any turn, including turn 1 when no evidence has been
  collected yet. Choose the one that best fits the current state.

- AO (ask about one specific seen object's placement):
  * Use AO to learn or verify where a single concrete object goes.
  * Good triggers: (a) you want to ground your prior before generalising —
    pick one object whose placement is most informative, (b) a hypothesis
    was just rejected and you need fresh evidence, (c) boundary objects
    that don't fit any existing rule, (d) you need one more concrete data
    point at a thinly-supported receptacle.
  * AO is fine as the OPENING move when you want to anchor the dialogue in
    a concrete observation before risking a category-level guess.

- PI (propose a category-level rule for the user to confirm/refine/reject):
  * The hypothesis MAY come from common sense or prior knowledge — you do
    NOT need accumulated confirmed_actions before proposing a PI.
  * The hypothesis SHOULD come from accumulated confirmed_actions when 2+
    actions point at the same receptacle and would compress into one rule.
    This "summarising what the user just told you" path is an essential
    LL behaviour — do not skip it in favour of more common-sense guesses.
  * Good triggers: (a) an uncovered receptacle has a plausible default
    category (e.g. "books → bookshelf"), (b) 2+ confirmed_actions at the
    same receptacle and a rule would compress them, (c) you have a strong
    common-sense prior worth testing.
  * PI is fine as the OPENING move when your common-sense prior about the
    room is strong enough that a category rule is worth proposing first.

- Decision principle: pick the pattern that reduces the most uncertainty
  given the CURRENT state. Mix AO and PI freely across turns — neither
  should dominate by default. After 2+ confirmed_actions at the same
  receptacle, PI to summarise them is usually the highest-value move. Do
  NOT choose preference_eliciting in this strategy.
""".strip()


class Study2QuestionPolicyController(QuestionPolicyController):
    """Policy controller for Study 2.

    LL mode delegates pattern selection to the LLM (free AO/PI choice via
    `_system_prompt`); evidence gate on PI is removed.
    """

    def _induction_is_available(self, *, state: AgentState) -> bool:
        # Study 2 LL allows common-sense PI; remove the parent ≥2-actions gate.
        return True

    def _rule_learner_led(
        self,
        *,
        state: AgentState,
        allowed_patterns: List[QuestionPattern],
    ) -> QuestionDecision:
        # No turn-by-turn hardcoded choice. Delegate to LLM-based selection
        # which uses the Study 2 LL system prompt below.
        return self._llm_select(
            state=state,
            allowed_patterns=allowed_patterns,
            mode="learner_led",
        )

    def _system_prompt(self, *, mode: PolicyMode) -> str:
        # Override parent's LL block with the Study 2 wording. All other modes
        # use the parent's prompt unchanged.
        if mode != "learner_led":
            return super()._system_prompt(mode=mode)

        return f"""
You are the high-level question policy controller for a household rearrangement agent.

Your job:
- choose exactly one next question pattern from the allowed patterns
- produce one short guidance string for the downstream proposer

The guidance should:
- be one sentence
- explain what the proposer should focus on next
- not be a full user-facing question
- help the proposer choose a good object or hypothesis

General rules:
- Use only the allowed question patterns.
- Respect the strategy instructions.
- Be state-driven; base the decision on the AgentState summary, not on
  fixed turn-number rules.
- If action_oriented is chosen, the guidance may suggest probing a
  boundary, grounding a recent hypothesis, or covering a receptacle that
  has no rule yet.
- If preference_induction is chosen, the guidance should name the
  receptacle / category the proposer should target, and may hint that
  common-sense priors are acceptable when evidence is thin.

{_STUDY2_LL_PROMPT}

Return only structured output.
""".strip()
