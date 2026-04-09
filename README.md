![Geopol Forecaster](docs/assets/banner.png)

# Geopol Forecaster

Two-stage geopolitical forecasting experiment:

1. **Stage A — actor simulation.** Referee + per-actor `Player` loop over ~10
   decision-makers (Khamenei, Netanyahu, Trump, IRGC, Hezbollah, Houthis, MbS,
   Erdoğan, Qatari mediator, CENTCOM). Pattern borrowed from IQTLabs'
   [snowglobe](https://github.com/IQTLabs/snowglobe) (`examples/ac_sim.py`).
2. **Stage B — lens council.** 6 lens directives deliberate via
   karpathy's [llm-council](https://github.com/karpathy/llm-council) 3-stage
   protocol (parallel query → blind peer review → chairman synthesis) with a
   frozen bundle of base context + Tavily/RSS/ISW fresh data + Stage A's
   simulation summary. The chairman writes the final report directly.

Output: markdown + Typst-rendered PDF in `reports/<timestamp>/`. No frontend.

See `docs/UPSTREAM-COMPONENTS.md` for how we use each upstream and what we
changed.

## Status

The TypeScript/Next.js prototype lives in `src/` and is frozen — it's kept
only as reference material while the Python port reaches parity and will be
deleted afterwards.

## Running

```bash
uv sync
cp .env.example .env     # fill in OPENROUTER_API_KEY and TAVILY_API_KEY
uv run geopol smoketest
uv run geopol forecast "Will the Iran-Israel ceasefire hold through Q3 2026?"
```

Outputs land in `reports/<UTC timestamp>/`:

- `chairman_report.md` — final report (also rendered to PDF)
- `report.pdf` — Typst-rendered PDF (requires `typst` on PATH)
- `report.typ` — Typst source
- `fresh_data.json` — frozen Tavily + RSS/ISW bundle
- `simulation.json` — all Stage A runs + summary
- `stage1_answers.md`, `stage2_reviews.md` — council trace

## Layout

```
geopol/
  config.py          Models, MC runs, paths. One constant per role.
  llm.py             OpenRouter async client. Single key, single router.
  base_context.py    Static conflict background (ported from src/lib/base-context.ts).
  schemas.py         Pydantic schemas (ported from src/lib/schemas.ts, extended).
  news/
    rss.py           Times of Israel + JPost RSS, ISW WordPress API.
    tavily.py        Tavily grounded-answer client.
    fresh_data.py    Single context-gathering agent → frozen FreshData bundle.
  actors/
    roster.py        ~10 persona briefs for the simulation.
  simulation/
    engine.py        Stage A. Control/Player loop + summariser.
  council/
    lenses.py        The 6 lens directives (neutral/pessimistic/…/historical).
    protocol.py      Stage B. 3-stage llm-council protocol, lens-flavoured.
  render/
    typst.py         Markdown → Typst source.
    pdf.py           Shell out to the typst CLI.
  pipeline.py        End-to-end orchestrator.
  cli.py             `geopol forecast` / `geopol smoketest`.
```

## Locked decisions

- Language: Python, `uv` + `pyproject.toml`.
- All LLM calls via OpenRouter. Single `OPENROUTER_API_KEY`. No provider SDKs.
- Grounding: Tavily only. No `gpt-researcher`, no Gemini `googleSearch`.
- Output: markdown + Typst PDF in `reports/`. No frontend, no SQLite.
- First run: Sonnet 4.6 everywhere, Monte Carlo N=1, 4 timesteps, all 6 lenses.

See the sibling
[`Geopol-Forecaster-Planning`](../Geopol-Forecaster-Planning) repo for the
full architectural rationale.
