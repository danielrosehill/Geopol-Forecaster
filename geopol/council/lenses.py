"""The 6 lens directives — ported verbatim from `src/lib/types.ts`.

Per locked decisions these ARE the council members. Each lens is a
system-prompted persona over the same base model (Sonnet 4.6). Diversity
comes from the prompts, not the models.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LensSpec:
    id: str
    name: str
    directive: str


LENSES: list[LensSpec] = [
    LensSpec(
        id="neutral",
        name="Neutral",
        directive=(
            "Provide your honest, unbiased assessment of how this conflict will "
            "evolve. Do not lean optimistic or pessimistic."
        ),
    ),
    LensSpec(
        id="pessimistic",
        name="Pessimistic",
        directive=(
            "Model the worst-case scenarios. Focus on escalation paths, failed "
            "diplomacy, and dangerous miscalculations."
        ),
    ),
    LensSpec(
        id="optimistic",
        name="Optimistic",
        directive=(
            "Model the best-case scenarios. Focus on de-escalation paths, "
            "diplomatic breakthroughs, and restraint by actors."
        ),
    ),
    LensSpec(
        id="blindsides",
        name="Blindsides",
        directive=(
            "Identify low-probability but conceivable pivots and black swan "
            "events that could fundamentally change the trajectory."
        ),
    ),
    LensSpec(
        id="probabilistic",
        name="Probabilistic",
        directive=(
            "Use probabilities and historical precedent to make mathematically "
            "rigorous predictions. Assign explicit probability ranges to outcomes."
        ),
    ),
    LensSpec(
        id="historical",
        name="Historical",
        directive=(
            "Make predictions solely through the lens of historical actor "
            "behaviour in similar circumstances. Deliberately ignore statistical "
            "weight of evidence to produce a differentiated, historically-grounded "
            "response."
        ),
    ),
]
