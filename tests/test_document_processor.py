
import pytest

from app.backend.document_processor import (
    split_into_chunks,
    split_pages_into_chunks,
)


def test_split_into_chunks_returns_text():
    text = "A" * 2500

    chunks = split_into_chunks(
        text,
        chunk_size=1000,
        overlap=150,
    )

    assert len(chunks) == 3
    assert "".join(chunks[:1]) == "A" * 1000
    assert all(chunk for chunk in chunks)


def test_chunks_preserve_overlap():
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    chunks = split_into_chunks(
        text,
        chunk_size=10,
        overlap=3,
    )

    assert len(chunks) > 1
    assert chunks[0][-3:] == chunks[1][:3]


def test_empty_text_returns_no_chunks():
    assert split_into_chunks("") == []


def test_invalid_chunk_size_raises_error():
    with pytest.raises(ValueError):
        split_into_chunks("Some text", chunk_size=0)


def test_invalid_overlap_raises_error():
    with pytest.raises(ValueError):
        split_into_chunks(
            "Some text",
            chunk_size=10,
            overlap=10,
        )


def test_page_numbers_are_preserved():
    pages = [
        {"page_number": 2, "text": "Artificial Intelligence " * 10},
        {"page_number": 7, "text": "Retrieval Augmented Generation " * 10},
    ]

    chunks = split_pages_into_chunks(
        pages,
        chunk_size=100,
        overlap=20,
    )

    assert chunks
    assert {chunk["page_number"] for chunk in chunks} == {2, 7}

    for chunk in chunks:
        assert chunk["text"]
        assert "chunk_index" in chunk