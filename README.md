# NOVA AI Assistant 🤖

**A local-first AI assistant that answers questions from your documents using Retrieval-Augmented Generation (RAG).**

NOVA helps users upload and index knowledge documents, retrieve relevant information, and generate answers grounded in the retrieved context.

## ✨ Features

* **Document processing:** Extract text from PDF documents, page by page.
* **Smart chunking:** Split documents into smaller, searchable text segments.
* **Semantic search:** Use sentence embeddings to find relevant content by meaning.
* **Vector database:** Store and search document embeddings using ChromaDB.
* **Local LLM integration:** Generate answers using Ollama and a locally running language model.
* **Source-aware answers:** Include document and page information in retrieved context.
* **Interactive chat interface:** Ask questions through a Streamlit application.
* **Automated tests:** Test important components of the application.

## 🏗️ Architecture

```text
                 User Question
                       |
                       v
              Streamlit Chat UI
                       |
                       v
                RAG Application
                       |
                       v
              Semantic Retrieval
                       |
                       v
                 ChromaDB
                       |
                       v
            Relevant Document Chunks
                       |
                       v
             Local Ollama LLM
                       |
                       v
              Grounded Answer
```

### Document indexing workflow

```text
PDF Documents
      |
      v
Text Extraction
      |
      v
Text Chunking + Metadata
      |
      v
Embedding Model
      |
      v
ChromaDB Vector Store
```

## 🧰 Technology Stack

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| Python                | Core application             |
| Streamlit             | Chat interface               |
| Sentence Transformers | Text embeddings              |
| ChromaDB              | Vector storage and retrieval |
| Ollama                | Local LLM inference          |
| PyPDF                 | PDF text extraction          |
| Pytest                | Automated testing            |

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
│   ├── documents/
│   └── chroma_db/
├── tests/
│   ├── test_document_processor.py
│   ├── test_vector_store.py
│   └── test_llm.py
├── reindex_documents.py
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

* Python 3.11 recommended
* Git
* Ollama installed and running locally
* A compatible Ollama model, such as `llama3.2:3b`

### 1. Clone the repository

```bash
git clone https://github.com/manojreddy2997/nova-ai-assistant.git
cd nova-ai-assistant
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS or Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Download the local language model

After installing Ollama, run:

```bash
ollama pull llama3.2:3b
```

Make sure the Ollama service is running before using the chat application.

### 5. Add your documents

Place the PDF files you want to search in:

```text
data/documents/
```

### 6. Index the documents

```bash
python reindex_documents.py
```

### 7. Start NOVA

```bash
streamlit run app/frontend/chat_ui.py
```

Open the local URL printed in your terminal.

## 🧪 Run Tests

```bash
python -m pytest -v
```

## 🔐 Privacy

NOVA is designed for local document processing and local LLM inference. When configured to use a local Ollama service and local embedding model, document content can remain on your computer.

Actual privacy depends on the models, dependencies, and services you configure. Avoid committing confidential documents, credentials, virtual environments, or local vector database files to GitHub.

## ⚠️ Current Limitations

* Answer quality depends on document quality, retrieval results, and the selected language model.
* Scanned PDFs may require OCR before their text can be searched.
* Local inference performance depends on available hardware and model size.
* A cloud-hosted interface cannot automatically access Ollama running on your personal computer.

## 🛣️ Future Improvements

* Add support for more document formats.
* Improve retrieval evaluation and source citations.
* Add conversation history and document management.
* Introduce hybrid search and reranking.
* Add authentication and access controls.
* Add performance and retrieval-quality evaluations.

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

* Retrieval-Augmented Generation (RAG)
* Text extraction and chunking
* Embeddings and semantic search
* Vector databases
* Local language model integration
* Python application structure
* Automated testing
* Git and GitHub project documentation

## 👨‍💻 Author

**Manoj Reddy**

GitHub: [@manojreddy2997](https://github.com/manojreddy2997)

---

*Built as a hands-on Generative AI portfolio project.*
