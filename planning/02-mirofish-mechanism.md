# 02 — The MiroFish Mechanism

*What the MiroFish project does, and what specifically is worth borrowing for geopolitical forecasting.*

Source: https://github.com/666ghj/MiroFish — "A Simple and Universal Swarm Intelligence Engine, Predicting Anything."

## What MiroFish actually is

**Not a deep research agent. Not web-grounded.** It is an **agent-based simulation forecaster**. The core insight is that for many prediction problems — especially those driven by the decisions of a small number of actors — you can forecast better by *simulating the actors* than by asking a single LLM to reason about them from the outside.

### Architecture (as documented)

1. **Graph building.** Seed materials (reports, articles, scenario descriptions) are ingested. Entities and relationships are extracted into a GraphRAG. Individual and collective memory is injected.
2. **Environment setup.** Personas are generated for each entity. Each agent gets configuration: personality, goals, memory, behavioural rules.
3. **Simulation.** Agents interact in a shared environment over multiple turns. They observe each other's public actions, update their private memory, and act again. MiroFish runs this on top of **OASIS** (Open Agent Social Interaction Simulations) from CAMEL-AI, with **Zep Cloud** handling long-term memory.
4. **Report generation.** A "ReportAgent" with a toolset reads the post-simulation state and writes a prediction report. Users can also chat with the simulated agents after the fact.
5. **God-view intervention.** The user can inject variables mid-simulation ("what if Iran's Supreme Leader dies next week?") and watch the system re-stabilise.

### Key technical characteristics

- **No web search, no live grounding.** The only inputs are the seed documents.
- **Scales to thousands of agents** — designed originally for social-media-style emergent-behaviour simulation.
- **Heavy infrastructure:** OASIS, CAMEL-AI, Zep Cloud, GraphRAG. Needs Python 3.11–3.12, uv, Docker.
- **LLM-provider-agnostic** (any OpenAI-SDK-compatible endpoint).

## Why this is interesting for geopolitical forecasting

Conflict forecasting has a structural property that makes it a *natural* fit for actor simulation: **a small number of decision-makers dominate the outcome space.** The Iran-Israel-US conflict is not driven by thousands of independent agents — it's driven by ~10 people and ~5 institutions whose decision calculus is partially knowable.

This is how real intelligence shops work:
- **Red team / blue team wargaming** — CIA, Mossad, IDF J-3 all run this
- **Analytic tradecraft** (Heuer): "analysis of competing hypotheses," "devil's advocacy," "team A / team B"
- **Reference-class forecasting** on actor behaviour ("how does Khamenei historically respond to X?")

Your current 6 lenses approximate this with *prompt diversity* — six different framings of the same external observer. MiroFish's mechanism is different: **inhabit the actors** and see what they do.

## The specific mechanism worth stealing

Strip MiroFish down to its essence. The irreducible loop is:

```
for t in timesteps:
    world_state[t] = summarize(world_state[t-1], actions[t-1])

    for actor in actors (in parallel):
        private_assessment[actor][t] = LLM(
            role = actor.persona,
            input = world_state[t] + actor.private_memory[t-1]
        )
        action[actor][t] = LLM(
            role = actor.persona,
            input = private_assessment[actor][t],
            constraint = "output one concrete action this actor would take next"
        )
        actor.private_memory[t] = update(actor.private_memory[t-1], action[actor][t])

    actions[t] = {actor: action[actor][t] for actor in actors}
    redlines_triggered[t] = referee_llm(actions[t], world_state[t])
```

That's it. No GraphRAG, no OASIS, no Zep, no social graph. Just:
- A fixed cast of ~8–12 actors, each with a hand-written persona
- A shared world state that updates every turn
- Each actor sees the world state and their own private history
- Each actor outputs a private assessment and a concrete next action
- A referee LLM resolves conflicts and flags red-line crossings
- Run N independent simulations (different random seeds) → empirical probability distribution over outcomes

## What you get that the current pipeline doesn't

1. **Actor-attributed predictions.** Instead of "there is a 60% chance of retaliatory strikes," you get "Khamenei authorises a limited retaliatory strike on day 3 because his internal assessment weighs regime survival above US deterrence, and IRGC Command's proposed target set excludes US personnel to avoid direct US entry." Specific, falsifiable, auditable.

2. **Emergent dynamics.** Actor A reacts to actor B's action, which actor B took in response to actor C. Single-shot forecasting can't capture reaction chains; simulation does, trivially.

3. **Empirical probability from repeated runs.** Run the simulation 10× with temperature 0.8. Count how often each outcome emerges. That *is* a probability distribution — grounded in the model's own behaviour, not pulled from the model's numerical intuition (which is famously miscalibrated).

4. **Red-line stress testing.** You can inject perturbations between turns ("assume a mass-casualty event on day 2") and observe which actors escalate, which de-escalate, and which fracture internally.

5. **Methodological diversity.** Your current 6 lenses are all the same *method* (external-observer inference) with different framings. Adding simulation gives you a genuinely different method in the ensemble. When simulation and inference agree, confidence is high. When they diverge, that divergence is itself information.

## What you don't get, and what to watch out for

- **Garbage-in-garbage-out on personas.** The quality of the forecast is bounded by the quality of the persona briefs. A shallow "Khamenei is hardline" persona produces cartoon outputs. Real personas need: historical decision patterns, known advisors, stated red lines, institutional constraints, domestic-politics pressures. This is research work, not prompting work.
- **LLMs role-playing real world leaders is a known failure mode for caution/sycophancy.** The model may refuse to commit to specific actions, or hedge into uselessness. Needs careful prompting to force commitment ("you must output exactly one action; hedging is not permitted").
- **Simulation drift.** Over many turns, actors can wander into implausible state space. Keep simulations short (3–5 turns max) and re-ground on real news between turns where possible.
- **Cost.** N actors × T turns × R runs × 2 calls per actor per turn = a lot of LLM calls. For 10 actors × 4 turns × 5 runs × 2 calls = 400 calls per forecast. Cheap on Grok/Gemini-Flash, expensive on frontier models. Route via OpenRouter with model choice per role.
