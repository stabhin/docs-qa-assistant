# Solution Design — Docs Q&A Assistant

## 1. Problem

Solstice Learning's support team receives many repeated questions from administrators about topics such as password resets, billing, and report exports. The answers already exist in the company's documentation, but users find it difficult to locate the right information.

The goal is to build a simple application where users can ask questions in everyday English and receive answers from the available documentation.

If the documentation does not contain the answer, the application should clearly say, **"I don't have an answer for that"** instead of guessing.

## 2. Assumptions

- The documentation is provided as a JSON file containing article titles, IDs, and content.
- The first version will be a simple application that runs locally on a computer.
- The application does not need a web interface or an AI language model in the first version.
- Providing reliable answers from the documentation is more important than giving long or conversational responses.

## 3. Proposed Solution

The application uses **TF-IDF**, a technique that helps identify which pieces of text are most relevant to a user's question.

The process works as follows:

1. **Load the documentation:** Read the available support articles from the JSON file.

2. **Break articles into smaller pieces:** Divide long articles into smaller sections so the application can search for relevant information more easily.

3. **Prepare the text for searching:** Use TF-IDF to give words different importance based on how frequently they appear and how useful they are for distinguishing one section from another. The application considers both individual words and pairs of words.

4. **Find the most relevant information:** When a user asks a question, compare it with the available sections and rank the results based on how closely their wording matches.

5. **Check whether the match is strong enough:** Return relevant information only when its similarity score meets a configured minimum threshold. If no result meets that threshold, respond with "I don't have an answer for that."

6. **Show the source:** Display the article title, document ID, matching text, and similarity score so users can see where the answer came from.

The first version returns relevant text directly from the documentation rather than generating new answers. This helps reduce the risk of providing information that the documentation does not support.

## 4. Benefits and Limitations

### Benefits

- **Simple and cost-effective:** TF-IDF runs locally and does not require an external AI service or API key.
- **Easy to understand:** The application can show which document sections matched a question and their similarity scores.
- **Reduces unsupported answers:** The application can refuse to answer when no result meets the configured threshold.
- **Easy to maintain:** The documentation can be updated without introducing a complex AI infrastructure.

### Limitations

- **Depends on matching words:** Questions that use different words to express the same meaning may not retrieve the correct article.
- **The threshold needs testing:** A high threshold may reject valid questions, while a low threshold may accept irrelevant results.
- **Answers may be incomplete:** If a relevant fact is split across multiple sections, returning only one section may omit important details.
- **Responses are less conversational:** The application returns documentation excerpts instead of composing a natural-language explanation.

A high similarity score does not guarantee that an answer is correct. The retrieved text must still contain information that supports the answer.

## 5. Testing and Future Improvements

The application should be tested with questions whose answers are available in the documentation, as well as questions that the documentation cannot answer.

The next steps are:

1. Measure how often the correct article is retrieved.
2. Check whether unsupported questions correctly receive the fallback response.
3. Adjust the similarity threshold and section size based on test results.
4. Improve searching for questions that use different words from the documentation, potentially by comparing TF-IDF with BM25 or a combination of keyword and semantic search.
5. Consider adding an AI language model in a future version to provide clearer, more conversational answers, while requiring it to use the retrieved documentation as evidence.

The priority for the first version is to build a small, working, and testable solution that provides traceable answers and avoids guessing when the documentation is insufficient.