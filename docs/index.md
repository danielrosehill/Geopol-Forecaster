---
layout: default
title: Geopol Forecaster
---

# Geopol Forecaster

A two-stage geopolitical forecasting pipeline that publishes every
perspective in every run — actor-by-actor, turn-by-turn, lens-by-lens,
review-by-review — not just a summarised headline.

- **Stage A — Actor simulation.** A persona-briefed roster of state,
  sub-state, and institutional actors independently commits to private
  assessments and concrete actions across four timesteps. A referee
  model narrates the resulting world state between turns. Actors see
  only the referee-authored state and their own private memory.
- **Stage B — Council lens panel.** Six analytical lenses answer the
  question independently, cross-review each other, and a chairman
  synthesises the final forecast.
- **Grounding.** Tavily search + RSS/ISW news ingestion, frozen into
  the Turn-0 world state and seeded identically to every actor and
  every lens.

## Experiment runs

| Run | Date | Topic | Format |
|---|---|---|---|
| [2026-04-09_224838Z](runs/2026-04-09_224838Z/) | 2026-04-10 | Iran–Israel–US ceasefire durability (April 8 2026 deal) | 40 actors · 4 turns · 6-lens council · intel PDF |
| [2026-03-24-22-51](runs/2026-03-24-22-51/) | 2026-03-25 | Iran–Israel–US escalation forecast (pre-ceasefire) | Legacy multi-lens scaffold · PDF only |

## What each run page exposes

For post-refactor runs, every page is navigable:

- **Chairman report** — final synthesised forecast
- **Intel PDF** — cover + BLUF + body + colophon, styled as an intelligence product
- **All actors** — one page per actor with every turn's private assessment, public statement, concrete action, red lines considered, and confidence
- **All turns** — world state at start of turn, all actions committed that turn, referee narration into the next turn
- **All lens answers** — Stage 1 first-round answers from each council lens
- **All cross-reviews** — Stage 2 cross-reviews between lenses

## Repository

Source, roster, prompts, and publishing scripts live in the
[Geopol-Forecaster GitHub repo](https://github.com/danielrosehill/Geopol-Forecaster).
