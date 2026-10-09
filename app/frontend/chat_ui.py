
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.backend.document_processor import (
    extract_pages_from_pdf,
    split_pages_into_chunks,
)
from app.backend.llm import generate_response, retrieve_sources
from app.backend.vector_store import add_chunks


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="NOVA AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .nova-subtitle {
        color: #8b95a5;
        font-size: 1rem;
        margin-top: -12px;
        margin-bottom: 24px;
    }

    .nova-card {
        padding: 20px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 14px;
        margin-bottom: 12px;
    }

    .nova-label {
        font-size: 0.85rem;
        color: #8b95a5;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Session state
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = set()

if "message_sources" not in st.session_state:
    st.session_state.message_sources = {}


# --------------------------------------------------
# Source display helper
# --------------------------------------------------

def display_sources(sources):
    """Display retrieved document chunks with metadata."""

    if not sources:
        st.caption("No document sources were retrieved.")
        return

    with st.expander(f"📚 Retrieved sources ({len(sources)})"):
        for number, source in enumerate(sources, start=1):
            metadata = source.get("metadata", {})

            source_name = metadata.get("source", "Unknown document")
            page_number = metadata.get("page_number")
            chunk_index = metadata.get("chunk_index")
            distance = source.get("distance")

            st.markdown(f"**Source {number}: {source_name}**")

            details = []

            if page_number is not None:
                details.append(f"Page {page_number}")

            if chunk_index is not None:
                details.append(f"Chunk {int(chunk_index) + 1}")

            if distance is not None:
                details.append(f"Distance: {distance:.3f}")

            if details:
                st.caption(" · ".join(details))

            st.write(source.get("text", ""))

            if number < len(sources):
                st.divider()


# --------------------------------------------------
# PDF upload and indexing helper
# --------------------------------------------------

def index_uploaded_pdf(uploaded_pdf):
    """Save, extract, chunk, and index a PDF with page metadata."""

    safe_name = Path(uploaded_pdf.name).name
    documents_dir = PROJECT_ROOT / "data" / "documents"
    documents_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = documents_dir / safe_name
    pdf_path.write_bytes(uploaded_pdf.getvalue())

    pages = extract_pages_from_pdf(str(pdf_path))

    if not pages:
        raise ValueError(
            "No readable text was found. "
            "Scanned PDFs may require OCR."
        )

    chunks = split_pages_into_chunks(pages)

    if not chunks:
        raise ValueError("No text chunks could be created.")

    count = add_chunks(chunks, source=safe_name)

    return len(pages), count


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.title("🤖 NOVA")
    st.caption("Your Local Intelligent AI Assistant")

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.message_sources = {}
        st.rerun()

    st.divider()

    st.subheader("📄 Knowledge Base")

    uploaded_pdf = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        help="Upload a PDF to make its contents searchable by NOVA.",
    )

    if uploaded_pdf is not None:
        file_key = (uploaded_pdf.name, uploaded_pdf.size)

        if file_key not in st.session_state.uploaded_files:
            if st.button(
                "Add PDF to Knowledge Base",
                use_container_width=True,
                type="primary",
            ):
                try:
                    with st.spinner(
                        "Extracting pages and indexing document..."
                    ):
                        page_count, chunk_count = index_uploaded_pdf(
                            uploaded_pdf
                        )

                    st.session_state.uploaded_files.add(file_key)

                    st.success(
                        f"Indexed {uploaded_pdf.name} successfully!"
                    )
                    st.write(f"Pages extracted: {page_count}")
                    st.write(f"Chunks stored: {chunk_count}")

                except Exception as error:
                    st.error("Could not process this PDF.")
                    st.caption(f"Details: {error}")

        else:
            st.success("This file has already been indexed in this session.")

    st.caption("Document folder: data/documents")

    st.divider()

    st.subheader("System Status")
    st.write("**Model:** `llama3.2:3b`")
    st.write("**Runtime:** Local Ollama")
    st.write("**Vector database:** ChromaDB")
    st.write("**Embeddings:** Local embedding model")
    st.write("**Privacy:** Documents stored locally")

    st.divider()

    st.subheader("About NOVA")
    st.write(
        "NOVA is a document-aware AI assistant built with "
        "Python, Streamlit, Ollama, embeddings, and ChromaDB."
    )
    st.caption("NOVA v0.8")


# --------------------------------------------------
# Main page
# --------------------------------------------------

st.title("🤖 NOVA AI Assistant")

st.markdown(
    '<p class="nova-subtitle">'
    "Your ideas. Your conversations. Your local AI."
    "</p>",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Welcome screen
# --------------------------------------------------

if not st.session_state.messages:
    st.markdown("### Welcome! What would you like to explore?")
    st.write(
        "Ask a question, learn a technical concept, or query your PDFs."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🧠 Explain an AI concept",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Explain artificial intelligence in simple terms "
                "with a practical example."
            )
            st.rerun()

        if st.button(
            "💻 Help me write Python code",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Teach me a useful Python programming example."
            )
            st.rerun()

    with col2:
        if st.button(
            "📚 Ask about my PDFs",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Summarize the main ideas in my uploaded PDF documents "
                "using relevant retrieved sources."
            )
            st.rerun()

        if st.button(
            "🚀 Improve my AI project",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Suggest the next practical improvement for my "
                "NOVA AI Assistant project."
            )
            st.rerun()

    st.divider()

# --------------------------------------------------
# Display conversation history
# --------------------------------------------------

for index, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            saved_sources = st.session_state.message_sources.get(
                index, []
            )

            if saved_sources:
                display_sources(saved_sources)


# --------------------------------------------------
# User input
# --------------------------------------------------

user_message = st.chat_input("Message NOVA...")

if st.session_state.pending_prompt:
    user_message = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


# --------------------------------------------------
# Generate response
# --------------------------------------------------

if user_message:
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        try:
            with st.spinner("NOVA is thinking..."):
                # Retrieve sources for the interface.
                sources = retrieve_sources(
                    user_message,
                    top_k=3,
                )

                # Generate a grounded response with local Ollama.
                response = st.write_stream(
                    generate_response(st.session_state.messages)
                )

                if not isinstance(response, str):
                    response = str(response)

            if sources:
                display_sources(sources)

        except Exception as error:
            response = (
                "I couldn't generate a response. Please check that "
                "Ollama is running and that llama3.2:3b is installed."
            )

            sources = []

            st.error(response)
            st.caption(f"Technical details: {error}")

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    assistant_index = len(st.session_state.messages) - 1

    st.session_state.message_sources[assistant_index] = sources