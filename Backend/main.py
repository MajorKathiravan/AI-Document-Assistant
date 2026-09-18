import os
import shutil
import requests
import numpy as np

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import pymupdf
import pytesseract


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DOCUMENT_FOLDER = os.path.join(BASE_DIR, "Document")
FRONTEND_FILE = os.path.join(BASE_DIR, "Frontend", "index.html")

os.makedirs(DOCUMENT_FOLDER, exist_ok=True)


# =========================================================
# OLLAMA CONFIGURATION
# =========================================================

OLLAMA_URL = "http://127.0.0.1:11434"

OLLAMA_MODEL = "llama3.2"


# =========================================================
# TESSERACT OCR CONFIGURATION
# =========================================================

windows_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(windows_tesseract):
    pytesseract.pytesseract.tesseract_cmd = windows_tesseract


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="AI Document Assistant",
    description="AI-powered document question answering system using RAG and Ollama",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================================================
# GLOBAL DOCUMENT DATA
# =========================================================

document_text = ""

document_chunks = []

document_page_numbers = []

conversation_history = []


# =========================================================
# HOME PAGE
# =========================================================

@app.get("/")
def root():

    return FileResponse(FRONTEND_FILE)


# =========================================================
# CREATE LOCAL EMBEDDINGS
# =========================================================
#
# We use a simple TF-IDF style semantic representation.
# This avoids paid APIs and keeps the project lightweight.
#
# =========================================================

def create_embeddings(texts):

    if not texts:
        return []

    vocabulary = {}

    tokenized_texts = []

    for text in texts:

        words = text.lower().split()

        tokenized_texts.append(words)

        for word in words:

            word = word.strip(".,!?;:()[]{}\"'")

            if word and word not in vocabulary:

                vocabulary[word] = len(vocabulary)


    embeddings = []

    for words in tokenized_texts:

        vector = np.zeros(len(vocabulary))

        for word in words:

            word = word.strip(".,!?;:()[]{}\"'")

            if word in vocabulary:

                vector[vocabulary[word]] += 1


        # Normalize vector

        norm = np.linalg.norm(vector)

        if norm > 0:

            vector = vector / norm


        embeddings.append(vector.tolist())


    return embeddings


# =========================================================
# OLLAMA CHAT FUNCTION
# =========================================================

def ask_ollama(prompt):

    try:

        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "I could not generate an answer."
        )

    except Exception as e:

        print("Ollama Error:", e)

        return (
            "Unable to connect to the local AI model. "
            "Please make sure Ollama is running."
        )


# =========================================================
# UPLOAD DOCUMENT
# =========================================================

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    global document_text
    global document_chunks
    global document_page_numbers
    global conversation_history


    # -----------------------------------------------------
    # Save uploaded document
    # -----------------------------------------------------

    safe_filename = os.path.basename(file.filename)

    file_path = os.path.join(
        DOCUMENT_FOLDER,
        safe_filename
    )


    with open(file_path, "wb") as buffer:

        content = await file.read()

        buffer.write(content)


    # -----------------------------------------------------
    # Open PDF
    # -----------------------------------------------------

    document = pymupdf.open(file_path)


    document_text = ""

    document_chunks = []

    document_page_numbers = []

    conversation_history = []


    page_data = []


    # -----------------------------------------------------
    # Extract text page by page
    # -----------------------------------------------------

    for page_number, page in enumerate(
        document,
        start=1
    ):

        page_text = page.get_text()


        # -------------------------------------------------
        # OCR fallback for scanned pages
        # -------------------------------------------------

        if not page_text.strip():

            try:

                if (
                    os.name == "nt"
                    or shutil.which("tesseract")
                ):

                    pix = page.get_pixmap()

                    image = pix.tobytes("png")

                    from PIL import Image

                    from io import BytesIO

                    img = Image.open(
                        BytesIO(image)
                    )

                    page_text = pytesseract.image_to_string(
                        img
                    )

            except Exception as e:

                print("OCR Error:", e)


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


    pages = len(document)

    document.close()


    # =====================================================
    # CHUNK DOCUMENT
    # =====================================================

    chunk_size = 500

    chunk_overlap = 100


    for page_number, page_text in page_data:

        start = 0


        while start < len(page_text):

            end = start + chunk_size

            chunk = page_text[start:end].strip()


            if chunk:

                document_chunks.append(
                    chunk
                )

                document_page_numbers.append(
                    page_number
                )


            start += (
                chunk_size
                - chunk_overlap
            )


    # =====================================================
    # CREATE LOCAL EMBEDDINGS
    # =====================================================

    try:

        document_embeddings = create_embeddings(
            document_chunks
        )

    except Exception as e:

        print(
            "Embedding Error:",
            e
        )

        return {
            "filename": safe_filename,
            "message": "Document processing failed.",
            "error": str(e)
        }


    return {

        "filename": safe_filename,

        "message": "Document uploaded successfully",

        "pages": pages,

        "chunks": len(document_chunks),

        "text_preview": document_text[:500]
    }


# =========================================================
# QUESTION ANSWERING
# =========================================================

@app.post("/ask")
async def ask_question(
    question: str
):

    global conversation_history


    # -----------------------------------------------------
    # Check document
    # -----------------------------------------------------

    if not document_text:

        return {

            "question": question,

            "answer":
            "Please upload a document first."
        }


    if not document_chunks:

        return {

            "question": question,

            "answer":
            "Document content is not available."
        }


    # -----------------------------------------------------
    # Create question embedding
    # -----------------------------------------------------

    try:

        question_embedding = create_embeddings(
            [question]
        )[0]

    except Exception as e:

        print(
            "Question embedding error:",
            e
        )

        return {

            "question": question,

            "answer":
            "Unable to process the question."
        }


    # =====================================================
    # SEMANTIC SIMILARITY
    # =====================================================

    similarities = []

    question_vector = np.array(
        question_embedding
    )


    for chunk in document_chunks:

        chunk_embedding = create_embeddings(
            [chunk]
        )[0]

        chunk_vector = np.array(
            chunk_embedding
        )


        # Different vocabulary sizes can occur,
        # therefore calculate lexical similarity
        # separately below.

        question_words = set(
            question.lower().split()
        )

        chunk_words = set(
            chunk.lower().split()
        )


        if not question_words:

            similarity = 0

        else:

            common_words = (
                question_words
                .intersection(chunk_words)
            )

            similarity = (
                len(common_words)
                / len(question_words)
            )


        similarities.append(
            similarity
        )


    # =====================================================
    # RETRIEVE TOP CHUNKS
    # =====================================================

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


    source_pages = sorted(
        set(
            document_page_numbers[i]
            for i in top_indices
        )
    )


    context = "\n\n".join(
        relevant_chunks
    )


    # =====================================================
    # CONVERSATION MEMORY
    # =====================================================

    previous_conversation = ""


    for item in conversation_history[-5:]:

        previous_conversation += (

            f"User: {item['question']}\n"

            f"Assistant: {item['answer']}\n\n"

        )


    # =====================================================
    # RAG PROMPT
    # =====================================================

    prompt = f"""
You are an AI Document Assistant.

Your task is to answer questions using the provided document context.

Previous conversation:
{previous_conversation}

Relevant document context:
{context}

Current user question:
{question}

Instructions:

- Answer using the document context.
- Use previous conversation when relevant.
- Do not invent information.
- Do not use outside knowledge for document-specific questions.
- If the answer cannot be found in the document, say:
"I could not find the answer in the document."
- Give a clear and concise answer.
"""


    # =====================================================
    # GENERATE ANSWER USING OLLAMA
    # =====================================================

    answer = ask_ollama(
        prompt
    )


    # =====================================================
    # SAVE CONVERSATION
    # =====================================================

    conversation_history.append(

        {
            "question": question,
            "answer": answer
        }

    )


    return {

        "question": question,

        "answer": answer,

        "source_pages": source_pages,

        "retrieved_chunks": len(
            relevant_chunks
        )
    }


# =========================================================
# CLEAR CHAT
# =========================================================

@app.post("/clear-chat")
async def clear_chat():

    global conversation_history

    conversation_history = []


    return {

        "message":
        "Chat history cleared successfully"
    }