# Self-Correction Log

## 2026-04-10 — Self-correction from run 2026-04-09_224838Z

### Gaps diagnosed

1. **Grounding: Tavily queries too static** — 2 of 4 queries were hardcoded Iran/Israel strings that missed Russia/nuclear and Hormuz angles the chairman report needed
2. **Data flow: Tavily snippet truncation too aggressive** — 400-char snippets lost analytical depth, forcing reliance on ISW/RSS alone
3. **Data flow: RSS HTML tags leaking** — RSS article descriptions contained raw `<p>` and `<a>` tags in the fresh_data bundle
4. **Simulation fidelity: Referee narration word limit too tight** — 300 words for 38 actors = ~8 words per actor, forcing generic compression
5. **Data flow: Simulation trace truncation** — 18k char cap on trace summary lost nuance with 38 actors x 4 timesteps
6. **Council quality: Chairman max_tokens too low** — 6000 token cap risked truncating the detailed final report
7. **Prompt engineering: Council horizons mismatched simulation** — Council asked for 24h/1w/1m/1y but simulation ran now/+24h/+1w/+1m; "1 year" had zero simulation support
8. **Experiment design: 38 actors too many** — Many actors produced generic output; reduced to 10 core decision-makers for sharper simulation
9. **Experiment design: 4 timesteps misaligned** — Changed from now/+24h/+1w/+1m to +24h/+72h/+2w to focus on the critical near-term window

### Fixes applied

- `geopol/news/tavily.py:37` — Doubled snippet length from 400 to 800 chars
- `geopol/news/tavily.py:64-69` — Added 2 new Tavily queries (Russia/China/nuclear, Hormuz shipping) and made diplomacy query more specific (6 queries total)
- `geopol/news/rss.py:52-55` — Added `_strip_html()` helper to clean HTML tags from RSS descriptions
- `geopol/news/rss.py:78-79` — Applied HTML stripping to RSS title and description fields
- `geopol/simulation/engine.py:116` — Raised referee narration limit from 300 to 500 words
- `geopol/simulation/engine.py:203` — Raised trace summary cap from 18k to 30k chars
- `geopol/simulation/engine.py` — Changed default roster from ROSTER (40) to ROSTER_CORE (10)
- `geopol/actors/roster.py:904-910` — Added ROSTER_CORE: 10-actor curated subset (khamenei, netanyahu, trump, irgc, hezbollah, centcom, mossad, idf, russia, mbs)
- `geopol/council/protocol.py:67` — Changed council horizons from 24h/1w/1m/1y to 24h/72h/2w
- `geopol/council/protocol.py:160` — Changed chairman report horizons to match
- `geopol/council/protocol.py:186` — Raised chairman max_tokens from 6000 to 12000
- `geopol/config.py:34-35` — Changed SIM_TIMESTEPS from 4 to 3, TIMESTEP_LABELS to ["+24h", "+72h", "+2 weeks"]

### Expected improvement

- **Better grounding** — 6 Tavily queries covering diplomacy, nuclear, and Hormuz angles should catch the kind of signals (Russian evacuation coordination) that Run 2 only got from ISW
- **Cleaner data** — No more HTML tags in RSS feed data; longer Tavily snippets carry more analytical weight
- **Sharper simulation** — 10 actors instead of 40 means each actor gets more referee attention per turn; 500-word narrations and 30k trace cap preserve more nuance
- **Aligned horizons** — Council and simulation now share the same 24h/72h/2w windows, eliminating the unsupported "1 year" horizon
- **Richer chairman output** — 12k token cap gives the chairman room for the kind of detailed report Run 2 produced
