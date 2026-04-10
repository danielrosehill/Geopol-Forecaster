# Self-Correcting Loop

Use when the user wants to review the last pipeline run and autonomously improve the system based on what the report reveals. Triggers on phrases like "self-correct", "improve from last run", "feedback loop", "correct the pipeline", "learn from last report".

## Procedure

You are an autonomous self-improvement agent for the Geopol-Forecaster pipeline. Your job is to read the most recent report, diagnose weaknesses in how the pipeline *functioned*, and apply targeted code fixes.

### Step 1 — Find the latest run

List directories under `reports/` sorted by name (they are timestamped). Pick the most recent one. Read these files from it:
- `chairman_report.md` (the final deliverable)
- `fresh_data.json` (the grounding data the pipeline had access to)
- `simulation.json` (the actor simulation trace)
- `stage1_answers.md` (the 6 lens answers)
- `stage2_reviews.md` (the blind peer reviews)
- `experiment_notes.md` (if present)

### Step 2 — Diagnose pipeline weaknesses

Analyse the report *as a report consumer* and identify gaps that trace back to how the pipeline operated, NOT to the geopolitical situation itself. Focus on these categories:

1. **Grounding gaps** — Did the fresh data actually cover the topics the council needed? Were Tavily queries too narrow or too generic? Were RSS keywords missing relevant terms? Did citations feel stale or irrelevant?
2. **Simulation fidelity** — Did actors produce generic boilerplate instead of sharp, persona-specific actions? Did the referee narration lose coherence across turns? Were red lines actually invoked or just listed?
3. **Council quality** — Did lenses produce meaningfully different forecasts or did they converge into hedge-speak? Did peer reviews add value or just restate? Did the chairman report have concrete predictions with probabilities, or vague hedging?
4. **Prompt engineering** — Are system prompts leaving too much room for generic output? Are they specific enough about output format? Are temperature settings appropriate?
5. **Data flow** — Was information lost between stages? Was the simulation summary too compressed for the council to use? Was the fresh data bundle too large or too small?

For each gap found, write a diagnosis with:
- **What went wrong** (quote the report where possible)
- **Root cause in pipeline code** (name the file, function, and line)
- **Proposed fix** (specific code change)

### Step 3 — Apply fixes autonomously

For each diagnosed gap, apply the fix directly to the pipeline code. The key files you may need to modify:

- `geopol/news/tavily.py` — Query derivation, search parameters, result processing
- `geopol/news/rss.py` — RSS feeds, keyword filters, age cutoffs, ISW fetching
- `geopol/news/fresh_data.py` — Data aggregation and bundling
- `geopol/simulation/engine.py` — Actor turn prompts, referee narration, summarisation
- `geopol/actors/roster.py` — Actor persona definitions, red lines, constraints
- `geopol/council/protocol.py` — Lens prompts, review prompts, chairman synthesis prompt
- `geopol/council/lenses.py` — Lens definitions and directives
- `geopol/config.py` — Model routing, simulation parameters
- `geopol/base_context.py` — Static background context
- `geopol/schemas.py` — Data models (only if new fields are needed)

**Rules:**
- Do NOT change the overall pipeline architecture (Stage 0 -> A -> B -> Render)
- Do NOT add new dependencies without asking
- Do NOT change model routing (all via OpenRouter) without asking
- DO improve prompts, query strategies, keyword lists, temperature values, truncation limits
- DO add missing actors or refine existing persona briefs if the simulation was weak
- DO tighten output format instructions if LLM responses were sloppy
- DO adjust Tavily search parameters or add query variants if grounding was poor

### Step 4 — Document changes

After applying fixes, create `reports/SELF_CORRECTION_LOG.md` (append if it already exists) with a dated entry:

```markdown
## YYYY-MM-DD — Self-correction from run <run_timestamp>

### Gaps diagnosed
- [list each gap with category]

### Fixes applied
- [file:line] — [what changed and why]

### Expected improvement
- [what should be better in the next run]
```

### Step 5 — Verify

Run a quick smoke test if available (`uv run geopol smoketest`) to ensure the changes don't break imports or basic execution flow. If the smoketest doesn't exist or fails on API calls (expected without live keys), at least verify the Python package imports cleanly with `uv run python -c "import geopol"`.
