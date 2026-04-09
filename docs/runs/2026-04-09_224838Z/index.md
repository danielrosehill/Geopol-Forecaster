---
layout: default
title: "Run 2026-04-09_224838Z — Iran–Israel–US Ceasefire"
---

# Run 2026-04-09_224838Z

**Question.** Iran, Israel, and the US just announced a two-week ceasefire
on April 8, 2026. Will it hold at +24h, +72h, +1 week, +1 month, and how
does the conflict evolve from here?

**Run date.** 2026-04-10
**Model.** `anthropic/claude-sonnet-4.5` via OpenRouter
**Stage A:** 38 actors × 4 timesteps × 1 MC run
**Stage B:** 6 council lenses, 2-stage protocol, chairman synthesis
**Grounding:** Tavily (4 queries) + RSS/ISW, frozen to Turn-0 world state

---

## Headline forecast

| Window | P(ceasefire holds) | 90% credible range |
|---|---|---|
| +24 hours | 55% | 42–68% |
| +72 hours | 22% | 15–32% |
| +1 week   | 10% | 6–16% |
| +1 month  | 4%  | 2–8% |

Council verdict: **will not survive beyond 72 hours**. The Lebanon scope
ambiguity is treated as a weaponised structural fault line, not a drafting
error. Full reasoning in the artifacts below.

---

## Artifacts

| File | Description | Size |
|---|---|---|
| [Chairman report](chairman_report) | Final synthesised forecast with probabilities, scenarios, and indicators | 23 KB |
| [Stage 1 — 6 lens answers](stage1_answers) | Independent first-round responses from the six council lenses | 221 KB |
| [Stage 2 — cross-reviews](stage2_reviews) | Lenses reviewing each other's reasoning | 94 KB |
| [Experiment notes](experiment_notes) | Design, roster, cost, runtime, known issues | — |
| [Rendered PDF](report_v2.pdf) | Typst-compiled chairman report | 62 KB |

Raw Stage A simulation (`simulation.json`, 744 KB) and fresh-data bundle
(`fresh_data.json`, 75 KB) are in the source repository under
`reports/2026-04-09_224838Z/`.

---

## Stage A — actor roster

38 actors briefed as personas with red lines, typical response patterns,
and institutional constraints. Grouped here for quick navigation:

**Iran — leadership & security state**
Khamenei · IRGC (collective) · IRGC Aerospace Force · IRGC Intelligence
Organization · Quds Force · MOIS · Artesh

**Iran — domestic society**
Organised dissidents · Quiet dissenting majority · Diaspora (general) ·
Pro-Pahlavi inside Iran · Pro-Pahlavi diaspora

**Israel — leadership & security state**
Netanyahu · Cabinet collective · IDF General Staff · Mossad · Shin Bet ·
Aman · Israeli IC collective

**United States**
Trump · CENTCOM · Executive branch collective · US Intelligence Community ·
Political opposition

**Lebanon & proxies**
Government of Lebanon · LAF · Hezbollah SG · Houthi leadership

**Regional mediators & powers**
MBS · Erdoğan · Qatar mediation track · Pakistan mediator

**Europe**
EU collective · Ireland · Germany

**Global powers**
Russia · China · North Korea

**Multilateral**
UN Secretariat · UNTSO

---

## Stage B — council lenses

Six analytical lenses run in parallel, then cross-review. See
[Stage 1 answers](stage1_answers) for the independent reasoning and
[Stage 2 reviews](stage2_reviews) for the mutual critique.

---

## Known issues with this run

See [experiment notes](experiment_notes) for full details. Summary:

- Original Typst render crashed on `<N` literals parsed as label openers.
  A simpler `report_v2.typ` template was written post-hoc using pandoc's
  Typst writer — that's the PDF linked above.
- Pipeline exception handling only caught `TypstNotInstalled`; a render
  failure bubbled up and killed the session banner. Fix queued.
- Stage A runs silently for ~10 minutes; per-turn progress logging would
  help long runs feel less opaque.
