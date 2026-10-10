
import re

import chromadb

from app.backend.embeddings import generate_embeddings


# --------------------------------------------------
# ChromaDB configuration
# --------------------------------------------------

DB_PATH = "data/chroma_db"
COLLECTION_NAME = "nova_documents"

_client = chromadb.PersistentClient(path=DB_PATH)

_collection = _client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)


# --------------------------------------------------
# Add document chunks
# --------------------------------------------------

def add_chunks(chunks: list, source: str = "sample.pdf") -> int:
    """
    Add document chunks to ChromaDB.

    Supports plain text chunks and dictionaries containing:
    - text
    - chunk_index
    - page_number

    Existing chunks for the same source are replaced.
    Returns the number of chunks indexed.
    """
    if not chunks:
        return 0

    # Extract text and metadata from each chunk.
    texts = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        if isinstance(chunk, dict):
            text = chunk.get("text", "")

            if not isinstance(text, str) or not text.strip():
                continue

            metadata = {
                "source": source,
                "chunk_index": chunk.get("chunk_index", index),
            }

            page_number = chunk.get("page_number")

            if page_number is not None:
                metadata["page_number"] = page_number

        else:
            text = str(chunk)

            if not text.strip():
                continue

            metadata = {
                "source": source,
                "chunk_index": index,
            }

        texts.append(text)
        metadatas.append(metadata)

    if not texts:
        return 0

    # Generate embeddings for all valid chunks.
    embeddings = generate_embeddings(texts)

    if hasattr(embeddings, "tolist"):
        embeddings = embeddings.tolist()

    # Replace previously indexed chunks for this source.
    _collection.delete(where={"source": source})

    # Keep IDs stable for each source and chunk position.
    ids = [
        f"{source}_chunk_{metadata['chunk_index']}"
        for metadata in metadatas
    ]

    # Store text, metadata, and embeddings.
    _collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    return len(texts)


# --------------------------------------------------
# Search document chunks
# --------------------------------------------------

def search_chunks(
    query: str,
    top_k: int = 3,
    max_distance: float = 0.70,
) -> list[dict]:
    """
    Retrieve relevant document chunks using semantic similarity.

    Common AI acronyms are expanded before embedding the query.
    Smaller cosine distances indicate closer matches.
    Results exceeding max_distance are excluded.
    """
    if not query or not query.strip():
        return []

    if top_k <= 0:
        return []

    collection_count = _collection.count()

    if collection_count == 0:
        return []

    # Expand common AI acronyms to improve semantic matching.
    acronym_expansions = {
        "RAG": "Retrieval-Augmented Generation",
        "LLM": "Large Language Model",
        "ML": "Machine Learning",
        "AI": "Artificial Intelligence",
        }

    expanded_query = query

    for acronym, expansion in acronym_expansions.items():
        expanded_query = re.sub(
            rf"\b{acronym}\b",
            expansion,
            expanded_query,
            flags=re.IGNORECASE,
        )

    # Generate the query embedding.
    query_embedding = generate_embeddings([expanded_query])[0]

    if hasattr(query_embedding, "tolist"):
        query_embedding = query_embedding.tolist()

    # Retrieve the closest chunks.
    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection_count),
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents") or []
    metadatas = results.get("metadatas") or []
    distances = results.get("distances") or []

    if not documents or not documents[0]:
        return []

    matches = []

    for index, document in enumerate(documents[0]):
        distance = distances[0][index]

        # Preserve the relevance threshold.
        if distance > max_distance:
            continue

        metadata = (
            metadatas[0][index]
            if metadatas and metadatas[0]
            else {}
        ) or {}

        matches.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return matches


# --------------------------------------------------
# Collection utilities
# --------------------------------------------------

def get_collection_count() -> int:
    """Return the total number of indexed chunks."""
    return _collection.count()


def clear_collection() -> None:
    """Delete all indexed chunks from the NOVA collection."""
    existing_ids = _collection.get().get("ids", [])

    if existing_ids:
        _collection.delete(ids=existing_ids)
