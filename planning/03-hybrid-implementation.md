# 03 — Hybrid Implementation: Deep Research + Actor Simulation

*A two-phase pipeline where an actor simulation (MiroFish-inspired) runs first, then its output feeds a deep-research + forecasting phase that has both the live news AND a summary of what the simulation produced.*

## The core idea

The user's framing — which is the right one — is:

> **Phase A:** Simulated actors take actions in a sandbox (MiroFish mechanism).
> **Phase B:** A second agent gets the live news **and** a summary of what Phase A yielded, then produces the final forecast.

This ordering matters. If the simulation runs *after* the research, the simulation is anchored on what actually happened — useful, but the simulation becomes a commentary on reality rather than an independent signal. If the simulation runs *before* or *in parallel with* the research, the two signals can be compared as genuinely independent predictions, and divergences become diagnostic.

We go with the user's framing: **simulation first, research second, synthesis has access to both.**

## Pipeline shape

```
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 0 — Static context                                             │
│   base_context.md (conflict background, actors, red lines, geography)│
│   RSS headlines + ISW reports (lightweight seed, not full research)  │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
           ┌────────────────────┴────────────────────┐
           ▼                                         ▼
┌───────────────────────┐            ┌──────────────────────────────┐
│ STAGE A — Simulation  │            │ STAGE B — Deep Research      │
│  (actor sandbox)      │            │  (gpt-researcher + Tavily)   │
│                       │            │                              │
│  Inputs:              │            │  Inputs:                     │
│   - base_context      │            │   - forecast question        │
│   - RSS/ISW seed      │            │   - base_context             │
│   - question          │            │   - RSS/ISW seed             │
│                       │            │                              │
│  Output:              │            │  Output:                     │
│   simulation_trace    │            │   ground_truth_with_citations│
│   (full turn-by-turn) │            │                              │
│   +                   │            │                              │
│   simulation_summary  │            │                              │
│   (condensed for B)   │            │                              │
└───────────┬───────────┘            └───────────────┬──────────────┘
            │                                         │
            │       ┌─────────────────────────────────┘
            ▼       ▼
┌───────────────────────────────────────────────────────────────────┐
│ STAGE C — Informed forecasting (the 6 lenses)                     │
│                                                                    │
│  Each lens receives:                                               │
│    - ground_truth (from B)                                         │
│    - simulation_summary (from A)                                   │
│    - base_context                                                  │
│                                                                    │
│  Lens prompt is extended to explicitly consider:                   │
│    "Compare your assessment to what the actor simulation produced.│
│     Where do you agree? Where do you disagree, and why?"          │
│                                                                    │
│  Output: 6 structured lens forecasts (as today)                    │
│          + 1 new field: simulation_divergence_notes                │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│ STAGE D — Synthesis & Report                                      │
│   Executive summary now has explicit section:                      │
│     "Where research-based and simulation-based forecasts agree"    │
│     "Where they diverge, and what that tells us"                   │
│   Typst PDF render                                                 │
└───────────────────────────────────────────────────────────────────┘
```

## Stage A: Actor simulation (detailed)

### A.1 Actor roster

Hand-curated list, stored in `geopol/actors/roster.yaml`. ~10–12 actors is the sweet spot.

```yaml
- id: khamenei
  name: Ali Khamenei
  role: Iran Supreme Leader
  institution: Office of the Supreme Leader
  persona_brief: |
    85-year-old cleric. Final authority on all strategic military decisions.
    Decision-making is consultative but not democratic — relies on a small
    inner circle including IRGC commander and Quds Force leadership. Has
    consistently prioritised regime survival over ideological maximalism
    when forced to choose (see: JCPOA acceptance 2015, restraint after
    Soleimani assassination 2020). Deep historical memory of Iran-Iraq war
    shapes his tolerance for prolonged conflict. Distrusts direct US
    negotiation channels but has accepted Omani and Qatari intermediation.
  known_red_lines:
    - direct strikes on Iranian nuclear facilities
    - strikes on his person or inner circle
    - visible regime instability
  typical_response_pattern: |
    Absorbs first blow, signals restraint publicly, authorises proportional
    retaliation via proxies before direct action. Prefers deniable response
    when possible. Escalates deliberately, not impulsively.
  constraints:
    - must maintain IRGC loyalty
    - must not appear weak domestically
    - economic pressure from sanctions limits long conflict tolerance

- id: netanyahu
  name: Benjamin Netanyahu
  role: Israeli PM
  ...

- id: trump
  name: Donald Trump
  role: US President
  ...

- id: irgc_command
  name: IRGC Command (collective)
  ...

- id: hezbollah_sg
  ...

- id: houthi_leadership
  ...

- id: mbs
  name: Mohammed bin Salman
  role: Saudi Crown Prince
  ...

- id: erdogan
  ...

- id: qatari_mediator
  ...

- id: centcom
  ...
```

Writing these personas is the **single highest-leverage task** in the whole project. They should cite historical decisions, name advisors, list actual institutional constraints. Two hours per actor minimum. This is research, not prompting.

### A.2 Simulation loop

```python
# geopol/simulation/engine.py

async def run_simulation(
    question: str,
    actors: list[Actor],
    base_context: str,
    news_seed: str,
    timesteps: int = 4,           # e.g. now, +24h, +1w, +1m
    n_runs: int = 5,              # monte carlo
) -> SimulationResult:
    runs = []
    for run_idx in range(n_runs):
        world_state = initial_state(base_context, news_seed, question)
        turns = []

        for t in range(timesteps):
            # Each actor assesses and acts in parallel
            actor_outputs = await asyncio.gather(*[
                actor_turn(actor, world_state, actor.private_memory)
                for actor in actors
            ])

            # Referee resolves interactions, updates world state
            world_state = await referee_update(
                prev_state=world_state,
                actor_actions=actor_outputs,
                timestep_label=TIMESTEP_LABELS[t],
            )

            # Each actor updates its private memory
            for actor, output in zip(actors, actor_outputs):
                actor.private_memory = await update_memory(
                    actor.private_memory, output, world_state
                )

            turns.append(Turn(
                timestep=TIMESTEP_LABELS[t],
                world_state=world_state,
                actor_outputs=actor_outputs,
            ))

        runs.append(Run(run_idx=run_idx, turns=turns))

    return SimulationResult(runs=runs, summary=summarize_runs(runs))
```

### A.3 Actor turn prompt (sketch)

```
SYSTEM:
You are simulating the decision-making of {actor.name}, {actor.role}.

Persona:
{actor.persona_brief}

Known red lines: {actor.known_red_lines}
Typical response pattern: {actor.typical_response_pattern}
Institutional constraints: {actor.constraints}

Rules:
- You are NOT an external analyst. You ARE this actor.
- Speak in first person where appropriate.
- Commit to a specific action. Hedging is not permitted.
- Your action must be consistent with this actor's historical pattern unless
  you can justify the deviation from within the persona's own logic.

USER:
Current world state:
{world_state}

Your private memory from prior turns:
{private_memory}

Question: what is your private assessment of the current situation, and
what is the single most likely action you will take before the next
timestep ({next_timestep_label})?

Output (structured):
  private_assessment: str   # 2-3 sentences, in character
  public_statement: str     # what you say publicly, if anything
  concrete_action: str      # the specific action — military, diplomatic,
                            # economic, covert — be specific about target,
                            # scale, timing
  redlines_considered: list[str]  # any red lines you consciously chose
                                  # to respect or cross
  confidence_in_action: float  # 0.0–1.0
```

### A.4 Summarisation for Stage C

After all N runs complete, we need a **compact summary** that Stage C can consume. Full traces are too long. Summary includes:

```python
SimulationSummary:
    dominant_trajectory: str      # modal outcome across runs
    divergent_trajectories: list  # minority outcomes that appeared in 2+ runs
    actor_behavior_patterns:
        {actor_id: {
            consistent_actions: list[str],     # actions this actor took in ≥4/5 runs
            variable_actions: list[str],       # actions that varied across runs
            redlines_crossed: list[str],       # red lines crossed in any run
        }}
    empirical_probabilities:
        {event: probability}       # e.g. "limited Iranian retaliation within 72h": 0.8
    emergent_dynamics: list[str]  # reaction chains the simulation surfaced
    flags_for_research: list[str] # "simulation assumed X about Saudi stance;
                                  # research should verify"
```

That last field — **flags_for_research** — is the handoff to Stage B/C. The simulation surfaces its own assumptions, and the research phase is asked to verify them.

## Stage B: Deep research (independent)

Runs **in parallel** with Stage A (no dependency). Uses gpt-researcher + Tavily + OpenRouter.

- Input: the forecast question + base_context + RSS/ISW seed
- Output: `01-ground-truth.md` with citations
- Key property: **Stage B does not see the simulation output.** It's an independent signal. We want it to be anchored only in real sources so its comparison with Stage A is meaningful.

## Stage C: Informed forecasting

Each of the 6 lenses now receives **three inputs**:

1. `base_context` (static)
2. `ground_truth` from Stage B (real)
3. `simulation_summary` from Stage A (simulated)

The lens prompt is extended:

```
You have two independent sources of information about this situation:

(1) GROUND TRUTH — a researched, cited summary of what has actually
    happened and what is currently known.

(2) SIMULATION SUMMARY — the output of an actor-based simulation that
    ran {n_runs} Monte Carlo runs with personas for the key decision-makers.
    This is NOT reality. It is a model's best guess at how the actors
    would behave if the situation evolved.

Your task:
  - Produce your forecast in the usual structured format.
  - For each prediction, note whether it is supported by the ground truth,
    by the simulation, or both.
  - Add a `simulation_divergence_notes` field: where does your assessment
    differ from what the simulation produced, and why? If the simulation
    surfaced something you would not have predicted from ground truth alone,
    take it seriously — that is the value of having two independent signals.
```

Schema addition:
```python
class LensForecast(BaseModel):
    # existing fields...
    simulation_divergence_notes: str
    predictions_supported_by: dict[str, Literal["research", "simulation", "both", "neither"]]
```

## Stage D: Synthesis & report

The executive summary agent now produces an extra section:

**"Cross-method agreement and divergence"**
- Where research and simulation agree, confidence is highest → headline predictions
- Where research suggests X but simulation suggests Y, flag as a critical uncertainty
- Where simulation surfaced a reaction chain research didn't consider, flag as a blind spot
- Where research has hard facts that contradict simulation assumptions, note that the simulation should be re-run with corrected priors

Typst template gets one new section: **"Simulation Appendix"** showing:
- The actor roster used
- Per-run trajectories (compact table)
- Empirical probabilities with confidence intervals
- The simulation's own flagged assumptions and whether research confirmed them

## What this buys us

1. **Two genuinely independent forecasting methods in one pipeline.** Not 6 flavours of the same method.
2. **Actor-attributed predictions** with specific reasoning chains you can audit.
3. **Empirical probabilities** from repeated simulation runs — more honest than LLM-generated probability numbers.
4. **Divergence as a signal.** The interesting cases are where research and simulation disagree. Those are the predictions worth questioning.
5. **Audit trail.** Every claim in the final report traces back to either a cited source (research) or a specific actor's simulated reasoning (simulation) — not "the LLM said so."

## What to build first (implementation order)

1. **`planning/` docs** — this file, `01-current-approach.md`, `02-mirofish-mechanism.md` (done when you're reading this).
2. **Actor roster** — hand-write 10 actor personas. This is the hardest and highest-value task. No code yet.
3. **Python scaffold** — `uv init`, `pyproject.toml`, `geopol/` package structure, OpenRouter client, Typst renderer port.
4. **Minimum simulation loop** — 3 actors, 2 timesteps, 1 run. Just prove the loop works and produces sensible output.
5. **Full simulation** — all actors, 4 timesteps, 5 runs. Summarisation step.
6. **Deep research integration** — gpt-researcher wired up with Tavily + OpenRouter.
7. **Stage C lens prompts** — extended to consume both inputs.
8. **Stage D synthesis + Typst** — port from TS.
9. **End-to-end run** on the ceasefire question.
10. **Evaluate.** If simulation output is noise, tune personas or drop Stage A. If it's signal, keep iterating.

## Open questions to resolve before coding

- **Model choice per role.** Simulation actors should probably use Grok or Gemini Flash (cheap, fast, high variance). Referee should be a stronger model (Claude Sonnet?). Research should use whatever gpt-researcher defaults to. Decide per-call routing in `geopol/config.py`.
- **Monte Carlo N.** 5 runs is a guess. May need 10+ for stable probabilities. Budget-dependent.
- **Persona grounding.** Do we let actors see news headlines, or only the abstracted world state? Risk: if actors see headlines, they just parrot them and the simulation collapses to inference. Recommendation: actors see ONLY the referee-maintained world state, not raw news.
- **Referee implementation.** How does the referee actually resolve conflicts? Simplest: LLM reads all actor actions, narrates the resulting world state. Risk: referee hallucinates outcomes the actors didn't imply. Mitigation: referee prompt is strict — "only report consequences that follow directly from the actions listed."
- **Failure modes.** What if an actor refuses to commit to an action (sycophancy)? What if two actors' actions are logically incompatible? Referee handles, with explicit fallback rules.
