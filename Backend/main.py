from dotenv import load_dotenv
import os
import numpy as np
import shutil

from openai import OpenAI

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import pymupdf
import pytesseract


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DOCUMENT_FOLDER = os.path.join(
    BASE_DIR,
    "Document"
)

FRONTEND_FILE = os.path.join(
    BASE_DIR,
    "Frontend",
    "index.html"
)

os.makedirs(
    DOCUMENT_FOLDER,
    exist_ok=True
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv(
    os.path.join(
        BASE_DIR,
        ".env"
    )
)

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

client = OpenAI(
    api_key=OPENAI_API_KEY
)


# ============================================================
# TESSERACT OCR
# ============================================================

windows_tesseract = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if os.path.exists(windows_tesseract):

    pytesseract.pytesseract.tesseract_cmd = (
        windows_tesseract
    )


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Document Assistant",
    description="AI-powered document question answering system",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# GLOBAL DOCUMENT DATA
# ============================================================

document_text = ""

document_chunks = []

document_embeddings = []

document_page_numbers = []

conversation_history = []


# ============================================================
# ROOT - SERVE FRONTEND
# ============================================================

@app.get("/")
def root():

    return FileResponse(
        FRONTEND_FILE
    )


# ============================================================
# CREATE OPENAI EMBEDDINGS
# ============================================================

def create_embeddings(texts):

    if not texts:
        return []

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    return [
        item.embedding
        for item in response.data
    ]


# ============================================================
# UPLOAD DOCUMENT
# ============================================================

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    global document_text
    global document_chunks
    global document_embeddings
    global document_page_numbers
    global conversation_history

    # --------------------------------------------------------
    # Save Uploaded File
    # --------------------------------------------------------

    safe_filename = os.path.basename(
        file.filename
    )

    file_path = os.path.join(
        DOCUMENT_FOLDER,
        safe_filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        content = await file.read()

        buffer.write(
            content
        )

    # --------------------------------------------------------
    # Open PDF
    # --------------------------------------------------------

    document = pymupdf.open(
        file_path
    )

    # --------------------------------------------------------
    # Reset Previous Data
    # --------------------------------------------------------

    document_text = ""

    document_chunks = []

    document_embeddings = []

    document_page_numbers = []

    conversation_history = []

    # --------------------------------------------------------
    # Extract Text Page By Page
    # --------------------------------------------------------

    page_data = []

    for page_number, page in enumerate(
        document,
        start=1
    ):

        page_text = page.get_text()

        # ----------------------------------------------------
        # OCR FOR SCANNED PAGES
        # ----------------------------------------------------

        if not page_text.strip():

            try:

                if (
                    os.name == "nt"
                    or shutil.which("tesseract")
                ):

                    pix = page.get_pixmap()

                    image = pix.tobytes(
                        "png"
                    )

                    from PIL import Image
                    from io import BytesIO

                    img = Image.open(
                        BytesIO(image)
                    )

                    page_text = (
                        pytesseract.image_to_string(
                            img
                        )
                    )

            except Exception as e:

                print(
                    "OCR Error:",
                    e
                )

        page_text = page_text.strip()

        if page_text:

            page_data.append(
                (
                    page_number,
                    page_text
                )
            )

            document_text += (
                page_text + "\n"
            )

    # --------------------------------------------------------
    # Page Count
    # --------------------------------------------------------

    pages = len(
        document
    )

    document.close()

    # ========================================================
    # CREATE PAGE-AWARE CHUNKS
    # ========================================================

    chunk_size = 500

    chunk_overlap = 100

    for page_number, page_text in page_data:

        start = 0

        while start < len(page_text):

            end = (
                start +
                chunk_size
            )

            chunk = page_text[
                start:end
            ].strip()

            if chunk:

                document_chunks.append(
                    chunk
                )

                document_page_numbers.append(
                    page_number
                )

            start += (
                chunk_size -
                chunk_overlap
            )

    # ========================================================
    # CREATE OPENAI EMBEDDINGS
    # ========================================================

    if document_chunks:

        try:

            document_embeddings = (
                create_embeddings(
                    document_chunks
                )
            )

        except Exception as e:

            print(
                "Embedding Error:",
                e
            )

            return {
                "filename": safe_filename,
                "message": "Document uploaded, but embedding creation failed.",
                "error": str(e)
            }

    # ========================================================
    # RESPONSE
    # ========================================================

    return {

        "filename":
            safe_filename,

        "message":
            "Document uploaded successfully",

        "pages":
            pages,

        "chunks":
            len(
                document_chunks
            ),

        "text_preview":
            document_text[:500]

    }


# ============================================================
# ASK QUESTION
# ============================================================

@app.post("/ask")
async def ask_question(
    question: str
):

    global conversation_history

    # --------------------------------------------------------
    # CHECK DOCUMENT
    # --------------------------------------------------------

    if not document_text:

        return {

            "question":
                question,

            "answer":
                "Please upload a document first."

        }

    # --------------------------------------------------------
    # CHECK EMBEDDINGS
    # --------------------------------------------------------

    if len(
        document_embeddings
    ) == 0:

        return {

            "question":
                question,

            "answer":
                "Document embeddings are not available."

        }

    # ========================================================
    # QUESTION EMBEDDING
    # ========================================================

    try:

        question_embedding = (
            create_embeddings(
                [question]
            )[0]
        )

    except Exception as e:

        print(
            "Question embedding error:",
            e
        )

        return {

            "question":
                question,

            "answer":
                "Unable to process the question."

        }

    # ========================================================
    # COSINE SIMILARITY
    # ========================================================

    similarities = []

    question_vector = np.array(
        question_embedding
    )

    for embedding in document_embeddings:

        embedding_vector = np.array(
            embedding
        )

        denominator = (

            np.linalg.norm(
                question_vector
            )

            *

            np.linalg.norm(
                embedding_vector
            )

        )

        if denominator == 0:

            similarity = 0

        else:

            similarity = (

                np.dot(
                    question_vector,
                    embedding_vector
                )

                /

                denominator

            )

        similarities.append(
            similarity
        )

    # ========================================================
    # TOP RELEVANT CHUNKS
    # ========================================================

    top_k = min(
        3,
        len(document_chunks)
    )

    top_indices = np.argsort(
        similarities
    )[-top_k:][::-1]

    relevant_chunks = [

        document_chunks[i]

        for i in top_indices

    ]

    # ========================================================
    # SOURCE PAGES
    # ========================================================

    source_pages = sorted(
        set(

            document_page_numbers[i]

            for i in top_indices

        )
    )

    # ========================================================
    # RAG CONTEXT
    # ========================================================

    context = "\n\n".join(
        relevant_chunks
    )

    # ========================================================
    # CONVERSATION CONTEXT
    # ========================================================

    previous_conversation = ""

    for item in conversation_history[-5:]:

        previous_conversation += (

            f"User: "
            f"{item['question']}\n"

            f"Assistant: "
            f"{item['answer']}\n\n"

        )

    # ========================================================
    # AI PROMPT
    # ========================================================

    prompt = f"""
You are an AI Document Assistant.

You have access to:

1. Relevant document context
2. Previous conversation

Previous conversation:

{previous_conversation}

Relevant document context:

{context}

Current user question:

{question}

Instructions:

- Answer document questions using the relevant document context.
- Use previous conversation when the user refers to earlier questions.
- Use both sources when both are relevant.
- Do not invent information.
- Do not use outside knowledge for document-specific questions.
- If the required information is unavailable, say:
"I could not find the answer."

Give a clear, concise and natural answer.
"""

    # ========================================================
    # OPENAI RESPONSE API
    # ========================================================

    try:

        response = client.responses.create(

            model="gpt-4o-mini",

            input=prompt

        )

        answer = response.output_text

    except Exception as e:

        print(
            "OpenAI Error:",
            e
        )

        return {

            "question":
                question,

            "answer":
                "OpenAI connection failed. Please check your API configuration."

        }

    # ========================================================
    # SAVE CONVERSATION
    # ========================================================

    conversation_history.append({

        "question":
            question,

        "answer":
            answer

    })

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "question":
            question,

        "answer":
            answer,

        "source_pages":
            source_pages,

        "retrieved_chunks":
            len(
                relevant_chunks
            )

    }


# ============================================================
# CLEAR CHAT
# ============================================================

@app.post("/clear-chat")
async def clear_chat():

    global conversation_history

    conversation_history = []

    return {

        "message":
            "Chat history cleared successfully"

    }