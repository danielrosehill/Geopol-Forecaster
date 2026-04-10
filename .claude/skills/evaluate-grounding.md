# Evaluate Grounding

Use when the user wants to review, audit, or improve the news ingestion and grounding mechanism used by the pipeline. Triggers on phrases like "evaluate grounding", "review news ingestion", "improve data sources", "grounding audit", "news quality", "tavily review", "rss audit".

## Procedure

You are a grounding-quality auditor for the Geopol-Forecaster pipeline. Your job is to investigate the current news ingestion and search grounding mechanisms, present a clear summary to the user, propose improvements, and — once agreed — implement them.

### Step 1 — Investigate the current grounding stack

Read and understand these files thoroughly:

**Data sources:**
- `geopol/news/tavily.py` — Tavily API search client, query derivation logic, result parsing
- `geopol/news/rss.py` — RSS feed list, keyword filter, ISW WordPress API fetcher, age cutoff
- `geopol/news/fresh_data.py` — Aggregator that bundles Tavily + RSS into a single FreshData object

**How grounding is consumed:**
- `geopol/schemas.py` — FreshData model and its `as_markdown()` serialisation
- `geopol/pipeline.py` — How fresh data flows into Stage A (news_seed) and Stage B (full bundle)
- `geopol/simulation/engine.py` — How the simulation uses the news seed (truncated to 8000 chars)
- `geopol/council/protocol.py` — How the council receives and references fresh data

**Configuration:**
- `geopol/config.py` — API keys, any grounding-related settings

**Evidence from recent runs:**
- Read `reports/<latest>/fresh_data.json` to see what data the last run actually collected
- Read `reports/<latest>/chairman_report.md` to see how (or whether) grounding data was actually cited

### Step 2 — Present findings to the user

Summarise the current grounding mechanism clearly, covering:

1. **Data sources inventory**
   - Tavily: how queries are derived, search depth, max results, topic filter
   - RSS: which feeds, keyword filter list, age cutoff
   - ISW: WordPress API parameters, post limit
   - What's missing (e.g., no social media, no government press releases, no wire services, no structured event databases)

2. **Query derivation quality**
   - How the forecast question maps to Tavily queries (the `derive_queries()` function)
   - Whether queries are too hardcoded (2 of 4 queries are static Iran/Israel strings)
   - Whether the LLM could generate better, more targeted queries

3. **Data freshness and coverage**
   - RSS age cutoff (currently 48h)
   - Whether ISW posts are timely enough
   - Whether Tavily's "news" topic filter is appropriate
   - Citation quality from the last run

4. **Information loss in the pipeline**
   - Tavily snippet truncation (400 chars per citation)
   - News seed truncation for simulation (8000 chars)
   - Whether FreshData.as_markdown() preserves enough signal

5. **Grounding verification**
   - Whether the council actually cites fresh data in predictions
   - Whether the chairman report's "supported_by" column is meaningful
   - Whether the peer review stage checks grounding quality

### Step 3 — Propose improvements

Based on the investigation, propose concrete improvements ranked by impact. Possible categories:

- **Query expansion** — Use LLM to generate Tavily queries instead of heuristic; add follow-up queries based on initial results
- **Source diversification** — Add RSS feeds (Al Jazeera, Reuters, BBC Middle East, Haaretz); add government press release sources; add OSINT feeds
- **Keyword expansion** — Update the keyword filter to cover more relevant terms
- **Search parameters** — Adjust Tavily depth, result count, topic filter
- **Data preservation** — Increase snippet length, reduce truncation, add full-text retrieval for key sources
- **Freshness** — Tighten age cutoffs, add staleness warnings, timestamp-aware prioritisation
- **Verification loop** — Add a post-council step that checks whether predictions are actually grounded in cited data
- **Multi-pass search** — After Stage A simulation, do a second Tavily search targeting the simulation's flags_for_council

Present these to the user and wait for their input on which to implement.

### Step 4 — Implement agreed changes

Once the user agrees on which improvements to pursue, implement them in the relevant files. Follow the same rules as the self-correcting loop:

- Do NOT change the overall pipeline architecture
- Do NOT add new dependencies without confirmation
- DO improve query derivation, add feeds, expand keywords, adjust parameters
- DO add new data source fetchers if agreed upon
- Ensure all changes are backward-compatible (pipeline should still work if a new source is unreachable)

### Step 5 — Verify

After implementing changes, verify:
1. `uv run python -c "import geopol"` — package imports cleanly
2. If possible, do a dry-run of `gather_fresh_data()` to confirm new sources work
3. Show the user a diff of all changes for final review
