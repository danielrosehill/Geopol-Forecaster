# 01 — Current Approach

*Snapshot of the pipeline as it exists on `main` at 2026-04-10, before any rewrite.*

## Stack

- **Runtime:** TypeScript / Node, Next.js 16 frontend + `scripts/run-pipeline.ts` CLI
- **LLM routing:** Vercel `ai` SDK → OpenRouter for Grok & Gemini-via-OR; `@google/genai` direct for Gemini search grounding
- **Grounding:** Gemini 3.1 Flash Lite with `googleSearch` tool (the **only** live-web touchpoint)
- **Structured output:** Zod schemas via `Output.object()`
- **Persistence:** SQLite (`data/geopol.db`) for frontend review state; per-run markdown/JSON files in `reports/<ts>/`
- **Rendering:** Typst template (`src/lib/typst-template.ts`, 859 lines) → `typst compile` → PDF

## Pipeline (6 stages, linear with some parallelism)

### Stage 0 — News ingestion (`src/lib/rss.ts`)
- Times of Israel RSS + Jerusalem Post RSS → keyword-filtered, age-filtered (48h), deduped headlines
- ISW/CTP WordPress API → up to 3 full Iran Update articles (~15k chars each)
- Output: `00-news-headlines.md`, `00-isw-analysis.md`

### Stage 1 — Intelligence gathering
Runs two grounding calls in parallel:
- **Feed A:** Gemini 3.1 Flash Lite with `googleSearch` tool — system prompt asks for past 3h/6h/12h/24h windows
- **Feed B:** Grok 4.1 Fast via OpenRouter — implicit X/social grounding

Then a **merge agent** (Grok via OR) consolidates Feed A + Feed B + Feed C (news context) into a single "Ground Truth" document. Prompt explicitly tells it to prioritise Feed C (sourced journalism) over A/B.
- Output: `01-ground-truth.md`

### Stage 2 — SITREP
One Gemini call (via OR) transforms ground truth into structured 14-section SITREP JSON modeled on ISW/CTP format. Sections: `key_takeaways`, `coalition_ops`, `iranian_ops`, `strikes`, `northern_front`, `gulf_states`, `military_technical`, `trajectory`, `us_statements`, `israel_statements`, `home_front`, `world_reaction`, `osint_indicators`, `outlook`.
- Output: `02-sitrep.json`

### Stage 3 — Six-lens forecasting (parallel)
Six parallel `generateText` calls with `Output.object(LensForecastSchema)`. Models alternate Gemini / Grok. Each lens has a distinct directive:

| Lens | Directive |
|---|---|
| **Neutral** | Honest unbiased assessment |
| **Pessimistic** | Worst-case escalation paths |
| **Optimistic** | De-escalation and restraint |
| **Blindsides** | Low-probability black swans |
| **Probabilistic** | Explicit probability ranges, historical precedent |
| **Historical** | Pure historical-analogy reasoning |

Each lens produces 4 timeframes (`24h`, `1w`, `1m`, `1y`), each with overview + 2–6 predictions (prediction, probability, confidence, reasoning) + keyRisks + indicators.
- Output: `03-forecasts.json`

### Stage 4 — Executive summary
One Grok call (structured, `SummarySchema`) synthesises all six lens outputs into: `overallAssessment`, `consensusThemes`, `highConfidencePredictions` (with lens-agreement counts), `keyDivergences`, `criticalUncertainties`, `actionableInsights`.
- Output: `04-summary.json`

### Stage 5 — PDF render
Markdown→Typst conversion (custom, in `typst-template.ts`) + structured forecasts/summary rendered directly as Typst tables and callout boxes. Cover page + TOC + Exec Summary + SITREP + Ground Truth + Forecasts-by-timeframe + Forecasts-by-lens appendix + Run Analysis.
- Output: `report.typ`, `report.pdf`

## Known weaknesses

1. **Single point of failure on grounding.** Gemini googleSearch is the only live-web source. If it returns empty or flakes, the entire pipeline runs on Grok + stale RSS. `response.text ?? ""` silently swallows failures.
2. **No retries, no verification.** No cross-check pass that validates ground truth claims against the raw feeds. LLM hallucinations propagate.
3. **Static lens prompts.** The six lenses are clever but they're all *single-shot inference* over the same ground truth. No iteration, no tool use, no interaction between lenses during generation.
4. **Model ID duplication.** `gemini-3.1-flash-lite-preview` hardcoded in 3 places; a preview model is load-bearing infrastructure.
5. **Frontend coupling.** SQLite + Next.js review UI is half-built and not essential for the core forecasting goal. Deferred — see `DEFERRED-FRONTEND-REFACTOR.md`.
6. **No methodological diversity in the forecast itself.** Every prediction comes from the same mechanism: "LLM reads ground truth, LLM writes forecast." There is no simulation, no historical base-rate lookup, no adversarial red-teaming, no empirical probability from repeated runs.

## What the pipeline does well

- Clean separation of stages with file-per-stage output (easy to inspect, resume, re-run)
- Structured outputs (Zod) throughout — no regex-parsing LLM markdown
- Parallel lens forecasts
- Typst rendering is genuinely high-quality (IBM Plex, callout boxes, cross-lens timeframe tables)
- Base context + ISW priority in merge prompt is a real differentiator vs generic "ask an LLM"
- Six-lens framing forces the model to produce genuinely different outputs rather than one averaged take
