
from pathlib import Path

from pypdf import PdfReader


def extract_pages_from_pdf(pdf_path: str) -> list[dict]:
    """Extract text page by page while preserving original page numbers."""

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(str(path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append(
                {
                    "page_number": page_number,
                    "text": text.strip(),
                }
            )

    return pages


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from every page of a PDF."""

    pages = extract_pages_from_pdf(pdf_path)

    return "\n\n".join(
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in pages
    )


def split_into_chunks(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:
    """Split text into overlapping character-based chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size.")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


def split_pages_into_chunks(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict]:
    """Split each PDF page into chunks while preserving its page number."""

    chunks = []

    for page in pages:
        page_chunks = split_into_chunks(
            page["text"],
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk_index, chunk_text in enumerate(page_chunks):
            chunks.append(
                {
                    "text": chunk_text,
                    "page_number": page["page_number"],
                    "chunk_index": chunk_index,
                }
            )

    return chunks