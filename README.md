# NOVA — Local AI Assistant with RAG

**A privacy-focused, document-aware AI assistant powered by a local Large Language Model (LLM).**

NOVA lets users ask questions about PDF documents and receive answers based on relevant document passages, with source references where available. It uses Retrieval-Augmented Generation (RAG) to connect document search with AI-generated responses.

## ✨ Features

* **Local LLM:** Uses Ollama with the `llama3.2:3b` model.
* **PDF processing:** Extracts text from PDF documents while preserving page numbers.
* **Smart chunking:** Splits document text into smaller, overlapping chunks.
* **Semantic search:** Uses sentence-transformer embeddings to find relevant passages.
* **Vector database:** Stores and searches document embeddings with ChromaDB.
* **Source-aware answers:** Supplies retrieved passages and source metadata to the language model.
* **Interactive interface:** Provides a Streamlit chat interface for asking questions.
* **Automated tests:** Tests document processing, retrieval, and LLM integration using mocks.

## 🏗️ Architecture

```text
             User
              |
              v
       Streamlit Chat UI
              |
              v
        User Question
              |
              v
      Sentence Embeddings
              |
              v
       ChromaDB Search
              |
              v
      Relevant PDF Chunks
              |
              v
        Local Ollama LLM
              |
              v
     Answer with Source Labels
```

### Document indexing workflow

```text
PDF Documents
     |
     v
Extract Text and Page Numbers
     |
     v
Split Text into Chunks
     |
     v
Generate Embeddings
     |
     v
Store in ChromaDB
```

## 🛠️ Technology Stack

| Technology            | Purpose                               |
| --------------------- | ------------------------------------- |
| Python                | Core application                      |
| Streamlit             | Chat interface                        |
| Ollama                | Runs the local language model         |
| Llama 3.2 3B          | Generates responses                   |
| Sentence Transformers | Creates text embeddings               |
| ChromaDB              | Vector storage and semantic retrieval |
| PyPDF                 | PDF text extraction                   |
| Pytest                | Automated testing                     |

## 📁 Project Structure

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
├── data/
│   ├── documents/       # Local PDF files (not committed)
│   └── chroma_db/       # Local vector database (not committed)
├── tests/
│   ├── test_document_processor.py
│   ├── test_vector_store.py
│   └── test_llm.py
├── reindex_documents.py
├── pytest.ini
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

* Python 3.11
* Git
* Ollama for Windows
* Sufficient memory and disk space for the local models

### 1. Clone the repository

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
cd nova-ai-assistant
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's URL.

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```powershell
python -m pip install streamlit chromadb sentence-transformers pypdf ollama pytest
```

### 4. Start Ollama

Install Ollama from its official website and open the Ollama application. Then download the model:

```powershell
ollama pull llama3.2:3b
```

Verify that the model is available:

```powershell
ollama list
```

### 5. Add your own PDF documents

Place PDF files you own or have permission to use inside:

```text
data/documents/
```

### 6. Index the documents

```powershell
python reindex_documents.py
```

### 7. Launch NOVA

```powershell
python -m streamlit run app/frontend/chat_ui.py
```

Open the local address displayed in the terminal.

> These instructions assume the project dependencies and Ollama are installed correctly. The repository's setup may need additional adjustments if dependency versions or application imports change.

## 🧪 Run Automated Tests

Run the test suite:

```powershell
python -m pytest
```

**Current development result:** 15 tests passed.

The tests cover document chunking, page metadata, retrieval behavior, relevance filtering, and LLM response handling.

## 🔒 Privacy and Security

* The language model runs locally through Ollama.
* PDF documents and the local vector database are excluded from Git using `.gitignore`.
* No hosted LLM API key is required for the intended local workflow.
* The embedding model may download from Hugging Face the first time it is used.
* Local execution does not automatically guarantee that every component is offline; model downloads and dependency installation may require internet access.

## 🔮 Future Improvements

* Add a dependency lock file for reproducible installations.
* Improve answer quality with retrieval evaluation and reranking.
* Add document deletion and re-indexing controls to the interface.
* Add conversation memory and document filtering.
* Measure retrieval precision, answer quality, latency, and resource usage.
* Package the application with Docker where supported.
* Add screenshots, a demo video, and a deployment guide.

## 👨‍💻 Project Goal

NOVA is a learning and portfolio project demonstrating practical skills in Generative AI, Retrieval-Augmented Generation, semantic search, vector databases, local LLM integration, and automated testing.

**Built to explore private, locally executed AI applications.**
