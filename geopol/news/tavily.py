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
        {"url": x.get("url", ""), "title": x.get("title", ""), "snippet": x.get("content", "")[:800]}
        for x in data.get("results", [])
    ]
    return TavilyResult(query=query, answer=data.get("answer", ""), citations=citations)


async def derive_queries(forecast_question: str) -> list[str]:
    """Quick heuristic — turn one forecast question into ~4 Tavily searches.

    Kept deliberately simple for v1; a smarter query-expansion agent can replace
    this later without touching the rest of the pipeline.
    """
    # Tavily has a ~400-char query limit — collapse whitespace, drop frontmatter
    # and markdown, and truncate to a short headline.
    raw = forecast_question.strip()
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            raw = parts[2]
    # Take the first non-empty, non-heading line as the headline.
    headline = ""
    for line in raw.splitlines():
        line = line.strip().lstrip("#").strip()
        if line and not line.startswith("-"):
            headline = line
            break
    q = (headline or raw).rstrip("?")[:180]
    return [
        f"{q} latest news",
        f"{q} analysis expert",
        "Iran Israel ceasefire diplomacy status this week",
        "IDF IRGC Hezbollah escalation latest",
        "Russia China Iran nuclear facility latest",
        "Strait of Hormuz shipping oil transit latest",
    ]
