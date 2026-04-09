---
layout: default
title: Geopol Forecaster
---

# Geopol Forecaster

A two-stage geopolitical forecaster that runs a multi-actor simulation
(snowglobe-pattern) followed by a multi-lens council review
(llm-council pattern) to produce a synthesised chairman report on a
forecast question.

- **Stage A — Actor simulation.** 38 persona-briefed actors take private
  assessments and commit to concrete actions across four timesteps. A
  referee model narrates the world state between turns.
- **Stage B — Council lens panel.** Six analytical lenses answer the
  question independently, cross-review each other, and a chairman
  synthesises the final forecast.
- **Grounding.** Tavily search + RSS/ISW news ingestion, frozen into
  the Turn-0 world state and seeded identically to every actor and
  every lens.

## Experiment runs

| Run ID | Date | Question | Artifacts |
|---|---|---|---|
| [2026-04-09_224838Z](runs/2026-04-09_224838Z/) | 2026-04-10 | Iran–Israel–US ceasefire durability (April 2026) | [chairman](runs/2026-04-09_224838Z/chairman_report) · [lenses](runs/2026-04-09_224838Z/stage1_answers) · [reviews](runs/2026-04-09_224838Z/stage2_reviews) · [notes](runs/2026-04-09_224838Z/experiment_notes) · [PDF](runs/2026-04-09_224838Z/report_v2.pdf) |

## Repository

Source code, roster, and raw pipeline output live in the
[Geopol-Forecaster GitHub repo](https://github.com/danielrosehill/Geopol-Forecaster).
