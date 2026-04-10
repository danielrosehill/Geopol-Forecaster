# Changelog

## 2026-04-10 — Self-correction from Run 2 + experiment redesign

Post-mortem of the 09/04/2026 ceasefire durability run. Applied targeted fixes based on where the pipeline underperformed.

### Experiment design changes

- **Actors reduced from 40 to 10.** New default `ROSTER_CORE` keeps only the key decision-makers: Khamenei, Netanyahu, Trump, IRGC, Hezbollah, CENTCOM, Mossad, IDF, Russia, MBS. Full 40-actor roster remains available via `ROSTER` for non-Iran scenarios.
- **Timesteps changed from 4 to 3.** New horizons: `+24h`, `+72h`, `+2 weeks` (was `now`, `+24h`, `+1 week`, `+1 month`). Focuses the simulation on the critical near-term window where the last run's predictions were densest.
- **Council horizons aligned to simulation.** Council members and chairman now forecast at `24h / 72h / 2w` (was `24h / 1w / 1m / 1y` — the "1 year" horizon had zero simulation support).

### Grounding improvements

- **Tavily queries expanded from 4 to 6.** Added `Russia China Iran nuclear facility latest` and `Strait of Hormuz shipping oil transit latest`. These cover the two biggest blind spots from Run 2 (Russian evacuation coordination and Hormuz shipping status were only caught by ISW/RSS).
- **Tavily snippet length doubled** (400 → 800 chars). Run 2's Tavily citations were too compressed to carry analytical weight.
- **RSS HTML tags stripped.** Article descriptions were leaking raw `<p>` and `<a>` tags into the fresh data bundle.

### Simulation fidelity improvements

- **Referee narration limit raised** (300 → 500 words). With 10 actors this gives ~50 words per actor per turn — enough for meaningful narration instead of generic compression.
- **Trace summary cap raised** (18k → 30k chars). Preserves more nuance for the summarisation model.

### Council quality improvements

- **Chairman max_tokens doubled** (6k → 12k). Run 2 produced an extremely detailed report; the old cap risked truncation.

### New skill

- **`run-and-publish`** — End-to-end skill: run a forecast from a user prompt, create a public repo with results and graphics, register in the Geopol-Forecasts-Index. Combines the pipeline CLI with the `new-geopol-forecast-repo` workflow.

### Self-correction log

Full diagnosis with file/line references written to `reports/SELF_CORRECTION_LOG.md`.
