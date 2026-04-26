"""Study-2-only Preference-Induction proposer.

Subclasses the Study 1 `PreferenceInductionProposer` and overrides only the
system/user prompts so that the agent can generate hypotheses from **common
sense and prior knowledge** about typical household organisation — not just
from accumulated confirmed_actions evidence.

This reflects the updated LL definition:
  PI questions may draw on the learner's domain knowledge, not only on
  placement observations collected in the current session.

Not changed:
  - Structured-output schema (PreferenceQuestionIntentBatch)
  - _normalize_preference_induction_intents post-processing
  - Model plumbing / __init__
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from proposers import (  # noqa: E402
    PreferenceInductionProposer,
    PreferenceQuestionIntent,
    _normalize_preference_induction_intents,
)
from agent_schema import AgentState  # noqa: E402


class Study2PreferenceInductionProposer(PreferenceInductionProposer):
    """PI proposer for Study 2: hypotheses may come from common sense."""

    def propose(
        self,
        *,
        state: AgentState,
        max_intents: int = 3,
        guidance: str = "",
    ) -> List[PreferenceQuestionIntent]:

        system_prompt = f"""
You are a proactive household-organisation agent running a Learner-Led (LL) dialogue.

Your role: **Active Constructor**. You form hypotheses about where items belong
based on (a) any placement observations already collected AND (b) common sense
and general knowledge about typical household organisation — e.g. you know that
chargers usually live near beds, that kitchenware belongs in the kitchen, that
books often go on shelves.

You do NOT need to wait for accumulated evidence before proposing a hypothesis.
You may propose a sensible rule at any point, as long as it has not already
been confirmed or rejected.

Your job:
Propose a small number of high-value preference-induction questions.
Each question presents a candidate placement rule and asks the user to
confirm, refine, or reject it.

Question form — STRICT. The question MUST be a confirmation question that
puts a hypothesis to the user; the user's job is to confirm, refine, or reject
it. The canonical template is:

  "I'd expect [category description] to go in the [receptacle] — does that
   match how you like to organise things?"

Acceptable openers: "I'd expect ...", "I'd guess ...", "I think ...".
Acceptable closers: "is that right?", "does that match how you organise things?",
"is that how you like it?".

NEVER output a question in any of these forms (these are PE, not PI):
- "What do you usually put in the [receptacle]?"
- "What kinds of items do you keep in the [receptacle]?"
- "How do you usually organise [category]?"
- "Where do you put [object/category]?"
A PE question asks the user to GENERATE the rule. A PI question asks the user
to ADJUDICATE a rule the agent already proposed. Do not invite the user to
list items — state your hypothesis and ask them to confirm it.

Rules:
- This pattern is always "preference_induction".
- Do not output action-oriented or preference-eliciting questions.
- Return at most {max_intents} intents.
- Use only exact seen object names in covered_objects (leave empty if hypothesis
  is category-level and no specific objects match yet).
- Hypotheses should describe a CATEGORY or SHARED ATTRIBUTE (material, size,
  power source, usage context), not just a single object.
  Good: "small plug-in bedside electronics → nightstand"
  Bad:  "the phone charger → nightstand"
- Do not propose a hypothesis that is already in confirmed_preferences or
  negative_preferences.
- Prefer hypotheses that target receptacles not yet covered by confirmed_preferences.
- Use the guidance as a soft instruction about what kind of rule to propose next.
""".strip()

        covered_receptacles = sorted({
            cp.get("receptacle") for cp in state["confirmed_preferences"]
            if cp.get("receptacle")
        })
        uncovered_receptacles = sorted({
            r for r in state["receptacles"]
            if r not in set(covered_receptacles)
        })

        user_prompt = f"""
Scene objects (seen so far):
{state["seen_objects"]}

Unresolved objects:
{state["unresolved_objects"]}

Receptacles in this scene:
{state["receptacles"]}

Placement observations collected so far (may be empty — that is fine):
{state["confirmed_actions"]}

Rules already established (do NOT repropose these):
{state["confirmed_preferences"]}

Rejected hypotheses (do NOT repropose these):
{state["negative_preferences"]}

Receptacles already covered by confirmed preferences:
{covered_receptacles}

Receptacles NOT yet covered — PRIORITIZE these:
{uncovered_receptacles}

Guidance:
{guidance}

Propose up to {max_intents} preference-induction intents.
Each intent must include:
- question_pattern = "preference_induction"
- hypothesis = a concise category-level placement rule (may be based on common
  sense, not only on placement observations above)
- covered_objects = exact seen object names plausibly covered by this rule
  (may be empty if hypothesis is broad or observations are sparse)
- receptacle = exact receptacle name if there is a clear target, otherwise null
- priority = 0.0 to 1.0
- question = an active, direct CONFIRMATION question in the canonical PI format:
  "I'd expect [category] to go in the [receptacle] — does that match how you
   like to organise things?"
  The question MUST start with one of: "I'd expect", "I'd guess", "I think".
  The question MUST NOT ask the user "what do you put / what kinds of items /
  how do you organise / where do you put" — those are PE forms and are
  forbidden in this proposer.
""".strip()

        result = self.structured_model.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ])
        return _normalize_preference_induction_intents(
            intents=result.intents,
            state=state,
            max_intents=max_intents,
        )
