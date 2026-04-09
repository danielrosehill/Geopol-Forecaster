# Experiment Notes — Run 2026-04-09_224838Z

## Question

Iran–Israel–US ceasefire durability, assessed at +24h / +72h / +1 week / +1 month,
with forecast of conflict evolution. Full seeded prompt in
`prompts/2026-04-10_iran-israel-us-ceasefire.md`.

## Design

**Two-stage pipeline.** Stage A is an actor-level Monte Carlo simulation
(snowglobe-style control/player loop). Stage B is a council lens panel
(llm-council-style multi-perspective review and chairman synthesis).

### Stage A — actor simulation

- **Roster:** 38 actors covering principals (Iran/Israel/US leadership), Iranian
  internal factions (IRGC collective, IRGC-ASF, IRGC-IO, Quds Force, MOIS,
  Artesh, dissidents, quiet dissenting majority, two pro-Pahlavi constituencies
  inside/outside Iran, general diaspora), Israeli security architecture (cabinet,
  IDF General Staff, Mossad, Shin Bet, Aman, collective IC), US apparatus
  (Trump, CENTCOM, executive collective, IC, opposition), Lebanon (government,
  LAF, Hezbollah), axis/proxy (Houthis), regional mediators and powers
  (MBS, Erdoğan, Qatar, Pakistan), Europe (EU collective, Ireland, Germany),
  global powers (Russia, China, DPRK), and multilateral (UN, UNTSO).
- **Timesteps:** 4 (`now`, `+24h`, `+1 week`, `+1 month`).
- **Monte Carlo runs:** 1 (N=1 — cost control for first seeded run).
- **Referee:** single-narrator model authoring world state between turns,
  enforcing authority-precedence conflict resolution, ≤300 words prose plus
  structured `ACTIVE_ACTORS / RECENT_EVENTS / OPEN_TENSIONS` block.
- **Information hygiene:** actors see only the referee-authored world state
  and their own private memory. No direct news access, no other actors'
  private assessments.
- **Temperature:** 0.8 for actors, 0.4 for referee.

### Stage B — 6-lens council

- 6 parallel lens members (see `stage1_answers.md`), 2-stage protocol
  (stage 1 independent answers → stage 2 cross-review), chairman synthesis.
- Council sees the seeded prompt, the fresh-data bundle, and the Stage A
  simulation summary — not the full per-turn transcripts.

### Grounding

- **Tavily** search grounding (4 derived queries) — see
  `fresh_data.json / tavily_*` fields and `prompts/...md` context block.
- **RSS/ISW** news ingestion for the last 48 hours (see
  `fresh_data.rss_brief` / `fresh_data.isw_brief`).
- Both are frozen into the Turn-0 world state and passed identically to every
  actor and every council lens — no per-actor re-searching, which would
  introduce inconsistent world-states and fragment the sim.

### Models

- All calls route through OpenRouter to `anthropic/claude-sonnet-4.5`.
  Single model for first seeded run; per-role overrides are wired in
  `config.py` for later diversification (council lenses are the obvious
  candidate for mixed providers to get genuine perspective divergence).

## Cost / runtime (observed)

- **Total wall clock:** ≈18 minutes (Stage A dominated).
- **Stage A:** ~10 minutes — 38 parallel actors × 4 sequential timesteps, plus
  4 referee calls. Timestep parallelism is bounded by the slowest actor call
  per step; 38-way fan-out put some pressure on OpenRouter throughput without
  surfacing 429s.
- **Stage B:** ~3 minutes — 6 parallel lenses × 2 stages + chairman.
- **PDF render:** failed — Typst compile errored on `unclosed label` /
  `unclosed delimiter` because the chairman output contains `<10 vessels/day`
  and similar `<N` literals that Typst parses as label openers. The pipeline's
  try/except only catches `TypstNotInstalled`, so `CalledProcessError` bubbled
  up and failed the run after all LLM work was complete. Artifacts were
  already written to disk — nothing lost.
- **OpenRouter cost:** not yet reconciled against the provider dashboard.
  Back-of-envelope at $3 in / $15 out per million tokens for Sonnet 4.5
  puts this run in the **$6–12** range, driven principally by Stage A's
  152 actor calls.

## What the prompt was seeded with

Live Tavily news search on 2026-04-10 pulled the April-8 ceasefire framing
(two-week term, Strait-of-Hormuz commitment, Pakistan/France/Egypt mediation),
the Lebanon-scope dispute (Araghchi vs. Netanyahu/Trump), the enrichment
"10-point plan" Farsi-version controversy, early ambiguous violations (refinery
claim, UAE/Kuwait attacks, Hezbollah pause with Moussawi warning), and the
Khademi (IRGC-IO chief) killing. This was baked into the prompt itself as a
failsafe against model-internal staleness — the council did not have to trust
its own training-data recall of the preceding six weeks.

## Artifacts in this directory

| File | What it is |
|---|---|
| `fresh_data.json` | Tavily + RSS/ISW seed, frozen |
| `simulation.json` | Full Stage A: 38 actors × 4 turns × N=1 run, with referee narrations |
| `stage1_answers.md` | 6 council lenses, independent first-round answers |
| `stage2_reviews.md` | Cross-reviews between lenses |
| `chairman_report.md` | Final synthesised chairman report |
| `report.typ` | **Broken** Typst source from original pipeline (unclosed-label errors) |
| `report.pdf` | (to be regenerated with fixed Typst script) |
| `experiment_notes.md` | This file |

## Known issues to fix in the pipeline

1. **Typst escaping.** `render/typst.py` must escape `<`, `>`, `@`, and `#` in
   body text so `<10`, `<30%`, `<email@domain>`, and `#hashtag` don't get
   parsed as Typst markup. Most minimal fix: replace unescaped `<` → `\<` and
   `>` → `\>` in converted body content (outside code fences).
2. **Exception swallowing.** `pipeline.py:74` catches `TypstNotInstalled` only.
   Broaden to `(TypstNotInstalled, subprocess.CalledProcessError)` so a
   render failure prints a warning and still emits session paths instead of
   discarding the exit banner.
3. **Cost controls.** Add per-run cost estimate printed before Stage A so
   expensive roster/timestep combinations are visible before burn.
4. **Per-actor progress logging.** Stage A runs silently for 10 minutes. A
   `[stage A] turn k/4 — 38 actors, xxxs` line per turn would make the long
   wait intelligible.
