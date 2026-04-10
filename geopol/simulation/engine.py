"""Stage A — actor simulation.

Wraps a lightweight loop over OpenRouter modelled on snowglobe's
`Control` / `Player` pattern (`examples/ac_sim.py`). We keep the sim
self-contained here rather than depending on llm-snowglobe's heavier
optional stack (torch, transformers, llama-cpp) — the dep is still listed
in `pyproject.toml` so a `snowglobe`-backed engine can be swapped in later
without touching the pipeline boundary.

Referee rules (§"What world state means"):
- Actors see ONLY the referee-authored world state. No raw news, no Tavily,
  no other actors' private reasoning.
- Turn 0 world state = base_context + forecast question + terse RSS/ISW seed.
- Turn 1..N world state = referee narration of previous-turn actions.
"""
from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone

from ..actors import ActorSpec, ROSTER_CORE
from ..base_context import BASE_CONTEXT
from ..config import (
    MODEL_SIM_ACTOR,
    MODEL_SIM_REFEREE,
    SIM_TIMESTEPS,
    TIMESTEP_LABELS,
)
from ..llm import chat
from ..schemas import (
    ActorAction,
    SimulationResult,
    SimulationRun,
    SimulationSummary,
    SimulationTurn,
)


def _initial_world_state(question: str, news_seed: str) -> str:
    return f"""# WORLD STATE — Turn 0 (initial)

## Forecast question under consideration
{question}

## Base context (static)
{BASE_CONTEXT}

## Recent events seed (from RSS/ISW, frozen into turn 0)
{news_seed}

*From this point on, the world state is authored exclusively by the referee.*
"""


async def _actor_turn(
    actor: ActorSpec, world_state: str, private_memory: str, next_label: str
) -> ActorAction:
    user = f"""Current world state (the only information you have access to):
{world_state}

Your private memory from prior turns:
{private_memory or "(none)"}

Question: what is your private assessment of the current situation, and what
is the single most likely action you will take before the next timestep
({next_label})?

Output STRICT JSON with these keys and no prose:
{{
  "private_assessment": str,
  "public_statement": str,
  "concrete_action": str,
  "redlines_considered": [str],
  "confidence_in_action": float
}}"""
    raw = await chat(
        [
            {"role": "system", "content": actor.as_system_prompt()},
            {"role": "user", "content": user},
        ],
        model=MODEL_SIM_ACTOR,
        temperature=0.8,
    )
    data = _extract_json(raw)
    return ActorAction(
        actor_id=actor.id,
        private_assessment=data.get("private_assessment", "")[:2000],
        public_statement=data.get("public_statement", "")[:800],
        concrete_action=data.get("concrete_action", "")[:800],
        redlines_considered=list(data.get("redlines_considered", []))[:6],
        confidence_in_action=float(data.get("confidence_in_action", 0.5) or 0.5),
    )


async def _referee_narrate(
    prior_state: str, actions: list[ActorAction], timestep_label: str
) -> str:
    action_dump = "\n\n".join(
        f"### {a.actor_id}\n- public: {a.public_statement}\n- concrete action: {a.concrete_action}"
        for a in actions
    )
    system = """You are the Referee of a geopolitical simulation. You narrate the
resulting world state after each turn. Strict rules:
- You may NOT invent consequences that do not follow directly from the actions
  each player committed to this turn. If two actions are logically incompatible,
  apply the documented fallback: the action with higher actor authority in its
  own lane takes effect (e.g. Khamenei authorises Iranian action; Netanyahu
  authorises Israeli action).
- You may note second-order effects only if they are clearly implied by the
  stated actions plus the existing base context.
- Write ≤500 words of prose narration, then a compact structured block:
  ACTIVE_ACTORS: [...]
  RECENT_EVENTS: [...]
  OPEN_TENSIONS: [...]
- Do not echo private assessments; actors cannot read each other's minds.
"""
    user = f"""Prior world state:
{prior_state}

Actions committed this turn ({timestep_label}):
{action_dump}

Narrate the resulting world state for the NEXT turn."""
    return await chat(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        model=MODEL_SIM_REFEREE,
        temperature=0.4,
    )


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
    start = raw.find("{")
    end = raw.rfind("}")
    if start >= 0 and end > start:
        raw = raw[start : end + 1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


async def _run_single(
    run_idx: int,
    actors: list[ActorSpec],
    question: str,
    news_seed: str,
    timesteps: int,
    *,
    timestep_labels: list[str] | None = None,
) -> SimulationRun:
    labels = timestep_labels or TIMESTEP_LABELS
    world_state = _initial_world_state(question, news_seed)
    private_memory: dict[str, str] = {a.id: "" for a in actors}
    turns: list[SimulationTurn] = []
    for t in range(timesteps):
        label = labels[t] if t < len(labels) else f"t+{t}"
        next_label = (
            labels[t + 1] if t + 1 < len(labels) else "(sim end)"
        )
        actions = await asyncio.gather(
            *[
                _actor_turn(a, world_state, private_memory[a.id], next_label)
                for a in actors
            ]
        )
        narration = await _referee_narrate(world_state, list(actions), label)
        turns.append(
            SimulationTurn(
                timestep_label=label,
                world_state=world_state,
                actions=list(actions),
                referee_narration=narration,
            )
        )
        # Update private memory (each actor remembers only their own trajectory)
        for a, act in zip(actors, actions):
            private_memory[a.id] = (
                (private_memory[a.id] + "\n\n" if private_memory[a.id] else "")
                + f"[{label}] I assessed: {act.private_assessment}\n"
                f"  I did: {act.concrete_action}"
            )[-4000:]
        world_state = narration
    return SimulationRun(run_idx=run_idx, turns=turns)


async def _summarise(runs: list[SimulationRun]) -> SimulationSummary:
    # Compact the trace and ask the model for a structured summary.
    trace_blob = []
    for run in runs:
        trace_blob.append(f"## RUN {run.run_idx}")
        for turn in run.turns:
            trace_blob.append(f"### Turn {turn.timestep_label}")
            for a in turn.actions:
                trace_blob.append(
                    f"- **{a.actor_id}**: {a.concrete_action} (conf={a.confidence_in_action:.2f})"
                )
            trace_blob.append("")
            trace_blob.append(f"_Referee:_ {turn.referee_narration[:800]}")
            trace_blob.append("")
    blob = "\n".join(trace_blob)[:30000]
    system = (
        "You are a simulation analyst. Read the multi-run trace and produce a "
        "strict-JSON summary with these keys: dominant_trajectory (str), "
        "divergent_trajectories (list[str]), actor_behavior_patterns "
        "(dict[actor_id -> {consistent_actions: [str], variable_actions: [str], "
        "redlines_crossed: [str]}]), empirical_probabilities (dict[event -> "
        "float 0..1]), emergent_dynamics (list[str]), flags_for_council (list[str]). "
        "The flags_for_council field should list assumptions the sim made that the "
        "council should verify against fresh data."
    )
    raw = await chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": blob or "(empty trace)"},
        ],
        model=MODEL_SIM_REFEREE,
        temperature=0.2,
    )
    data = _extract_json(raw)
    return SimulationSummary(
        dominant_trajectory=data.get("dominant_trajectory", "(unknown)"),
        divergent_trajectories=list(data.get("divergent_trajectories", [])),
        actor_behavior_patterns=dict(data.get("actor_behavior_patterns", {})),
        empirical_probabilities={
            k: float(v) for k, v in dict(data.get("empirical_probabilities", {})).items()
        },
        emergent_dynamics=list(data.get("emergent_dynamics", [])),
        flags_for_council=list(data.get("flags_for_council", [])),
    )


async def run_simulation(
    question: str,
    news_seed: str,
    *,
    actors: list[ActorSpec] | None = None,
    n_runs: int | None = None,
    timesteps: int | None = None,
    horizons: list[str] | None = None,
) -> SimulationResult:
    from ..config import MC_RUNS

    actors = actors or ROSTER_CORE
    n_runs = n_runs if n_runs is not None else MC_RUNS

    if horizons:
        effective_labels = horizons
        effective_timesteps = len(horizons)
    else:
        effective_labels = TIMESTEP_LABELS
        effective_timesteps = timesteps if timesteps is not None else SIM_TIMESTEPS

    runs = []
    for i in range(n_runs):
        runs.append(
            await _run_single(
                i, actors, question, news_seed, effective_timesteps,
                timestep_labels=effective_labels,
            )
        )
    summary = await _summarise(runs)
    return SimulationResult(runs=runs, summary=summary)
