"""TF-IDF retrieval for the Docs Q&A Assistant."""
import json
from pathlib import Path
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_CHUNK_SIZE = 400


def load_docs(path: str | Path) -> list[dict[str, Any]]:
    """Load docs from a JSON file shaped like { "docs": [...] }."""
    with open(path, encoding="utf-8") as file:
        payload = json.load(file)
    docs = payload.get("docs", [])
    for doc in docs:
        if not all(key in doc for key in ("doc_id", "title", "content")):
            raise ValueError("Each document must contain doc_id, title, and content.")
    return docs


def chunk_text(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE) -> list[str]:
    """Split text into chunks and keep the final partial chunk."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    return [
        text[start:start + chunk_size].strip()
        for start in range(0, len(text), chunk_size)
        if text[start:start + chunk_size].strip()
    ]


def chunk_all_docs(
    docs: list[dict[str, Any]], chunk_size: int = DEFAULT_CHUNK_SIZE
) -> list[dict[str, Any]]:
    """Flatten articles into chunks while preserving article metadata."""
    chunks = []
    for doc in docs:
        for index, chunk in enumerate(chunk_text(doc["content"], chunk_size)):
            chunks.append({
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "chunk_index": index,
                "text": chunk,
            })
    return chunks


class TfidfRetriever:
    """Fit TF-IDF once, then rank chunks by cosine similarity."""

    def __init__(
        self,
        chunks: list[dict[str, Any]],
        min_score: float = 0.12,
    ) -> None:
        if not chunks:
            raise ValueError("No document chunks were loaded.")
        if not 0 <= min_score <= 1:
            raise ValueError("min_score must be between 0 and 1")

        self.chunks = chunks
        self.min_score = min_score
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
        )
        self.matrix = self.vectorizer.fit_transform(
            chunk["text"] for chunk in chunks
        )

    def search(self, question: str, top_k: int = 3) -> list[dict]:
        question = question.strip()

        if not question or top_k < 1:
            return []

        query_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(query_vector, self.matrix).ravel()

        ranked_indices = scores.argsort()[::-1]

        results = []
        seen_doc_ids = set()

        for index in ranked_indices:
            score = float(scores[index])

            if score < self.min_score:
                break

            chunk = self.chunks[int(index)]
            doc_id = chunk["doc_id"]

            # Skip additional chunks from the same document
            if doc_id in seen_doc_ids:
                continue

            result = dict(chunk)
            result["score"] = score
            results.append(result)
            seen_doc_ids.add(doc_id)

            if len(results) >= top_k:
                break

        return results