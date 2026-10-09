
import chromadb
from app.backend.embeddings import generate_embeddings

# Local persistent vector database
DB_PATH = "data/chroma_db"
COLLECTION_NAME = "nova_documents"

_client = chromadb.PersistentClient(path=DB_PATH)

_collection = _client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)


def add_chunks(chunks: list, source: str = "sample.pdf") -> int:
    """
    Store document chunks and their metadata in ChromaDB.

    Supports both plain text chunks and dictionaries containing:
    text, page_number, and chunk_index.
    """
    # Remove old chunks belonging to this document.
    _collection.delete(where={"source": source})

    if not chunks:
        return 0

    normalized_chunks = []

    for index, chunk in enumerate(chunks):
        if isinstance(chunk, str):
            normalized_chunks.append({
                "text": chunk,
                "chunk_index": index,
                "page_number": None,
            })
        else:
            normalized_chunks.append({
                "text": chunk["text"],
                "chunk_index": chunk.get("chunk_index", index),
                "page_number": chunk.get("page_number"),
            })

    texts = [chunk["text"] for chunk in normalized_chunks]

    # Convert text into embeddings using the local embedding model.
    embeddings = generate_embeddings(texts)

    # Generate unique IDs for each chunk.
    ids = [
        f"{source}_chunk_{index}"
        for index in range(len(normalized_chunks))
    ]

    metadatas = []

    for chunk in normalized_chunks:
        metadata = {
            "source": source,
            "chunk_index": chunk["chunk_index"],
        }

        if chunk["page_number"] is not None:
            metadata["page_number"] = chunk["page_number"]

        metadatas.append(metadata)

    # Store chunks, embeddings, and metadata.
    _collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(normalized_chunks)


def search_chunks(
    query: str,
    top_k: int = 3,
    max_distance: float = 0.70,
) -> list[dict]:
    """
    Retrieve relevant document chunks using semantic similarity.

    Smaller cosine distances indicate closer matches.
    Results exceeding max_distance are excluded.
    """
    if not query or not query.strip():
        return []

    if top_k <= 0:
        return []

    if _collection.count() == 0:
        return []

    # Convert the user's question into an embedding.
    query_embedding = generate_embeddings([query])[0]

    # Retrieve the closest chunks from ChromaDB.
    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, _collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    matches = []

    documents = results.get("documents") or []
    metadatas = results.get("metadatas") or []
    distances = results.get("distances") or []

    if not documents or not documents[0]:
        return []

    for index, document in enumerate(documents[0]):
        distance = distances[0][index]

        # Filter out weak semantic matches.
        if distance > max_distance:
            continue

        metadata = metadatas[0][index] or {}

        matches.append({
            "text": document,
            "metadata": metadata,
            "distance": distance,
        })

    return matches


def get_collection_count() -> int:
    """Return the total number of indexed chunks."""
    return _collection.count()


def clear_collection() -> None:
    """Delete all indexed chunks from the NOVA collection."""
    existing_ids = _collection.get().get("ids", [])

    if existing_ids:
        _collection.delete(ids=existing_ids)