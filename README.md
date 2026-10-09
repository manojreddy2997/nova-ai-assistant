# NOVA AI Assistant

**A local-first, RAG-powered document question-answering assistant.**

NOVA helps users ask questions about PDF documents and retrieve relevant information using semantic search and a locally running language model. The goal is to keep document processing and language-model inference on the user's machine.

## Architecture

![NOVA AI Assistant Architecture](assets/nova-architecture.png)

### How It Works

1. **Document ingestion:** Extract text from PDF documents.
2. **Text chunking:** Split document text into smaller segments and retain relevant metadata.
3. **Embedding generation:** Convert text into vector representations using Sentence Transformers.
4. **Vector storage:** Store embeddings and searchable document information in ChromaDB.
5. **Semantic retrieval:** Find document chunks relevant to the user's question.
6. **Answer generation:** Pass retrieved context to a local Ollama model.
7. **Grounded response:** Return an answer based on retrieved context, with source information where available.

## Features

- PDF document processing
- Text chunking and metadata handling
- Semantic search using embeddings
- Vector storage and retrieval with ChromaDB
- Local language-model integration through Ollama
- Source-aware question answering
- Streamlit chat interface
- Automated tests with Pytest

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | User interface |
| Sentence Transformers | Text embeddings |
| ChromaDB | Vector storage and retrieval |
| Ollama | Local language-model inference |
| PyPDF | PDF text extraction |
| Pytest | Automated testing |
| Git and GitHub | Version control and project hosting |

## Project Structure

```text
nova-ai-assistant/
├── app/
│   ├── backend/
│   │   ├── document_processor.py
│   │   ├── embeddings.py
│   │   ├── llm.py
│   │   └── vector_store.py
│   └── frontend/
│       └── chat_ui.py
├── assets/
│   └── nova-architecture.png
├── data/
│   ├── documents/
│   └── chroma_db/
├── tests/
├── reindex_documents.py
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 recommended
- Git
- Ollama installed locally
- An Ollama model compatible with your application

### 1. Clone the repository

```bash
git clone https://github.com/manojreddy2997/nova-ai-assistant.git
cd nova-ai-assistant
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Set up Ollama

Install Ollama for your operating system, then download a supported model:

```bash
ollama pull llama3.2:3b
```

Ensure the Ollama service is running and that the model name matches your application configuration.

### 5. Add PDF documents

Place the PDF files you want to search in:

```text
data/documents/
```

### 6. Index your documents

```bash
python reindex_documents.py
```

### 7. Launch NOVA

```bash
streamlit run app/frontend/chat_ui.py
```

Open the local address shown in the terminal.

## Run Tests

Run the project's automated tests with:

```bash
python -m pytest -v
```

## Privacy and Limitations

- The project is designed for local document processing and local LLM inference.
- Keep documents and generated database files out of version control when they contain private information.
- Answer quality depends on document quality, retrieval accuracy, and the selected model.
- Scanned PDFs may require OCR.
- Local model performance depends on available memory and hardware.
- Verify answers against their source documents, especially for important decisions.

## Future Improvements

- Hybrid search and reranking
- Retrieval-quality evaluation
- Improved source citations
- Conversation history and document management
- Authentication and access control
- Response latency and resource monitoring

## Skills Demonstrated

- Retrieval-Augmented Generation (RAG)
- Document ingestion and text chunking
- Embeddings and semantic retrieval
- Vector databases
- Local LLM integration
- Python application development
- Automated testing
- Git and GitHub workflows

## Author

**Manoj Reddy**

GitHub: [@manojreddy2997](https://github.com/manojreddy2997)

---

*An ongoing Generative AI portfolio project.*
