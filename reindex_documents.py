
from pathlib import Path

from app.backend.document_processor import (
    extract_pages_from_pdf,
    split_pages_into_chunks,
)
from app.backend.vector_store import add_chunks


DOCUMENTS_DIR = Path("data/documents")

for pdf_path in DOCUMENTS_DIR.glob("*.pdf"):
    print(f"\nProcessing: {pdf_path.name}")

    pages = extract_pages_from_pdf(str(pdf_path))
    chunks = split_pages_into_chunks(pages)

    stored = add_chunks(
        chunks,
        source=pdf_path.name,
    )

    print(f"Pages extracted: {len(pages)}")
    print(f"Chunks stored: {stored}")

print("\nRe-indexing complete!")