
from unittest.mock import patch

from app.backend.vector_store import search_chunks


def test_empty_query_returns_no_results():
    assert search_chunks("") == []
    assert search_chunks("   ") == []


def test_non_positive_top_k_returns_no_results():
    assert search_chunks("What is AI?", top_k=0) == []
    assert search_chunks("What is AI?", top_k=-1) == []


@patch("app.backend.vector_store.generate_embeddings")
@patch("app.backend.vector_store._collection")
def test_relevant_chunks_are_returned(mock_collection, mock_embeddings):
    mock_collection.count.return_value = 2
    mock_embeddings.return_value = [[0.1, 0.2, 0.3]]

    mock_collection.query.return_value = {
        "documents": [["Artificial Intelligence is AI."]],
        "metadatas": [[
            {
                "source": "ai_basics.pdf",
                "page_number": 1,
                "chunk_index": 0,
            }
        ]],
        "distances": [[0.25]],
    }

    results = search_chunks("What is AI?")

    assert len(results) == 1
    assert results[0]["text"] == "Artificial Intelligence is AI."
    assert results[0]["metadata"]["source"] == "ai_basics.pdf"
    assert results[0]["metadata"]["page_number"] == 1
    assert results[0]["distance"] == 0.25


@patch("app.backend.vector_store.generate_embeddings")
@patch("app.backend.vector_store._collection")
def test_irrelevant_chunks_are_filtered(mock_collection, mock_embeddings):
    mock_collection.count.return_value = 2
    mock_embeddings.return_value = [[0.1, 0.2, 0.3]]

    mock_collection.query.return_value = {
        "documents": [
            [
                "Unrelated document content.",
                "Another unrelated document.",
            ]
        ],
        "metadatas": [[
            {"source": "sample.pdf", "page_number": 3},
            {"source": "sample.pdf", "page_number": 4},
        ]],
        "distances": [[0.85, 0.95]],
    }

    results = search_chunks(
        "What is the population of Mars?",
        top_k=2,
        max_distance=0.70,
    )

    assert results == []


@patch("app.backend.vector_store.generate_embeddings")
@patch("app.backend.vector_store._collection")
def test_chunks_above_threshold_are_excluded(
    mock_collection,
    mock_embeddings,
):
    mock_collection.count.return_value = 3
    mock_embeddings.return_value = [[0.1, 0.2, 0.3]]

    mock_collection.query.return_value = {
        "documents": [
            ["Relevant chunk.", "Borderline chunk.", "Irrelevant chunk."]
        ],
        "metadatas": [[
            {"source": "a.pdf", "page_number": 1},
            {"source": "b.pdf", "page_number": 2},
            {"source": "c.pdf", "page_number": 3},
        ]],
        "distances": [[0.30, 0.70, 0.91]],
    }

    results = search_chunks("Test query", top_k=3, max_distance=0.70)

    assert len(results) == 2
    assert results[0]["text"] == "Relevant chunk."
    assert results[1]["text"] == "Borderline chunk."