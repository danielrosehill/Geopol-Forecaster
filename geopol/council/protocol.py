"""Stage B — llm-council's 3-stage protocol, adapted from
karpathy/llm-council/backend/council.py:

  1. Parallel query        — each lens answers independently
  2. Anonymised peer review — each lens critiques the other 5, blind
  3. Chairman synthesis     — chairman writes the final report directly

Differences from the upstream:
- Members are our 6 lens directives, not a multi-provider model list.
- Each member receives the same fixed bundle of inputs (base_context,
  fresh_data, simulation_summary, question) — no per-member retrieval.
- The chairman writes a full markdown report, not just an answer.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass

from ..base_context import BASE_CONTEXT
from ..config import MODEL_COUNCIL_CHAIRMAN, MODEL_COUNCIL_MEMBER
from ..llm import chat
from ..schemas import FreshData, SimulationResult
from .lenses import LENSES, LensSpec


@dataclass
class CouncilMemberAnswer:
    lens: LensSpec
    answer: str


@dataclass
class CouncilPeerReview:
    reviewer_lens_id: str
    critique: str


@dataclass
class CouncilResult:
    stage1: list[CouncilMemberAnswer]
    stage2: list[CouncilPeerReview]
    final_report_markdown: str


def _member_system_prompt(lens: LensSpec) -> str:
    return f"""You are a forecasting analyst operating under the **{lens.name}** lens.

Directive: {lens.directive}

You have three sources of information about the situation:

(1) BASE CONTEXT — static background on the conflict, actors, and geography.
(2) FRESH DATA — live Tavily search results and RSS/ISW headlines. This is
    ground truth as of the timestamp noted in the bundle.
(3) SIMULATION SUMMARY — the output of an actor simulation with personas for
    the key decision-makers. This is NOT reality; it is a model of how those
    actors would plausibly behave. The simulation has declared its own
    assumptions in `flags_for_council` — verify them against the fresh data.

Your task:
- Produce a forecast under your lens's directive, across 24h / 72h / 2 week
  horizons.
- For each prediction, note whether it is supported by fresh data, by the
  simulation, or both.
- Include a `simulation_divergence_notes` section describing where your
  assessment differs from the simulation, and why. If the simulation surfaced
  something you would not have predicted from the fresh data alone, take it
  seriously.
- Markdown output. Be specific, cite sources from FRESH DATA where possible,
  and do not hedge generically.
"""


def _bundle(question: str, fresh: FreshData, sim: SimulationResult) -> str:
    sim_json = sim.summary.model_dump_json(indent=2)
    return f"""# FORECAST QUESTION
{question}

# BASE CONTEXT
{BASE_CONTEXT}

# FRESH DATA
{fresh.as_markdown()}

# SIMULATION SUMMARY (Stage A)
```json
{sim_json}
```
"""


async def _stage1_member(lens: LensSpec, bundle: str) -> CouncilMemberAnswer:
    content = await chat(
        [
            {"role": "system", "content": _member_system_prompt(lens)},
            {"role": "user", "content": bundle},
        ],
        model=MODEL_COUNCIL_MEMBER,
        temperature=0.6,
    )
    return CouncilMemberAnswer(lens=lens, answer=content)


async def _stage2_review(
    reviewer: LensSpec,
    anonymised_answers: list[tuple[str, str]],
    bundle: str,
) -> CouncilPeerReview:
    blob = "\n\n".join(
        f"## {label}\n{ans}" for label, ans in anonymised_answers
    )
    system = f"""You are a forecasting analyst under the **{reviewer.name}** lens.
Directive: {reviewer.directive}

You are performing blind peer review of other analysts' forecasts. You do not
know which analyst wrote which response. Critique each one on:
- Specificity (named actors, named actions, calibrated timelines)
- Fidelity to fresh data and simulation evidence
- Internal consistency
- Lens-appropriate sharpness (is it hedge-speak or a real forecast?)

End with a ranked list best → worst. Use exact labels (Response A, Response B, …).
"""
    user = f"""Shared context all analysts saw:
{bundle}

Anonymised responses to critique:
{blob}"""
    content = await chat(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        model=MODEL_COUNCIL_MEMBER,
        temperature=0.4,
    )
    return CouncilPeerReview(reviewer_lens_id=reviewer.id, critique=content)


async def _stage3_chairman(
    question: str,
    bundle: str,
    stage1: list[CouncilMemberAnswer],
    stage2: list[CouncilPeerReview],
) -> str:
    answers_blob = "\n\n".join(
        f"## {m.lens.name} Lens\n{m.answer}" for m in stage1
    )
    reviews_blob = "\n\n".join(
        f"## Review by {r.reviewer_lens_id}\n{r.critique}" for r in stage2
    )
    system = """You are the Chairman of a 6-lens forecasting council. Six analysts
answered the same question under different directives, then reviewed each
other anonymously. Your job is to write the FINAL REPORT directly — there is
no downstream synthesis stage.

Write the report in Markdown with these sections, in this order:

1. **Headline forecast** — one paragraph with an explicit confidence statement
   and a probability-band for the core outcome.
2. **Key predictions** — a table. Columns: prediction | horizon (24h / 72h / 2w)
   | probability | confidence | supported_by (fresh_data / simulation / both / neither).
3. **Where research and simulation agree** — high-confidence claims.
4. **Where they diverge** — flagged as critical uncertainties, with explanation.
5. **Simulation blind-spot check** — reaction chains the sim surfaced that the
   fresh data did not.
6. **Per-lens contributions** — one paragraph per lens, summarising what it
   added and how peer review scored it.
7. **Simulation appendix** — actor-by-actor behaviour patterns, empirical
   probabilities, and the sim's `flags_for_council` and whether fresh data
   confirmed each.

Be concrete. Name actors. Avoid hedge-speak. Cite fresh data where possible."""
    user = f"""# ORIGINAL CONTEXT BUNDLE
{bundle}

# STAGE 1 — 6 LENS ANSWERS
{answers_blob}

# STAGE 2 — BLIND PEER REVIEWS
{reviews_blob}

Write the final report now."""
    return await chat(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        model=MODEL_COUNCIL_CHAIRMAN,
        temperature=0.5,
        max_tokens=12000,
    )


async def run_council(
    question: str,
    fresh: FreshData,
    sim: SimulationResult,
) -> CouncilResult:
    bundle = _bundle(question, fresh, sim)

    # Stage 1 — parallel
    stage1 = await asyncio.gather(*[_stage1_member(l, bundle) for l in LENSES])

    # Stage 2 — blind peer review (label responses A..F)
    labels = [chr(ord("A") + i) for i in range(len(stage1))]
    anonymised = [(f"Response {lbl}", m.answer) for lbl, m in zip(labels, stage1)]
    stage2 = await asyncio.gather(
        *[_stage2_review(LENSES[i], anonymised, bundle) for i in range(len(LENSES))]
    )

    # Stage 3 — chairman writes the report
    report = await _stage3_chairman(question, bundle, list(stage1), list(stage2))

    return CouncilResult(
        stage1=list(stage1), stage2=list(stage2), final_report_markdown=report
    )
