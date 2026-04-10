"""RSS + ISW news ingestion. Port of `src/lib/rss.ts`.

Uses feedparser instead of the TS regex parser. Keyword filter and age cutoff
match the original.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Iterable

import feedparser
import httpx

USER_AGENT = "GeoPolForecaster/1.0 (conflict analysis research tool)"

KEYWORDS = [
    "iran", "hezbollah", "hizballah", "missile", "rocket", "strike", "idf",
    "irgc", "hormuz", "centcom", "ceasefire", "escalat", "nuclear", "drone",
    "intercept", "shelter", "siren", "houthi", "lebanon", "tehran", "trump",
    "diplomat",
]

RSS_FEEDS = [
    ("Times of Israel", "https://www.timesofisrael.com/feed/"),
    ("Jerusalem Post", "https://www.jpost.com/rss/rssfeedsfrontpage.aspx"),
]

ISW_API = "https://understandingwar.org/wp-json/wp/v2/posts"


@dataclass
class Article:
    title: str
    link: str
    pub_date: str
    description: str
    source: str
    full_text: str | None = None


@dataclass
class NewsBrief:
    articles: list[Article] = field(default_factory=list)
    isw_reports: list[Article] = field(default_factory=list)
    rss_brief: str = ""
    isw_brief: str = ""


def _strip_html(html: str) -> str:
    import re
    return re.sub(r"<[^>]+>", "", html).replace("&nbsp;", " ").replace("&amp;", "&").strip()


def _has_keyword(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in KEYWORDS)


def _within_age(pub_date: str, max_age_hours: int) -> bool:
    if not pub_date:
        return True
    try:
        dt = datetime(*feedparser._parse_date(pub_date)[:6], tzinfo=timezone.utc)  # type: ignore[misc]
    except Exception:
        return True
    return dt >= datetime.now(timezone.utc) - timedelta(hours=max_age_hours)


async def _fetch_rss(client: httpx.AsyncClient, name: str, url: str, max_age_hours: int) -> list[Article]:
    r = await client.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
    r.raise_for_status()
    parsed = feedparser.parse(r.text)
    out: list[Article] = []
    for item in parsed.entries:
        title = getattr(item, "title", "")
        link = getattr(item, "link", "")
        pub = getattr(item, "published", "") or getattr(item, "updated", "")
        desc = _strip_html(getattr(item, "summary", "") or getattr(item, "description", ""))
        title = _strip_html(title)
        if not title or not link:
            continue
        blob = f"{title} {desc}"
        if not _has_keyword(blob):
            continue
        if not _within_age(pub, max_age_hours):
            continue
        out.append(Article(title=title, link=link, pub_date=pub, description=desc[:500], source=name))
    return out


async def _fetch_isw(client: httpx.AsyncClient, max_posts: int = 3) -> list[Article]:
    params = {
        "per_page": max_posts,
        "search": "iran update",
        "_fields": "title,date,link,content,excerpt",
    }
    r = await client.get(ISW_API, params=params, headers={"User-Agent": USER_AGENT}, timeout=20)
    r.raise_for_status()
    posts = r.json()
    import re
    def strip(html: str) -> str:
        return re.sub(r"<[^>]+>", "", html).replace("&nbsp;", " ").strip()
    out: list[Article] = []
    for p in posts:
        title = strip(p["title"]["rendered"])
        full = strip(p["content"]["rendered"])
        excerpt = strip(p["excerpt"]["rendered"])[:500]
        out.append(Article(
            title=title, link=p["link"], pub_date=p["date"],
            description=excerpt, source="ISW/CTP", full_text=full,
        ))
    return out


def _format_rss_brief(articles: Iterable[Article]) -> str:
    arts = list(articles)
    if not arts:
        return "No conflict-relevant news articles found in RSS feeds."
    lines = [
        f"## NEWS HEADLINES ({len(arts)} conflict-relevant articles)",
        f"*Fetched: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*",
        "",
    ]
    for a in arts:
        lines.append(f"- **{a.title}** ({a.pub_date}, {a.source})")
        if a.description:
            lines.append(f"  {a.description[:300]}")
    return "\n".join(lines)


def _format_isw_brief(reports: Iterable[Article]) -> str:
    rs = list(reports)
    if not rs:
        return "No ISW/CTP Iran Updates available."
    lines = [
        "## ISW/CTP EXPERT ANALYSIS",
        f"*{len(rs)} recent Iran Update(s)*",
        "",
    ]
    for r in rs:
        lines.append(f"### {r.title}")
        lines.append(f"*Published: {r.pub_date}*")
        lines.append(f"*Source: {r.link}*")
        lines.append("")
        if r.full_text:
            text = r.full_text
            if len(text) > 15_000:
                text = text[:15_000] + "\n\n[... truncated for length ...]"
            lines.append(text)
        lines.append("")
    return "\n".join(lines)


async def fetch_all_news(max_age_hours: int = 48) -> NewsBrief:
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[_fetch_rss(client, name, url, max_age_hours) for name, url in RSS_FEEDS],
            _fetch_isw(client, 3),
            return_exceptions=True,
        )
    articles: list[Article] = []
    for r in results[:-1]:
        if isinstance(r, list):
            articles.extend(r)
    isw: list[Article] = results[-1] if isinstance(results[-1], list) else []

    # Dedupe
    seen: set[str] = set()
    deduped: list[Article] = []
    for a in articles:
        key = "".join(c.lower() for c in a.title if c.isalnum())[:50]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(a)

    return NewsBrief(
        articles=deduped,
        isw_reports=isw,
        rss_brief=_format_rss_brief(deduped),
        isw_brief=_format_isw_brief(isw),
    )
