# Run and Publish Forecast

End-to-end skill: run a geopolitical forecast from a user prompt, then create a public repo with the results and register it in the index. Triggers on phrases like "run a forecast", "new prediction", "forecast and publish", "run simulation and publish", "predict and open-source".

## When to use

- User provides a geopolitical question and wants a full pipeline run followed by automatic open-sourcing
- User says "run a forecast about …", "predict …", "new prediction run on …"

## Inputs

1. **Forecast question** — the user's prompt (e.g. "Will the Iran-Israel ceasefire hold through Q3 2026?")
2. **Topic slug** (optional) — short name for the output repo. If not provided, derive one from the question in `{Topic}-Prediction-{DDMMYY}` Title-Case format using today's date.

## Phase 1 — Run the pipeline

1. `cd ~/repos/github/my-repos/Geopol-Forecaster`
2. Run the full pipeline:
   ```bash
   uv run geopol forecast "<question>"
   ```
3. Wait for completion. Capture the output — it will print the session ID and report directory path.
4. Verify the run produced the expected artifacts in `reports/<timestamp>/`:
   - `chairman_report.md`
   - `simulation.json`
   - `stage1_answers.md`
   - `stage2_reviews.md`
   - `fresh_data.json`
5. Show the user a brief summary of the headline forecast and key findings from the chairman report before proceeding.

**If the pipeline fails:** Read the error, diagnose, and report to the user. Do NOT proceed to Phase 2.

## Phase 2 — Create the public repo

Follow the full procedure from the `new-geopol-forecast-repo` skill (at `~/.claude/skills/new-geopol-forecast-repo/SKILL.md`). In summary:

1. **Derive the topic slug** from the question if not provided. Convention: `{Topic}-Prediction-{DDMMYY}`, Title-Case-With-Hyphens, using today's date.
2. **Create repo directory** at `~/repos/github/my-repos/{Topic}-Prediction-{DDMMYY}/`.
3. **Copy report artifacts** into `report/`:
   - `chairman_report.md`, `experiment_notes.md` (if present), `stage1_answers.md`, `stage2_reviews.md`
   - Find the matching prompt and copy as `report/prompt.md`
4. **Copy code snapshot** — entire `geopol/` package + `pyproject.toml` into `code_snapshot/`. Remove `__pycache__/`.
5. **Extract probability data** from chairman report and stage1 answers.
6. **Generate `generate_graphics.py`** with the extracted data. Run it to produce 4 matplotlib charts (dark theme `#0d1117`):
   - `convergence_all_lenses.png` — all lens probability curves + chairman + simulation
   - `chairman_forecast.png` — bar chart with 90% credible intervals
   - `key_predictions.png` — horizontal bar chart of top predictions
   - `72h_convergence.png` — per-lens spread at critical window
7. **Write README.md** following the template from the `new-geopol-forecast-repo` skill:
   - Headline forecast with chairman chart
   - Stack credits (Snowglobe + LLM Council)
   - Experiment design
   - Simulation-council convergence
   - Key predictions chart
   - Key findings (4-6 bullets)
   - Repository contents tree
   - Link to full source, author, CC BY 4.0 license
8. **Git init, commit, create public GitHub repo, push.**

## Phase 3 — Register in Geopol-Forecasts-Index

1. Open `~/repos/github/my-repos/Geopol-Forecasts-Index/README.md`.
2. Add a new row to the **Prediction Runs** table. Increment the run number. Use the format:
   ```
   | # | DD/MM/YYYY | Topic | 38 | 6 | Claude Sonnet 4.5 | [Repo-Name](https://github.com/danielrosehill/Repo-Name) | Key finding summary |
   ```
3. Add a new **Accuracy Tracking** section for the run with an initial "Not Yet Testable" entry for the headline prediction.
4. Commit and push the index repo.

## Phase 4 — Report to user

Print:
- The GitHub URL of the new public repo
- The headline forecast and key finding
- Confirmation that the index was updated
- Offer to also register in AI-Geopol-Projects or subindices

## Conventions

- **Repo naming**: `{Topic}-Prediction-{DDMMYY}`, Title-Case-With-Hyphens
- **Date format**: DD/MM/YYYY in prose, DDMMYY in repo name
- **Always public** repos
- **Code snapshot is frozen** — note in README and link to parent repo
- **CC BY 4.0** license
- **Run number** in the index is auto-incremented from the last entry
