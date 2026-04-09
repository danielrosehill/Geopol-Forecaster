"""Tavily search client — produces grounded Q/A pairs + citations."""
from __future__ import annotations

from dataclasses import dataclass

import httpx

from ..config import TAVILY_API_KEY


@dataclass
class TavilyResult:
    query: str
    answer: str
    citations: list[dict[str, str]]


TAVILY_URL = "https://api.tavily.com/search"


async def tavily_search(query: str, max_results: int = 5) -> TavilyResult:
    if not TAVILY_API_KEY:
        return TavilyResult(query=query, answer="(tavily disabled — no key)", citations=[])
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "include_answer": True,
        "max_results": max_results,
        "topic": "news",
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(TAVILY_URL, json=payload)
        r.raise_for_status()
        data = r.json()
    citations = [
        {"url": x.get("url", ""), "title": x.get("title", ""), "snippet": x.get("content", "")[:400]}
        for x in data.get("results", [])
    ]
    return TavilyResult(query=query, answer=data.get("answer", ""), citations=citations)


async def derive_queries(forecast_question: str) -> list[str]:
    """Quick heuristic — turn one forecast question into ~4 Tavily searches.

    Kept deliberately simple for v1; a smarter query-expansion agent can replace
    this later without touching the rest of the pipeline.
    """
    q = forecast_question.strip().rstrip("?")
    return [
        f"{q} latest news",
        f"{q} analysis expert",
        "Iran Israel ceasefire status this week",
        "IDF IRGC Hezbollah escalation latest",
    ]
