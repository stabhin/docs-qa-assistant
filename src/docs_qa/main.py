"""Command-line entry point."""
import argparse
from pathlib import Path

from docs_qa.answer import answer_question
from docs_qa.retriever import TfidfRetriever, chunk_all_docs, load_docs


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DOCS_PATH = PROJECT_ROOT / "data" / "docs.json"


def build_retriever(docs_path: Path, min_score: float) -> TfidfRetriever:
    docs = load_docs(docs_path)
    chunks = chunk_all_docs(docs)
    return TfidfRetriever(chunks, min_score=min_score)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask questions about Solstice docs.")
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS_PATH)
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.12,
        help="Minimum cosine similarity required to return a result (tune with tests).",
    )
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    retriever = build_retriever(args.docs, args.min_score)
    print("Docs Q&A Assistant (TF-IDF). Type 'exit' to quit.")
    while True:
        try:
            question = input("\nQuestion: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if question.lower() in {"exit", "quit"}:
            break
        result = answer_question(question, retriever, top_k=args.top_k)
        print("\nAnswer:", result["answer"])
        if result["sources"]:
            print("Sources:")
            for source in result["sources"]:
                print(
                    f"- {source['title']} ({source['doc_id']}, "
                    f"score={source['score']:.4f})"
                )
        print()
if __name__ == "__main__":
    main()
