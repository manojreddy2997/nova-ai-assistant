
from sentence_transformers import SentenceTransformer

# A small, open-source embedding model that runs locally.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None


def get_embedding_model():
    """Load the embedding model once and reuse it."""
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Convert text chunks into numerical vectors."""
    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.tolist()