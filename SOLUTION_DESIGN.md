# Solution Design — Docs Q&A Assistant

## Problem
Let Solstice Learning admins ask plain-English questions and receive answers grounded in the
supplied support documentation. If the docs do not support an answer, the system should abstain.

## Assumptions
- The seed corpus is a small JSON file containing document IDs, titles, and plain-text content.
- V1 is a local command-line prototype; an HTTP API and LLM are not required.
- Traceability and avoiding unsupported answers are more important than fluent generated prose.

## Approach
1. Load the JSON documents and split content into fixed-size chunks.
2. Fit `TfidfVectorizer` over all chunks, using lowercasing, English stop-word removal,
   unigrams/bigrams, and sublinear term frequency.
3. Vectorize each question and rank chunks with cosine similarity.
4. Return up to `top_k` passages that meet a minimum similarity threshold.
5. If no passage meets the threshold, return `I don't have an answer for that.`
6. Return document IDs, titles, and scores alongside excerpts for auditability.

## Trade-offs
- TF-IDF is lightweight, explainable, and needs no external service or API key.
- It mainly matches lexical overlap, so it can miss semantically equivalent wording.
- A threshold reduces weak matches but does not prove factual support; it must be calibrated
  on representative known-answer and unanswerable questions.
- Returning excerpts is less conversational than LLM-generated answers, but minimizes
  hallucination risk and is a reasonable v1.

## Evaluation and next steps
Run the unit tests and create a labelled evaluation set of answerable and unanswerable questions.
Measure retrieval accuracy and abstention quality, then tune chunk size, n-grams, and threshold.
If needed, compare BM25 or hybrid lexical/semantic retrieval. Only add answer generation if it
can be constrained to retrieved evidence and tested for unsupported claims.
