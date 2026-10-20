import json

from docs_qa.retriever import TfidfRetriever, chunk_all_docs
from docs_qa.answer import ABSTAIN_MESSAGE, answer_question


def test_chunking_keeps_final_partial_chunk():
    chunks = chunk_all_docs([
        {"doc_id": "D1", "title": "Example", "content": "abcdefghij"}
    ], chunk_size=4)
    assert [chunk["text"] for chunk in chunks] == ["abcd", "efgh", "ij"]


def test_known_question_retrieves_password_document():
    docs = [{
        "doc_id": "D1",
        "title": "Resetting Your Password",
        "content": (
            "Click Forgot password on the login screen. Password reset links "
            "expire after 15 minutes. Choose a password at least 8 characters long."
        ),
    }, {
        "doc_id": "D2",
        "title": "Billing",
        "content": "Invoices are emailed three days before monthly renewal.",
    }]
    retriever = TfidfRetriever(chunk_all_docs(docs), min_score=0.01)
    matches = retriever.search("How long do password reset links last?")
    assert matches
    assert matches[0]["title"] == "Resetting Your Password"


def test_unrelated_question_abstains():
    docs = [{
        "doc_id": "D1",
        "title": "Password",
        "content": "Reset your password from the login page.",
    }]
    retriever = TfidfRetriever(chunk_all_docs(docs), min_score=0.5)
    result = answer_question("What is the weather on Mars?", retriever)
    assert result["answer"] == ABSTAIN_MESSAGE
    assert result["supported"] is False
