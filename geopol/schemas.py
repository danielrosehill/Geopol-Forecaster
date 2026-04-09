"""Pydantic schemas — port of `src/lib/schemas.ts`.

Extensions for the new pipeline: `LensForecast` gains `simulation_divergence_notes`
and `predictions_supported_by`, per `03-hybrid-implementation.md` §B.2.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Confidence = Literal["High", "Medium", "Low"]
Support = Literal["fresh_data", "simulation", "both", "neither"]


class Prediction(BaseModel):
    prediction: str
    probability: str
    confidence: Confidence
    reasoning: str
    supported_by: Support = "fresh_data"


class TimeframeForecast(BaseModel):
    overview: str
    predictions: list[Prediction] = Field(min_length=2, max_length=6)
    key_risks: list[str] = Field(min_length=1, max_length=4)
    indicators: list[str] = Field(min_length=1, max_length=3)


class LensForecast(BaseModel):
    lens_id: str
    lens_assessment: str
    timeframes: dict[str, TimeframeForecast]
    simulation_divergence_notes: str = ""


# ─── Fresh data ───

class TavilyCitation(BaseModel):
    url: str
    title: str = ""
    snippet: str = ""


class FreshData(BaseModel):
    timestamp_utc: str
    tavily_queries: list[str] = []
    tavily_answers: list[str] = []
    tavily_citations: list[TavilyCitation] = []
    rss_brief: str = ""
    isw_brief: str = ""

    def as_markdown(self) -> str:
        parts = ["## FRESH DATA", f"*As of {self.timestamp_utc}*", ""]
        if self.tavily_answers:
            parts.append("### Tavily Grounded Answers")
            for q, a in zip(self.tavily_queries, self.tavily_answers):
                parts.append(f"**Q:** {q}")
                parts.append(f"{a}\n")
        if self.tavily_citations:
            parts.append("### Citations")
            for c in self.tavily_citations:
                parts.append(f"- [{c.title or c.url}]({c.url})")
            parts.append("")
        if self.rss_brief:
            parts.append(self.rss_brief)
            parts.append("")
        if self.isw_brief:
            parts.append(self.isw_brief)
        return "\n".join(parts)


# ─── Simulation ───

class ActorAction(BaseModel):
    actor_id: str
    private_assessment: str
    public_statement: str
    concrete_action: str
    redlines_considered: list[str] = []
    confidence_in_action: float = 0.5


class SimulationTurn(BaseModel):
    timestep_label: str
    world_state: str
    actions: list[ActorAction]
    referee_narration: str = ""


class SimulationRun(BaseModel):
    run_idx: int
    turns: list[SimulationTurn]


class SimulationSummary(BaseModel):
    dominant_trajectory: str
    divergent_trajectories: list[str] = []
    actor_behavior_patterns: dict[str, dict[str, list[str]]] = {}
    empirical_probabilities: dict[str, float] = {}
    emergent_dynamics: list[str] = []
    flags_for_council: list[str] = []


class SimulationResult(BaseModel):
    runs: list[SimulationRun]
    summary: SimulationSummary
