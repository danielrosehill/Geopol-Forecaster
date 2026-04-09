# Deferred: Frontend Refactor

The Next.js frontend (`src/app/`, SQLite review UI, Markdown editor for ground truth/SITREP review) is **deferred indefinitely** in favour of focusing on the backend deep-research + simulation pipeline.

## What the frontend was

A review loop where a human could:
- See the pipeline-generated ground truth and edit it
- See the generated SITREP and edit it
- Trigger the forecasting stages against the edited ground truth
- Browse prior session reports

Persisted in `data/geopol.db` (SQLite via `better-sqlite3`).

## Why deferred

The core goal is producing a high-quality PDF forecast report. The review UI is useful but not on the critical path. Building it alongside a backend rewrite doubles the work and blocks progress on the more interesting problem (deep research + actor simulation).

## What to preserve during the rewrite

- **File layout contract.** The backend writes to `reports/<ts>/` with the exact same file names the frontend expects:
  - `00-news-headlines.md`
  - `00-isw-analysis.md`
  - `01-ground-truth.md`
  - `02-sitrep.json`
  - `03-forecasts.json`
  - `04-summary.json`
  - `report.typ`
  - `report.pdf`
- **Schemas.** Python `pydantic` models should mirror the Zod schemas in `src/lib/schemas.ts` so a future frontend can deserialize the same JSON without translation.
- **Session IDs.** Keep the UUID + ISO timestamp pattern.

## What a future frontend would need to add

- A new "simulation trace" view (if the hybrid pipeline from `03-hybrid-implementation.md` ships). Stage A output is structurally interesting — turn-by-turn actor actions, per-run trajectories, empirical probability tables.
- Ability to edit actor personas (the highest-leverage configuration in the whole system).
- Monte Carlo controls (N runs, temperature, timestep count).
- Comparison view: research-based vs simulation-based predictions side by side.

## When to revisit

After the backend produces a forecast Daniel trusts end-to-end on a real question (the Iran-Israel ceasefire forecast is the first test). If the output is good, a frontend is worth building. If the output needs tuning, iterate on the backend first.
