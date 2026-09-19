# 🤖 AI Document Assistant

> An AI-powered document question-answering system that allows users to upload PDF documents, retrieve relevant information, and interact with their documents using Retrieval-Augmented Generation (RAG) and a local Llama 3.2 model.

**FastAPI** • **Python** • **RAG** • **NLP** • **Generative AI** • **Ollama** • **Llama 3.2** • **PyMuPDF** • **Tesseract OCR** • **NumPy**

---

## 📖 Overview

AI Document Assistant is an AI-powered document question-answering application that allows users to upload PDF documents and interact with their content using natural-language questions.

The system extracts text from uploaded PDF documents using PyMuPDF and uses Tesseract OCR as a fallback for scanned pages. The extracted content is divided into smaller chunks, relevant document context is retrieved, and the context is provided to a local Llama 3.2 Large Language Model through Ollama.

The application follows a Retrieval-Augmented Generation (RAG) architecture and supports conversation memory, follow-up questions, source-page tracking, and a browser-based interface.

The project demonstrates practical AI Product Development using Python, FastAPI, document processing, OCR, information retrieval, RAG, and local Generative AI.

---

## 🎯 Problem Statement

Large PDF documents can be difficult and time-consuming to search manually. Users often need to locate specific information quickly without reading the entire document.

This project provides a conversational AI interface that allows users to:

- Upload PDF documents
- Ask questions in natural language
- Retrieve relevant document information
- Receive AI-generated answers
- Ask follow-up questions
- Track source pages
- Interact with documents conversationally

---

## 💡 Solution

The system combines PDF processing, OCR, document chunking, context retrieval, and local LLM inference.

```text
PDF Document
     ↓
Text Extraction
     ↓
OCR Fallback
     ↓
Text Chunking
     ↓
Context Retrieval
     ↓
Relevant Document Chunks
     ↓
RAG Context
     ↓
Llama 3.2 via Ollama
     ↓
AI Generated Answer
     ↓
Source Pages
```

---

## ✨ Features

### 📄 PDF Document Upload

- Upload PDF documents
- Process documents page by page
- Store uploaded documents locally
- Extract text from PDF files
- Support scanned pages through OCR
- Track original page numbers

### 🔍 Document Processing

- Page-by-page PDF processing
- Text extraction using PyMuPDF
- OCR fallback using Tesseract
- Text preprocessing
- Document chunking
- Chunk overlap
- Page-aware chunk storage

### 🧠 Retrieval-Augmented Generation

- Retrieve relevant document content
- Build context from retrieved chunks
- Pass retrieved context to Llama 3.2
- Generate document-grounded answers
- Support follow-up questions
- Track source pages

### 🤖 Generative AI

- Local LLM inference
- Ollama integration
- Llama 3.2 integration
- Natural-language question answering
- Context-aware responses
- Local AI execution
- No paid AI API required

### 💬 Conversation Memory

- Maintain recent conversation history
- Store previous questions
- Store previous AI answers
- Support follow-up questions
- Include relevant previous conversation in prompts
- Clear chat history

### 📚 Source Page Tracking

- Track source PDF pages
- Associate chunks with page numbers
- Return source pages with answers
- Improve transparency of retrieved information

### 🌐 Web Interface

- Browser-based interface
- PDF upload
- Question input
- AI response display
- Source information
- Conversation interaction
- Clear chat functionality

### ⚡ FastAPI Backend

- REST API architecture
- PDF upload endpoint
- Question-answering endpoint
- Chat management
- Swagger documentation
- CORS support
- Local development server

---

## 🏗️ System Architecture

```text
┌───────────────────────────────────────────────┐
│                 Web Frontend                  │
│              HTML / CSS / JavaScript          │
└───────────────────────┬───────────────────────┘
                        │
                        │ REST API
                        ▼
┌───────────────────────────────────────────────┐
│                 FastAPI Backend               │
│                    Python                     │
└───────────────────────┬───────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
┌────────────────┐ ┌────────────┐ ┌──────────────┐
│ PDF Processing │ │ Document   │ │ Conversation │
│                │ │ Retrieval  │ │ Memory       │
└───────┬────────┘ └─────┬──────┘ └──────────────┘
        │                │
        ▼                ▼
┌───────────────┐ ┌────────────────────┐
│   PyMuPDF     │ │ Context Retrieval  │
└───────┬───────┘ └─────────┬──────────┘
        │                    │
        ▼                    ▼
┌───────────────┐     Relevant Chunks
│ Tesseract OCR │             │
└───────┬───────┘             ▼
        │              ┌──────────────┐
        └─────────────►│ RAG Context  │
                       └──────┬───────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Ollama           │
                    │ Llama 3.2        │
                    └────────┬─────────┘
                             │
                             ▼
                       AI Response
                             │
                             ▼
                       Source Pages
```

---

## 🛠️ Technology Stack

### Backend

-  Python 
-  FastAPI 
-  Uvicorn 
-  Requests 

### AI / Generative AI

-  Ollama 
-  Llama 3.2 
-  Retrieval-Augmented Generation (RAG) 
-  Natural Language Processing 
-  Local LLM inference 

### Document Processing

-  PyMuPDF 
-  Tesseract OCR 
-  Pillow 

### Data Processing

-  NumPy 
-  Python text processing 
-  Document chunking 
-  Context retrieval 
-  Word-overlap relevance matching 

### Frontend

-  HTML 
-  CSS 
-  JavaScript 

### API

-  REST API 
-  FastAPI 
-  Swagger / OpenAPI 

---

## 📁 Project Structure

```
```

```
AI-Document-Assistant/
│
├── Backend/
│   └── main.py
│
├── Database/
│
├── Document/
│
├── Frontend/
│   └── index.html
│
├── venv/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔄 Application Workflow

```
```

```
1. Upload PDF Document
        ↓
2. Save Uploaded Document
        ↓
3. Open PDF using PyMuPDF
        ↓
4. Extract Text Page by Page
        ↓
5. Detect Scanned Pages
        ↓
6. Apply Tesseract OCR if Required
        ↓
7. Combine Extracted Text
        ↓
8. Split Document into Chunks
        ↓
9. Track Source Page Numbers
        ↓
10. User Asks a Question
        ↓
11. Process Question
        ↓
12. Retrieve Relevant Document Chunks
        ↓
13. Build RAG Context
        ↓
14. Include Previous Conversation
        ↓
15. Send Context to Llama 3.2
        ↓
16. Generate AI Answer
        ↓
17. Store Conversation
        ↓
18. Return Answer + Source Pages
```

---

## 🧠 Retrieval-Augmented Generation

The application follows a Retrieval-Augmented Generation architecture.

Instead of directly asking the language model to answer a question, the system first retrieves relevant information from the uploaded document.

The retrieved document content is then provided to Llama 3.2 as context.

```
```

```
User Question
      │
      ▼
Question Processing
      │
      ▼
Document Retrieval
      │
      ▼
Relevant Chunks
      │
      ▼
RAG Context
      │
      ▼
Previous Conversation
      │
      ▼
Llama 3.2
      │
      ▼
Generated Answer
```

This approach allows the application to generate responses based on the uploaded document rather than relying only on the model's general knowledge.

---

## 📄 Document Processing Pipeline

The document processing pipeline handles both normal PDFs and scanned PDF pages.

```
```

```
PDF Upload
    │
    ▼
PyMuPDF
    │
    ├───────────────► Text Available
    │                       │
    │                       ▼
    │                 Extract Text
    │
    └───────────────► No Text
                            │
                            ▼
                       Tesseract OCR
                            │
                            ▼
                       Extract Text
                            │
                            ▼
                     Text Combination
                            │
                            ▼
                       Text Chunking
                            │
                            ▼
                    Page Number Tracking
```

### PyMuPDF

PyMuPDF is used to open PDF files and extract text page by page.

### Tesseract OCR

Tesseract is used as a fallback when a PDF page does not contain directly extractable text.

This provides basic support for scanned documents.

---

## ✂️ Document Chunking

Large documents are divided into smaller text chunks before retrieval.

The current implementation uses:

```
```

```
Chunk Size: 500 characters
Chunk Overlap: 100 characters
```

The overlap helps preserve contextual information between neighboring chunks.

```
```

```
Document
   │
   ▼
Page Text
   │
   ▼
┌──────────────────────────────┐
│ Chunk 1                      │
└──────────────────────────────┘
        │
        │ 100 character overlap
        ▼
┌──────────────────────────────┐
│ Chunk 2                      │
└──────────────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│ Chunk 3                      │
└──────────────────────────────┘
```

Each chunk is associated with its original PDF page number.

---

## 🔍 Context Retrieval

When the user asks a question, the system identifies document chunks that are relevant to the question.

The current lightweight implementation uses word-overlap based retrieval to identify relevant document content.

```
```

```
User Question
      │
      ▼
Question Words
      │
      ▼
Compare with Document Chunks
      │
      ▼
Calculate Relevance
      │
      ▼
Rank Relevant Chunks
      │
      ▼
Select Top Chunks
      │
      ▼
Build Context
```

The top relevant chunks are passed to the Llama 3.2 model.

---

## 🧮 Retrieval Logic

The current lightweight retrieval approach compares words from the user's question with words contained in document chunks.

The relevance is calculated based on the number of common words between the question and each document chunk.

```
```

```
Question
    │
    ▼
Extract Question Words
    │
    ▼
Compare Against Chunks
    │
    ▼
Calculate Word Overlap
    │
    ▼
Rank Chunks
    │
    ▼
Top 3 Relevant Chunks
```

The top three relevant chunks are selected as the context for the LLM.

This lightweight approach keeps the application simple and avoids requiring paid embedding APIs or large local embedding models.

---

## 🤖 Generative AI

The application uses:

**Ollama + Llama 3.2**

for local AI response generation.

The backend communicates with the locally running Ollama service:

```
```

```
http://127.0.0.1:11434
```

The model receives:

-  Previous conversation 
-  Relevant document context 
-  Current user question 
-  Instructions to avoid unsupported information 

The generated response is returned to the frontend.

---

## 🧠 RAG Prompt Architecture

The LLM prompt is constructed using three major components:

```
```

```
Previous Conversation
        +
Relevant Document Context
        +
Current User Question
        │
        ▼
     Llama 3.2
        │
        ▼
     AI Response
```

The prompt instructs the model to:

-  Answer using the document context 
-  Use previous conversation when relevant 
-  Avoid inventing information 
-  Avoid outside knowledge for document-specific questions 
-  Clearly state when the information cannot be found 

---

## 💬 Conversation Memory

The application maintains recent conversation history.

Each interaction stores:

```
```

```
User Question
      +
AI Answer
```

The most recent conversation items are included when generating a new response.

This allows follow-up questions such as:

```
```

```
User:
What is the exam pattern?

AI:
The examination consists of...

User:
How many questions are there in Stage 1?

AI:
There are 100 questions...
```

The application also provides an endpoint to clear the conversation history.

---

## 📚 Source Page Tracking

Each document chunk stores its original PDF page number.

When relevant chunks are retrieved, the system identifies their corresponding pages.

The API response includes:

```
```

```
{
    "question": "What is the exam pattern?",
    "answer": "...",
    "source_pages": [1, 4],
    "retrieved_chunks": 3
}
```

This provides users with additional transparency about where the answer originated.

---

## 🔌 API Endpoints

| MethodEndpointDescription |               |                                            |
| ------------------------- | ------------- | ------------------------------------------ |
| `GET`                     | `/`           | Serve the web application                  |
| `POST`                    | `/upload`     | Upload and process a PDF document          |
| `POST`                    | `/ask`        | Ask a question about the uploaded document |
| `POST`                    | `/clear-chat` | Clear conversation history                 |

---

## 📚 Swagger API Documentation

FastAPI automatically provides interactive API documentation.

After starting the backend, open:

```
```

```
http://127.0.0.1:8000/docs
```

Swagger can be used to inspect and test the available API endpoints.

---

## ⚙️ Backend Setup

### 1. Clone the repository

```
```

```
git clone https://github.com/MajorKathiravan/AI-Document-Assistant.git
```

### 2. Navigate to the project

```
```

```
cd AI-Document-Assistant
```

### 3. Create a virtual environment

```
```

```
python -m venv venv
```

### 4. Activate the virtual environment

```
```

```
.\venv\Scripts\activate
```

### 5. Install dependencies

```
```

```
pip install -r requirements.txt
```

### 6. Install and configure Tesseract OCR

Install Tesseract OCR and ensure it is available on the system.

For Windows, the application checks:

```
```

```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

### 7. Start Ollama

Make sure Ollama is installed and running.

Download Llama 3.2 if required:

```
```

```
ollama pull llama3.2
```

### 8. Start the FastAPI server

```
```

```
python -m uvicorn Backend.main:app --reload --host 127.0.0.1 --port 8000
```

Backend URL:

```
```

```
http://127.0.0.1:8000
```

Swagger URL:

```
```

```
http://127.0.0.1:8000/docs
```

---

## 🦙 Ollama Setup

The Generative AI component uses **Ollama + Llama 3.2**.

Check installed models:

```
```

```
ollama list
```

Download Llama 3.2 if it is not already installed:

```
```

```
ollama pull llama3.2
```

Test the model:

```
```

```
ollama run llama3.2
```

Example:

```
```

```
>>> hello
```

The model should return an AI-generated response.

The backend communicates with Ollama through:

```
```

```
http://127.0.0.1:11434/api/generate
```

---

## 🧪 Testing

The complete application workflow has been tested successfully.

### Backend

-  ✅ FastAPI startup 
-  ✅ Web application serving 
-  ✅ PDF upload 
-  ✅ PDF text extraction 
-  ✅ Page-by-page processing 
-  ✅ OCR fallback 
-  ✅ Document chunking 
-  ✅ Context retrieval 
-  ✅ Question answering 
-  ✅ Source-page tracking 
-  ✅ Chat history 
-  ✅ Clear-chat endpoint 

### Generative AI

-  ✅ Ollama integration 
-  ✅ Llama 3.2 integration 
-  ✅ Document-context prompting 
-  ✅ Natural-language answers 
-  ✅ Follow-up questions 
-  ✅ Conversation memory 

### Document Processing

-  ✅ PyMuPDF integration 
-  ✅ Tesseract OCR 
-  ✅ PDF page tracking 
-  ✅ Chunk creation 

### Frontend

-  ✅ PDF upload interface 
-  ✅ Question input 
-  ✅ AI response display 
-  ✅ Source-page display 
-  ✅ Conversation interaction 
-  ✅ FastAPI integration 

### Functional Test

The application was tested using an examination syllabus PDF.

Example query:

```
```

```
What is the exam pattern?
```

Follow-up query:

```
```

```
How many questions are there in Stage 1?
```

The application successfully retrieved relevant document information and generated answers using Llama 3.2.

---

## 🔐 Repository Hygiene

The following local and generated files are excluded from Git:

```
```

```
venv/
.env
__pycache__/
*.pyc
Document/*
```

This helps prevent:

-  API keys 
-  Local virtual environments 
-  Uploaded documents 
-  Python cache files 

from being accidentally committed to the repository.

---

## 🚀 Future Improvements

Potential future enhancements include:

-  Vector database integration 
-  Advanced embedding models 
-  Improved semantic search 
-  Multi-document support 
-  Document citation highlighting 
-  Support for DOCX documents 
-  Support for TXT documents 
-  User authentication 
-  Cloud deployment 
-  Persistent document storage 
-  Advanced conversation management 
-  Streaming LLM responses 
-  Improved OCR processing 
-  Document summarization 
-  Automatic question generation 
-  Conversation export 
-  Document comparison 
-  Advanced document analytics 

---

## 🎯 Project Objective

This project demonstrates how to build a complete AI-powered document intelligence product by combining:

-  Artificial Intelligence 
-  Generative AI 
-  Retrieval-Augmented Generation 
-  Natural Language Processing 
-  Large Language Models 
-  Python 
-  FastAPI 
-  REST APIs 
-  PDF Processing 
-  OCR 
-  Local AI Inference 
-  Document Retrieval 
-  Conversation Management 

The project is designed as a portfolio project demonstrating **AI Product Development and AI application engineering**.

---

## 💼 Skills Demonstrated

This project demonstrates practical experience with:

-  Python application development 
-  FastAPI backend development 
-  REST API development 
-  Large Language Model integration 
-  Ollama 
-  Llama 3.2 
-  Retrieval-Augmented Generation 
-  Natural Language Processing 
-  PDF processing 
-  OCR 
-  Document chunking 
-  Information retrieval 
-  Prompt engineering 
-  Conversation memory 
-  API architecture 
-  Frontend/backend integration 
-  Local AI deployment 
-  Git and GitHub 

---

## 🎤 Interview Explanation

### 30-Second Explanation

> I built an AI Document Assistant using a Retrieval-Augmented Generation architecture. The user uploads a PDF, and the system extracts its content using PyMuPDF, with Tesseract OCR as a fallback for scanned pages. I split the document into chunks and retrieve the most relevant chunks based on the user's question. The retrieved context and conversation history are then passed to a local Llama 3.2 model through Ollama, which generates the final answer. I also implemented source-page tracking and conversation memory using FastAPI.

### Technical Flow

```
```

```
PDF
 ↓
PyMuPDF / Tesseract OCR
 ↓
Text Extraction
 ↓
Chunking
 ↓
Context Retrieval
 ↓
RAG Context
 ↓
Ollama
 ↓
Llama 3.2
 ↓
AI Answer
 ↓
Source Pages
```

---

## 📌 Key Learning Outcomes

Through this project, the following concepts were implemented:

### Artificial Intelligence

-  Large Language Models 
-  Generative AI 
-  Prompt Engineering 
-  Local AI inference 

### Machine Learning / NLP

-  Text processing 
-  Context retrieval 
-  Relevance matching 
-  Natural-language question answering 

### AI Product Development

-  AI application architecture 
-  Backend API development 
-  Frontend/backend integration 
-  User interaction design 
-  Error handling 
-  Local deployment 

### Software Engineering

-  Project structure 
-  Virtual environments 
-  Dependency management 
-  Git version control 
-  GitHub repository management 
-  API documentation 

---

## 🚀 Future Product Roadmap

```
```

```
Current Version
      │
      ▼
PDF Question Answering
      │
      ▼
Vector Database
      │
      ▼
Advanced Embeddings
      │
      ▼
Multi-Document RAG
      │
      ▼
Document Comparison
      │
      ▼
Document Summarization
      │
      ▼
Cloud Deployment
      │
      ▼
Enterprise Document Intelligence Platform
```

---

## 👨‍💻 Author

### Kathiravan Velmurugan

**B.Tech – Artificial Intelligence & Data Science**

**AI / ML • Generative AI • Python • FastAPI • RAG • NLP • Data Science**

---

## ⭐ Project

**AI Document Assistant**

Built as an **AI Product Development portfolio project**.

```
```
