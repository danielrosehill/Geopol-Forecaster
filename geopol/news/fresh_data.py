"""Single context-gathering agent. Runs once at pipeline start, freezes a
`FreshData` bundle, and that bundle is seeded identically to every council
member. No member calls Tavily themselves.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from ..schemas import FreshData, TavilyCitation
from .rss import fetch_all_news
from .tavily import derive_queries, tavily_search


async def gather_fresh_data(forecast_question: str) -> FreshData:
    queries = await derive_queries(forecast_question)
    news_task = fetch_all_news(48)
    tavily_tasks = [tavily_search(q) for q in queries]
    news, *tavily_results = await asyncio.gather(news_task, *tavily_tasks)

    citations: list[TavilyCitation] = []
    answers: list[str] = []
    for tr in tavily_results:
        answers.append(tr.answer)
        for c in tr.citations:
            citations.append(TavilyCitation(**c))

    return FreshData(
        timestamp_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        tavily_queries=queries,
        tavily_answers=answers,
        tavily_citations=citations,
        rss_brief=news.rss_brief,
        isw_brief=news.isw_brief,
    )
