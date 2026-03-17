from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence, Tuple

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:  # pragma: no cover - optional dependency at runtime
    RecursiveCharacterTextSplitter = None


@dataclass(frozen=True)
class GenerationConfig:
    """Sampling defaults inspired by llms-from-scratch ch05 generation patterns."""

    temperature: float = 0.3
    top_k: int = 40
    max_new_tokens: int = 256


@dataclass(frozen=True)
class RetrievalConfig:
    """Chunking defaults inspired by the external RAG challenge pipeline."""

    chunk_size: int = 450
    chunk_overlap: int = 80
    top_k: int = 4


DEFAULT_GENERATION_CONFIG = GenerationConfig()
DEFAULT_RETRIEVAL_CONFIG = RetrievalConfig()


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", str(text).lower())


def _tokens(text: str) -> List[str]:
    return [token for token in _normalize(text).split() if len(token) > 2]


def score_text_relevance(query: str, text: str) -> float:
    """Lightweight lexical reranker inspired by retrieval + reranking pipelines."""
    query_tokens = set(_tokens(query))
    if not query_tokens:
        return 0.0

    text_tokens = _tokens(text)
    if not text_tokens:
        return 0.0

    text_token_set = set(text_tokens)
    overlap = len(query_tokens & text_token_set)
    coverage = overlap / max(len(query_tokens), 1)
    density = overlap / max(len(text_token_set), 1)
    exact_phrase_bonus = 0.35 if _normalize(query).strip() in _normalize(text) else 0.0
    return round((coverage * 0.7) + (density * 0.3) + exact_phrase_bonus, 4)


def split_documents(documents: Sequence[Any], chunk_size: int = DEFAULT_RETRIEVAL_CONFIG.chunk_size,
                    chunk_overlap: int = DEFAULT_RETRIEVAL_CONFIG.chunk_overlap) -> List[Any]:
    """Token-aware chunking with a safe fallback if tiktoken-based splitting fails."""
    if not documents or RecursiveCharacterTextSplitter is None:
        return list(documents)

    try:
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-4o-mini",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    except Exception:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    return splitter.split_documents(list(documents))


def rerank_documents(query: str, documents: Sequence[Any], limit: int = DEFAULT_RETRIEVAL_CONFIG.top_k) -> List[Any]:
    """Rerank LangChain documents using local lexical relevance."""
    ranked: List[Tuple[float, Any]] = []
    for document in documents:
        content = getattr(document, "page_content", "")
        score = score_text_relevance(query, content)
        ranked.append((score, document))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [document for score, document in ranked if score > 0][:limit] or list(documents)[:limit]


def rerank_records(query: str, records: Iterable[Dict[str, Any]], limit: int = DEFAULT_RETRIEVAL_CONFIG.top_k,
                   text_fields: Sequence[str] = ("name", "description", "content", "category", "type")) -> List[Dict[str, Any]]:
    """Rank tourism records against a user query."""
    scored: List[Tuple[float, Dict[str, Any]]] = []
    for record in records:
        combined_text = " ".join(str(record.get(field, "")) for field in text_fields)
        score = score_text_relevance(query, combined_text)
        if score > 0:
            record_copy = dict(record)
            record_copy["relevance_score"] = score
            scored.append((score, record_copy))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [record for _, record in scored[:limit]]


def summarize_ranked_records(query: str, records: Sequence[Dict[str, Any]]) -> str:
    if not records:
        return ""

    bullets = []
    for record in records[:3]:
        name = record.get("name") or record.get("place_name") or record.get("title") or "Recommended place"
        description = str(record.get("description") or record.get("content") or record.get("short_description") or "")
        short_description = description[:180].strip()
        if short_description and not short_description.endswith("."):
            short_description += "..."
        bullets.append(f"- {name}: {short_description or 'Matches your query about Tshwane tourism.'}")

    intro = f"Here are the strongest local matches I found for '{query}':"
    return "\n".join([intro, *bullets])
