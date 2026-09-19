# AI Document Assistant

An AI-powered document question-answering system built using Retrieval-Augmented Generation (RAG).

The application allows users to upload PDF documents and ask natural-language questions about their content. It extracts document text, divides it into chunks, retrieves relevant content, and uses a local Llama 3.2 model through Ollama to generate answers.

## Features

- PDF document upload
- Text extraction using PyMuPDF
- OCR support using Tesseract
- Document chunking
- Context-based document retrieval
- RAG-based question answering
- Local Llama 3.2 integration using Ollama
- Conversation memory
- Source-page tracking
- FastAPI REST API
- Web-based user interface
- No paid AI API required

## Architecture

```text
User
  |
  v
Web Interface
  |
  v
FastAPI Backend
  |
  +----> PDF Processing
  |          |
  |          +----> PyMuPDF
  |          |
  |          +----> Tesseract OCR
  |
  +----> Document Chunking
  |
  +----> Context Retrieval
  |
  +----> Ollama
            |
            +----> Llama 3.2
            |
            v
         AI Answer
  |
  v
Source Pages + Response
