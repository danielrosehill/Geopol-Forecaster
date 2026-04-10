"""Pinecone vector store for archiving and retrieving past forecast runs.

Uses httpx directly against the integrated index REST API (the index has
built-in embeddings, so we upsert plain text and it embeds server-side).
"""
from __future__ import annotations

import httpx

from .config import PINECONE_API_KEY, PINECONE_INDEX_HOST

_NAMESPACE = "runs"
_TIMEOUT = 30.0


def _headers() -> dict[str, str]:
    return {
        "Api-Key": PINECONE_API_KEY or "",
        "Content-Type": "application/json",
        "X-Pinecone-API-Version": "2025-04",
    }


async def upsert_run(
    session_id: str,
    question: str,
    created_at: str,
    chairman_md: str,
    sim_summary_text: str,
    lens_digest: str,
    mode: str = "full",
) -> None:
    """Upsert 3 records for a completed forecast run."""
    if not PINECONE_API_KEY:
        print("[pinecone] no API key — skipping upsert")
        return

    records = [
        {
            "_id": f"{session_id}/chairman",
            "text": chairman_md[:40000],
            "session_id": session_id,
            "question": question,
            "created_at": created_at,
            "record_type": "chairman",
            "mode": mode,
        },
        {
            "_id": f"{session_id}/sim_summary",
            "text": sim_summary_text[:20000],
            "session_id": session_id,
            "question": question,
            "created_at": created_at,
            "record_type": "simulation",
            "mode": mode,
        },
        {
            "_id": f"{session_id}/lenses",
            "text": lens_digest[:40000],
            "session_id": session_id,
            "question": question,
            "created_at": created_at,
            "record_type": "lenses",
            "mode": mode,
        },
    ]

    url = f"{PINECONE_INDEX_HOST}/records/namespaces/{_NAMESPACE}/upsert"
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        for rec in records:
            try:
                resp = await client.post(url, json=rec, headers=_headers())
                resp.raise_for_status()
            except Exception as e:
                print(f"[pinecone] upsert {rec['_id']} failed: {e}")


async def query_past_runs(question: str, top_k: int = 3) -> str:
    """Query Pinecone for past chairman reports relevant to the question.

    Returns a formatted markdown string for injection into the chairman prompt,
    or empty string if Pinecone is unavailable.
    """
    if not PINECONE_API_KEY:
        return ""

    url = f"{PINECONE_INDEX_HOST}/records/namespaces/{_NAMESPACE}/search"
    payload = {
        "query": {"top_k": top_k, "inputs": {"text": question}},
        "fields": ["text", "question", "created_at", "session_id"],
    }

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(url, json=payload, headers=_headers())
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        print(f"[pinecone] query failed: {e}")
        return ""

    hits = data.get("result", {}).get("hits", [])
    if not hits:
        return ""

    parts = []
    for hit in hits:
        fields = hit.get("fields", {})
        created = fields.get("created_at", "unknown date")
        q = fields.get("question", "")
        text = fields.get("text", "")[:3000]
        parts.append(
            f"### Past run ({created})\n**Question:** {q}\n\n{text}"
        )

    return "\n\n---\n\n".join(parts)
