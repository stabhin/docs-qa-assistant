"""Answer policy for a retrieval-only Docs Q&A Assistant."""
from typing import Any


ABSTAIN_MESSAGE = "I don't have an answer for that."


def answer_question(
    question: str,
    retriever,
    top_k: int = 3,
) -> dict[str, Any]:
    """
    Return relevant source excerpts rather than inventing a generated answer.

    TF-IDF scores are relevance signals, not calibrated confidence probabilities.
    The threshold must be tuned with known-answer and unknown-answer examples.
    """
    matches = retriever.search(question, top_k=top_k)
    if not matches:
        return {
            "answer": ABSTAIN_MESSAGE,
            "supported": False,
            "sources": [],
        }

    # Retrieval-only v1: present the highest-ranked passage as the answer.
    # Include the source metadata so users can verify the information.
    best = matches[0]
    return {
        "answer": best["text"],
        "supported": True,
        "sources": [
            {
                "doc_id": item["doc_id"],
                "title": item["title"],
                "chunk_index": item["chunk_index"],
                "score": round(item["score"], 4),
                "text": item["text"],
            }
            for item in matches
        ],
    }
