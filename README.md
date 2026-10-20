# Docs Q&A Assistant — TF-IDF

Retrieval-only Q&A over the provided Solstice Learning documentation. It ranks text chunks using
scikit-learn's `TfidfVectorizer` and cosine similarity. When no result reaches the configured
minimum score, it returns: `I don't have an answer for that.`

## Requirements
- Python 3.10+
- pip

## Setup
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -e ".[dev]"
```

## Run
```bash
python -m docs_qa.main
```
Or tune the abstention threshold:
```bash
python -m docs_qa.main --min-score 0.12 --top-k 3
```

## Tests
```bash
pytest
```

## Design notes / limitations
- TF-IDF is lexical retrieval, not semantic search; synonyms may be missed.
- Cosine similarity is not a probability of correctness. The default threshold `0.12` is a
  starting point and should be tuned against known-answer and out-of-scope test questions.
- The first version returns a source excerpt rather than generating a paraphrase, which reduces
  hallucination risk and keeps answers auditable.
- Fixed-size chunking is simple but may split a sentence or related facts across chunks.
- Production follow-ups: evaluate on a labelled question set, use sentence-aware chunking,
  add source links, and consider BM25 or hybrid retrieval if lexical matching is insufficient.
