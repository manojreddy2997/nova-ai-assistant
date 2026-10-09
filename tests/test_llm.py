
from unittest.mock import patch

from app.backend.llm import generate_response


def collect_response(messages):
    """Collect the streamed response into one string."""
    return "".join(generate_response(messages))


@patch("app.backend.llm.ollama.chat")
@patch("app.backend.llm.retrieve_sources")
def test_answer_uses_retrieved_source(
    mock_retrieve,
    mock_chat,
):
    mock_retrieve.return_value = [
        {
            "text": "Artificial Intelligence is the field of building systems that perform tasks requiring human-like intelligence.",
            "metadata": {
                "source": "ai_basics.pdf",
                "page_number": 1,
                "chunk_index": 0,
            },
            "distance": 0.25,
        }
    ]

    mock_chat.return_value = iter([
        {"message": {"content": "AI builds intelligent systems. "}},
        {"message": {"content": "[Source 1: ai_basics.pdf, Page 1]"}},
    ])

    response = collect_response([
        {"role": "user", "content": "What is AI?"}
    ])

    assert "AI builds intelligent systems." in response
    assert "ai_basics.pdf" in response

    mock_chat.assert_called_once()
    mock_retrieve.assert_called_once_with("What is AI?", top_k=3)


@patch("app.backend.llm.ollama.chat")
@patch("app.backend.llm.retrieve_sources")
def test_no_relevant_documents_use_fallback_prompt(
    mock_retrieve,
    mock_chat,
):
    mock_retrieve.return_value = []

    mock_chat.return_value = iter([
        {"message": {"content": "The available documents do not provide enough information."}}
    ])

    response = collect_response([
        {
            "role": "user",
            "content": "What is the population of Mars in 2026?",
        }
    ])

    assert "do not provide enough information" in response

    call_args = mock_chat.call_args.kwargs
    system_prompt = call_args["messages"][0]["content"]

    assert "No sufficiently relevant document chunks were found" in system_prompt
    assert "do not invent document citations" in system_prompt


@patch("app.backend.llm.ollama.chat")
@patch("app.backend.llm.retrieve_sources")
def test_empty_question_does_not_call_llm(
    mock_retrieve,
    mock_chat,
):
    response = collect_response([
        {"role": "user", "content": "   "}
    ])

    assert response == "Please enter a question."
    mock_retrieve.assert_not_called()
    mock_chat.assert_not_called()


@patch("app.backend.llm.ollama.chat")
@patch("app.backend.llm.retrieve_sources")
def test_document_page_is_included_in_context(
    mock_retrieve,
    mock_chat,
):
    mock_retrieve.return_value = [
        {
            "text": "ETL means Extract, Transform, Load.",
            "metadata": {
                "source": "data_engineering.pdf",
                "page_number": 7,
                "chunk_index": 2,
            },
            "distance": 0.20,
        }
    ]

    mock_chat.return_value = iter([
        {"message": {"content": "ETL means Extract, Transform, Load."}}
    ])

    collect_response([
        {"role": "user", "content": "What does ETL mean?"}
    ])

    call_args = mock_chat.call_args.kwargs
    system_prompt = call_args["messages"][0]["content"]

    assert "[Source 1: data_engineering.pdf, Page 7, Chunk 2]" in system_prompt
    assert "ETL means Extract, Transform, Load." in system_prompt
    