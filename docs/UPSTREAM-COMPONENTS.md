# Upstream Components

Two existing open-source projects are the load-bearing inspirations for this
refactor. Neither is reimplemented from scratch; we adopt their protocols and
either vendor or lightly-wrap their code.

## 1. IQTLabs / snowglobe (Stage A — actor simulation)

- **Repo:** https://github.com/IQTLabs/snowglobe
- **PyPI:** `llm-snowglobe`
- **License:** Apache 2.0
- **Role in this project:** Stage A. Actor simulation of key decision-makers
  (Khamenei, Netanyahu, Trump, IRGC, Hezbollah, Houthis, MbS, Erdoğan, Qatari
  mediator, CENTCOM) with a referee that narrates the resulting world state
  each turn.

### What we take from it

- The **architectural pattern**: a `Control` (referee) orchestrates a list of
  `Player`s (actors), each with a persona system prompt, across N turns. After
  all players commit an action, the control narrates the consequences and
  updates shared state. This is exactly what we need for sealed-off
  actor-attributed reasoning.
- The **reference implementation** in `examples/ac_sim.py`
  (`AzuristanCrimsonia`): a two-actor geopolitical game with move loops,
  Monte Carlo assessment questions, and narrated adjudication.
- The **`geopol` mode** in `Control.adjudicate` — a phrasing flag that frames
  adjudication as "leaders issuing orders" rather than generic planning.

### What we changed / why

- We do **not** run the full llm-snowglobe stack (which pulls torch,
  transformers, langchain, llama-cpp-python) for the first pass. Instead,
  `geopol/simulation/engine.py` implements the same Control/Player loop
  directly against our OpenRouter client. This keeps the dependency surface
  small and guarantees every LLM call routes through the project's single
  key/router. `llm-snowglobe` is still listed in `pyproject.toml` so we can
  swap to the real classes (`snowglobe.Control`, `snowglobe.Player`) later
  without rewriting the pipeline boundary.
- We enforce stricter world-state sealing than `ac_sim.py`: actors see **only**
  the referee-authored world state, never raw news, never Tavily, never other
  actors' private memory. This prevents the sim from collapsing into
  "inference over the news feed."
- Referee prompt forbids inventing consequences that do not follow directly
  from the actions each player committed this turn.

### Reference files

- `examples/ac_sim.py` — the canonical minimal example we pattern-matched on.
- `src/llm_snowglobe/core/control.py` — the Control class.
- `src/llm_snowglobe/core/player.py` — the Player class and `respond()` method.

---

## 2. karpathy / llm-council (Stage B — lens panel & synthesis)

- **Repo:** https://github.com/karpathy/llm-council
- **License:** (upstream repo license)
- **Role in this project:** Stage B. A 3-stage deliberative protocol across
  our 6 lens directives, culminating in a chairman-written final report.

### What we take from it

- The **3-stage protocol** from `backend/council.py`:
  1. `stage1_collect_responses` — parallel queries to every member.
  2. `stage2_collect_rankings` — each member blind-reviews the anonymised
     answers of the others, ending with a FINAL RANKING block.
  3. `stage3_synthesize_final` — a chairman model reads every answer plus
     every peer review and writes the final synthesis.
- The **anonymisation scheme** (`Response A`, `Response B`, …) and the
  `label_to_model` mapping. We port this so peer review stays honestly blind.
- The **OpenRouter-native** design: every call is a plain HTTPS POST to
  `/chat/completions`, no provider SDKs. Our `geopol/llm.py` mirrors this.

### What we changed / why

- **Members are lens directives, not different providers.** karpathy's council
  gets diversity from multi-provider models (GPT-5, Gemini, Claude, Grok). Ours
  gets diversity from the 6 system-prompted lens personas ported from
  `src/lib/types.ts` in the original POC (`neutral`, `pessimistic`,
  `optimistic`, `blindsides`, `probabilistic`, `historical`). All 6 use the
  same model (Sonnet 4.6) for the first run. Per-role overrides can come
  later without touching the protocol.
- **Shared input bundle.** Every member receives an identical frozen bundle —
  `base_context` + `fresh_data` (Tavily + RSS/ISW) + `simulation_summary`
  (Stage A output) + the forecast question. No member calls Tavily
  themselves.
- **The chairman writes the report directly.** There is no separate Stage D /
  synthesis step in our pipeline. The chairman's markdown output, rendered
  via Typst to PDF, **is** the deliverable.
- Lens-specific reporting fields: each lens forecast is asked to declare
  `simulation_divergence_notes` and tag each prediction as supported by
  `fresh_data` / `simulation` / `both` / `neither`.

### Reference files

- `backend/council.py` — the 3-stage orchestration and ranking parser.
- `backend/openrouter.py` — the minimal OpenRouter client we mirrored in
  `geopol/llm.py`.
- `backend/config.py` — the `COUNCIL_MODELS` / `CHAIRMAN_MODEL` split that we
  mapped onto our `LENSES` / `MODEL_COUNCIL_CHAIRMAN`.

---

## Why these two, together

Neither component alone is sufficient:

- **snowglobe** gives actor-attributed reasoning and empirical probabilities
  from repeated play, but has no mechanism for grounding against live
  real-world data. On its own it would drift into plausible fiction.
- **llm-council** gives rigorous multi-perspective deliberation grounded in
  whatever context you feed it, but has no independent model of how specific
  decision-makers actually behave. On its own it would collapse into a
  well-organised version of the single-shot lens POC we are replacing.

Composed — snowglobe's simulation summary becomes one of llm-council's inputs
— they produce **two independent forecasting signals in a single pipeline**,
and the interesting predictions are the ones where the research-grounded
council and the actor-driven simulation **disagree**. That divergence is the
actual product.
