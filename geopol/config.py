"""Central configuration. All LLM calls route through OpenRouter.

Per locked decisions: one model everywhere (Claude Sonnet 4.6 via OpenRouter),
Monte Carlo N=1 for the first run, 6 lens council members, Tavily-only grounding.
Per-role overrides are declared here so they can diverge later without rewiring.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ─── Routing ───
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_CHAT_URL = f"{OPENROUTER_BASE_URL}/chat/completions"

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ─── Models (all the same for first run; override per role later) ───
MODEL_DEFAULT = "anthropic/claude-sonnet-4.5"

MODEL_SIM_ACTOR = MODEL_DEFAULT
MODEL_SIM_REFEREE = MODEL_DEFAULT
MODEL_COUNCIL_MEMBER = MODEL_DEFAULT
MODEL_COUNCIL_CHAIRMAN = MODEL_DEFAULT
MODEL_RESEARCHER = MODEL_DEFAULT

# ─── Simulation parameters ───
MC_RUNS = 1
SIM_TIMESTEPS = 3
TIMESTEP_LABELS = ["+24h", "+72h", "+2 weeks"]

# ─── Paths ───
REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = REPO_ROOT / "reports"


@dataclass
class Settings:
    openrouter_api_key: str | None = OPENROUTER_API_KEY
    tavily_api_key: str | None = TAVILY_API_KEY
    model_default: str = MODEL_DEFAULT
    mc_runs: int = MC_RUNS
    sim_timesteps: int = SIM_TIMESTEPS


settings = Settings()


def require_keys() -> None:
    missing = []
    if not OPENROUTER_API_KEY:
        missing.append("OPENROUTER_API_KEY")
    if not TAVILY_API_KEY:
        missing.append("TAVILY_API_KEY")
    if missing:
        raise RuntimeError(
            f"Missing required env vars: {', '.join(missing)}. "
            "Set them in .env or the shell environment."
        )
