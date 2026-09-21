# 🧠 Enterprise Knowledge Assistant

An AI-powered enterprise knowledge assistant that allows employees to ask questions about internal company policies and documents using natural language.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from company documents and provide it as context to a Large Language Model (LLM) before generating an answer.

---

## 🚀 Project Overview

In an organization, employees often need to search through policies, guidelines, and internal documentation to find specific information.

The **Enterprise Knowledge Assistant** provides a conversational way to interact with this information.

Instead of manually searching through documents, users can ask questions such as:

* What is the work-from-home policy?
* Who is eligible for remote work?
* How many days of remote work are allowed?
* Who approves a work-from-home request?
* What are the hybrid working requirements?
* What security requirements apply when working remotely?

The system retrieves relevant sections from the knowledge base and uses them as context for generating an answer.

---

## 🎯 Problem Statement

Traditional document-based knowledge systems require employees to manually search through large amounts of information.

This project explores how **Generative AI and Retrieval-Augmented Generation (RAG)** can provide a more natural way of accessing enterprise knowledge.

The goal is to allow users to ask questions in everyday language while keeping generated answers grounded in the available documentation.

---

## ⭐ Key Highlights

* Built an end-to-end **RAG-based enterprise knowledge assistant**
* Implemented document processing and text chunking
* Generated embeddings for semantic retrieval
* Used **ChromaDB** for vector-based search
* Integrated an LLM for context-aware answer generation
* Built a conversational **Gradio interface**
* Implemented user authentication
* Added protected API endpoints
* Added document upload and indexing functionality
* Used SQLite for local application data
* Configured sensitive credentials through environment variables
* Designed responses to remain grounded in retrieved documentation

---

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation workflow:

```text
                  Company Documents
                         │
                         ▼
                  Document Processing
                         │
                         ▼
                    Text Chunking
                         │
                         ▼
                     Embeddings
                         │
                         ▼
                  Vector Database
                         │
                         │
  User Question ─────────┤
                         ▼
                  Similarity Search
                         │
                         ▼
                Relevant Document Chunks
                         │
                         ▼
                       LLM
                         │
                         ▼
                  Grounded Answer
```

The retrieval step provides relevant information from the knowledge base to the LLM, helping the application generate answers based on the available documentation.

---

## ✨ Features

### 🔎 Knowledge Retrieval

* Natural-language question answering
* Semantic document search
* Retrieval-Augmented Generation
* Context-aware responses
* Vector similarity search

### 📄 Document Management

* Document upload
* Document processing
* Text chunking
* Document indexing
* Embedding generation

### 🔐 Authentication

* User registration
* User login
* Password hashing
* Token-based authentication
* Protected API endpoints

### 💬 User Interface

* Conversational Gradio interface
* Simple natural-language interaction
* Knowledge-base question answering

---

## 🛠️ Tech Stack

| Technology        | Purpose                              |
| ----------------- | ------------------------------------ |
| **Python**        | Application development              |
| **FastAPI**       | Backend API                          |
| **LangChain**     | RAG and LLM workflow                 |
| **LLM API**       | Answer generation                    |
| **Embeddings**    | Semantic representation of documents |
| **ChromaDB**      | Vector storage and similarity search |
| **SQLite**        | Local application data               |
| **Gradio**        | User interface                       |
| **Pydantic**      | Data validation                      |
| **Python-dotenv** | Environment configuration            |
| **Git & GitHub**  | Version control                      |

---

## 📂 Project Structure

```text
enterprise-knowledge-assistant/
│
├── app/
│   ├── assistant.py
│   ├── auth.py
│   ├── database.py
│   ├── gradio_app.py
│   ├── index_documents.py
│   └── ...
│
├── data/
│   └── Local project data
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

> Local environment files, API keys, databases, generated files, and other unnecessary files should not be committed to GitHub.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/TauqeerHusain/enterprise-knowledge-assistant.git
```

```bash
cd enterprise-knowledge-assistant
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root and add the API credentials required by the application.

For example:

```env
OPENAI_API_KEY=your_api_key_here
```

> The exact environment variables depend on the LLM and services configured in the application.

**Never commit API keys or `.env` files to GitHub.**

---

## ▶️ Running the Application

After installing the dependencies and configuring the required environment variables, run:

```bash
python -m app.gradio_app
```

The Gradio interface will start locally.

Open the local URL shown in the terminal, typically:

```text
http://127.0.0.1:7860
```

### Windows

If you already have a virtual environment named `.venv312`, you can also run:

```powershell
.venv312\Scripts\python.exe -m app.gradio_app
```

For other users, the recommended command is:

```bash
python -m app.gradio_app
```

---

## 📚 Knowledge Base

The project uses **fictional internal-style company documentation** as its knowledge source.

Example:

**NovaTech Solutions — Work From Home and Hybrid Working Policy**

The policy contains information related to:

* Employee eligibility
* Remote-work guidelines
* Hybrid working
* Employee responsibilities
* Manager responsibilities
* Security requirements
* Attendance expectations
* Exceptions and approvals

The documents are processed and indexed so that the RAG pipeline can retrieve relevant information when answering questions.

---

## 🔍 RAG Pipeline

### 1. Document Processing

Company documentation is loaded and prepared for the application.

### 2. Text Chunking

Large documents are divided into smaller chunks so relevant sections can be retrieved efficiently.

### 3. Embedding Generation

Each document chunk is converted into a numerical vector representation using an embedding model.

### 4. Vector Storage

The generated embeddings are stored in **ChromaDB**.

### 5. User Query

The user submits a natural-language question through the application.

### 6. Query Embedding

The question is converted into an embedding representation.

### 7. Similarity Search

The vector database is searched for document chunks that are semantically relevant to the question.

### 8. Context Retrieval

Relevant document information is provided to the LLM as context.

### 9. Answer Generation

The LLM generates a response using the retrieved context.

---

## 🛡️ Hallucination Control

The assistant is designed to ground its answers in information retrieved from the available knowledge base.

When the required information is not available in the retrieved documentation, the application is designed to indicate that sufficient information was not found rather than confidently providing unsupported information.

This approach helps improve reliability for enterprise knowledge-based question answering.

---

## 💡 Example Questions

Try questions such as:

```text
What is the company's work-from-home policy?
```

```text
Who can request remote work?
```

```text
What are the employee responsibilities while working remotely?
```

```text
What security requirements apply when working from home?
```

```text
What is the process for requesting an exception?
```

The assistant retrieves relevant information from the knowledge base before generating its response.

---

## 🎯 Learning Objectives

This project demonstrates practical experience with:

* Large Language Models (LLMs)
* Generative AI
* Retrieval-Augmented Generation (RAG)
* Embeddings
* Vector databases
* Semantic search
* Prompt engineering
* Document processing
* Context retrieval
* API development
* Authentication
* AI application development
* LLM-powered question answering

---

## 🔮 Future Improvements

Possible future improvements include:

* Multi-document support
* Source citations in responses
* Conversation history
* Role-based access control
* Hybrid search
* Reranking
* Retrieval evaluation
* Document version management
* User feedback
* Cloud deployment
* Monitoring and observability

---

## 👨‍💻 Author

**Tauqeer Husain**

Aspiring AI / LLM Engineer

This project was developed as a hands-on project to demonstrate practical skills in Generative AI, Retrieval-Augmented Generation, LLM applications, API development, authentication, and AI engineering.

---

## 📌 Disclaimer

The company, employees, policies, and documents used in this project are **fictional** and were created for demonstration and learning purposes.

They do not represent a real company's internal policies, confidential information, or proprietary documentation.
