# 🧠 Enterprise Knowledge & Action Assistant

An AI-powered enterprise knowledge and action assistant that allows employees to ask questions about internal company policies and documents using natural language.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from company documents and provide it as context to an LLM before generating a grounded answer.

It also includes authentication, protected APIs, document upload, document indexing, conversational sessions, and IT support tool calling.

---

## 🚀 Project Overview

In an organization, employees often need to search through policies, guidelines, and internal documentation to find specific information.

The **Enterprise Knowledge & Action Assistant** provides a conversational way to interact with this information.

Instead of manually searching through documents, users can ask questions such as:

* What is the work-from-home policy?
* Who is eligible for remote work?
* How many days of remote work are allowed?
* Who approves a work-from-home request?
* How many annual leaves does a confirmed employee receive?
* Can annual leave be carried forward?

The assistant retrieves relevant information from the knowledge base and uses it as context for generating an answer.

The application also supports action-oriented workflows such as creating and checking IT support tickets using LLM tool calling.

---

## 🎯 Problem Statement

Traditional document-based knowledge systems require employees to manually search through large amounts of information.

This project explores how **Generative AI, Retrieval-Augmented Generation, semantic search, and tool calling** can provide a more natural way of accessing enterprise knowledge and performing simple business actions.

The goal is to allow users to ask questions in everyday language while keeping generated answers grounded in the available documentation.

---

## ⭐ Key Highlights

* Built an end-to-end **RAG-based enterprise knowledge assistant**
* Implemented document loading and processing
* Implemented text chunking
* Generated OpenAI embeddings
* Implemented semantic retrieval using **FAISS**
* Integrated an LLM for context-aware answer generation
* Added grounded responses with automatic source information
* Implemented conversational history
* Implemented LLM tool calling
* Added mock IT ticket creation and lookup
* Implemented user registration and login
* Added password hashing
* Added JWT-based authentication
* Added protected API endpoints
* Added document upload and indexing
* Added SQLite for application data
* Added a conversational Gradio interface
* Configured sensitive credentials through environment variables
* Added hallucination-control behavior for unsupported questions

---

# 🧠 How It Works

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
                     FAISS Index
                           │
                           │
User Question ─────────────┤
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

For action-oriented requests, the system can also use tools:

```text
User Request
     │
     ▼
     LLM
     │
     ├──────────────► Knowledge Retrieval
     │
     └──────────────► Tool Calling
                           │
                           ▼
                    IT Support Tools
                           │
                           ▼
                    Tool Result
                           │
                           ▼
                    Assistant Response
```

---

# ✨ Features

## 🔎 Knowledge Retrieval

* Natural-language question answering
* Semantic document search
* Retrieval-Augmented Generation
* Context-aware responses
* Vector similarity search
* Grounded answers
* Source information for retrieved chunks
* "I don't know" behavior when information is unavailable

## 📄 Document Management

* Document loading
* Text extraction
* Text chunking
* Embedding generation
* FAISS indexing
* Document upload
* Automatic document indexing
* PDF and DOCX support through the API

## 💬 Conversation

* Multi-turn conversations
* Session-based conversation history
* Follow-up questions
* Context-aware responses

## 🤖 Tool Calling

The assistant can interact with mock enterprise tools.

Current IT support tools include:

* Create IT ticket
* Get IT ticket
* List IT tickets

Example:

```text
User:
Create an IT ticket. My laptop is not connecting to VPN.

Assistant:
IT ticket created successfully.
Ticket ID: IT-0001
Issue: Laptop is not connecting to VPN
Priority: high
Status: Open
```

The assistant can also retrieve an existing ticket:

```text
User:
What is the status of IT-0001?

Assistant:
Ticket found.
Ticket ID: IT-0001
Issue: Laptop is not connecting to VPN
Priority: high
Status: Open
```

## 🔐 Authentication

* User registration
* User login
* Password hashing
* JWT access tokens
* Token validation
* Protected API endpoints

## 🌐 API

The project uses FastAPI for backend API development.

Available endpoints include:

```text
GET  /
GET  /health
POST /register
POST /login
POST /chat
POST /upload
```

## 🖥️ User Interface

The project includes a conversational Gradio interface for interacting with the assistant.

---

# 🛠️ Tech Stack

| Technology        | Purpose                      |
| ----------------- | ---------------------------- |
| **Python**        | Application development      |
| **FastAPI**       | Backend API                  |
| **OpenAI API**    | Embeddings and LLM responses |
| **FAISS**         | Vector similarity search     |
| **Gradio**        | User interface               |
| **SQLite**        | Local application database   |
| **Pydantic**      | Data validation              |
| **python-dotenv** | Environment configuration    |
| **PyPDF**         | PDF processing               |
| **python-docx**   | DOCX processing              |
| **Git & GitHub**  | Version control              |

---

# 📂 Project Structure

```text
enterprise-knowledge-assistant/
│
├── app/
│   ├── assistant.py
│   ├── answer.py
│   ├── auth.py
│   ├── chunk_document.py
│   ├── conversation.py
│   ├── database.py
│   ├── document_loader.py
│   ├── embed_and_store.py
│   ├── gradio_app.py
│   ├── index_documents.py
│   ├── main.py
│   ├── retrieve.py
│   ├── tool_agent.py
│   └── tools.py
│
├── data/
│   ├── documents/
│   │   ├── hr/
│   │   ├── it/
│   │   ├── finance/
│   │   └── general/
│   │
│   └── vector_store/
│       ├── company_knowledge.index
│       └── chunks.json
│
├── assets/
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

> Local environment files, API keys, databases, generated vector indexes, and other sensitive or unnecessary files should not be committed to GitHub.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/TauqeerHusain/enterprise-knowledge-assistant.git
```

```bash
cd enterprise-knowledge-assistant
```

---

# 2. Create Virtual Environment

## Windows

```bash
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\activate
```

After activation, the terminal should show:

```text
(.venv)
```

at the beginning of the command prompt.

Verify Python:

```bash
python --version
```

Verify the active Python executable:

```bash
where python
```

The Python path should point to the project's `.venv` directory.

---

## Existing `.venv312` Environment

During development, a Python 3.12 environment named `.venv312` was also used.

To activate it on Windows:

```powershell
.venv312\Scripts\activate
```

However, for a fresh installation, `.venv` is the recommended environment.

---

# 3. Install Dependencies

After activating the virtual environment:

```bash
pip install -r requirements.txt
```

If FastAPI and Uvicorn are not already included in `requirements.txt`, install them with:

```bash
pip install fastapi uvicorn
```

---

# 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

Never commit the real API key to GitHub.

The `.gitignore` file should include:

```text
.env
.venv
.venv312
__pycache__
```

---

# 🗂️ Knowledge Base

The project uses **fictional internal-style company documentation** as its knowledge source.

The current knowledge base contains documents covering areas such as:

### HR

* Annual leave
* Sick leave
* Work from home
* Hybrid working
* Attendance

### IT

* Laptop policy
* Password policy
* VPN policy
* IT support

### Finance

* Expense policy
* Travel policy
* Reimbursement policy

### General

* Working hours
* Holidays

The documents are processed, chunked, embedded, and indexed for semantic retrieval.

---

# 🔍 RAG Pipeline

## 1. Document Loading

Company documentation is loaded from the `data/documents/` directory.

## 2. Text Chunking

Large documents are divided into smaller chunks.

This makes semantic retrieval more efficient.

## 3. Embedding Generation

Each chunk is converted into a numerical vector using:

```text
text-embedding-3-small
```

## 4. Vector Indexing

The embeddings are stored in a **FAISS index**.

The generated vector store contains:

```text
data/vector_store/
├── company_knowledge.index
└── chunks.json
```

## 5. User Query

The user submits a natural-language question.

## 6. Query Embedding

The question is converted into an embedding using the same embedding model.

## 7. Similarity Search

FAISS searches for the most relevant document chunks.

## 8. Context Retrieval

The retrieved chunks are provided to the LLM as context.

## 9. Answer Generation

The LLM generates a response using the retrieved company information.

---

# 🛡️ Hallucination Control

The assistant is designed to answer questions using the available company documentation.

The prompt instructs the model not to invent information.

When the available documents do not contain the requested information, the assistant can respond:

```text
I don't know based on the available company documents.
```

This helps reduce unsupported answers in enterprise knowledge scenarios.

---

# 🤖 Tool Calling

The project also demonstrates LLM function/tool calling.

The assistant can select an appropriate tool based on the user's request.

Available tools:

```text
create_it_ticket
get_ticket
list_tickets
```

Example:

```text
User:
Create an IT ticket. My laptop is not connecting to VPN.
```

The LLM can select:

```text
create_it_ticket
```

The Python application executes the function and returns the result.

This demonstrates the basic architecture used by AI agents to interact with external systems.

---

# ▶️ Running the Application

## Run FastAPI

Make sure the virtual environment is activated:

```powershell
.venv\Scripts\activate
```

The FastAPI application is located at:

```text
app/main.py
```

Run it from the project root:

```bash
python -m uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Run FastAPI on Port 8001

If the frontend or another application is configured to use port `8001`, run:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

The API will then be available at:

```text
http://127.0.0.1:8001
```

Swagger:

```text
http://127.0.0.1:8001/docs
```

---

# 🖥️ Run Gradio

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

Then run:

```bash
python -m app.gradio_app
```

If using the Python 3.12 environment:

```powershell
.venv312\Scripts\python.exe -m app.gradio_app
```

Gradio will normally start at:

```text
http://127.0.0.1:7860
```

---

# 🔑 Authentication Flow

The application supports:

```text
Register
   │
   ▼
Username + Password
   │
   ▼
Password Hashing
   │
   ▼
SQLite Database
```

For login:

```text
Username + Password
        │
        ▼
Password Verification
        │
        ▼
JWT Access Token
        │
        ▼
Protected API Requests
```

Protected endpoints require a valid bearer token.

---

# 📡 API Examples

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

## Register

```http
POST /register
```

Example:

```json
{
  "username": "employee1",
  "password": "password123"
}
```

## Login

```http
POST /login
```

Example:

```json
{
  "username": "employee1",
  "password": "password123"
}
```

The API returns an access token.

## Chat

```http
POST /chat
```

Example:

```json
{
  "question": "How many annual leaves does a confirmed employee get?",
  "session_id": "default"
}
```

## Document Upload

```http
POST /upload
```

Supported document types:

```text
.pdf
.docx
```

The uploaded document is saved and then indexed.

---

# 💡 Example Questions

Try questions such as:

```text
What is the company's work-from-home policy?
```

```text
Who can request remote work?
```

```text
How many WFH days are allowed for confirmed employees?
```

```text
What security requirements apply when working from home?
```

```text
How many annual leaves does a confirmed employee get?
```

```text
Can I carry forward my annual leave?
```

```text
What is the company's dress code?
```

For information that is not available in the knowledge base, the assistant is designed to avoid confidently inventing an answer.

---

# 🎯 Learning Objectives

This project demonstrates practical experience with:

* Large Language Models
* Generative AI
* Retrieval-Augmented Generation
* Embeddings
* Vector similarity search
* FAISS
* Semantic search
* Prompt engineering
* Document processing
* Text chunking
* Context retrieval
* Conversation history
* LLM tool calling
* AI agents
* FastAPI
* REST APIs
* JWT authentication
* Password hashing
* SQLite
* Gradio
* Environment variables
* AI application development
* Enterprise knowledge systems

---

# 🔮 Future Improvements

Possible future improvements include:

* Persistent IT ticket storage
* Pushover notifications
* More enterprise tools
* Role-based access control
* Hybrid search
* Reranking
* Retrieval evaluation
* Automated RAG evaluation
* Document version management
* User feedback
* Cloud deployment
* Monitoring and observability
* Production vector database
* Better citation formatting
* Streaming responses

---

# 👨‍💻 Author

**Tauqeer Husain**

Aspiring AI / LLM Engineer

This project was developed as a hands-on project to demonstrate practical skills in Generative AI, Retrieval-Augmented Generation, LLM applications, API development, authentication, semantic search, and AI engineering.

---

# 📌 Disclaimer

The company, employees, policies, and documents used in this project are **fictional** and were created for demonstration and learning purposes.

They do not represent a real company's internal policies, confidential information, or proprietary documentation.
