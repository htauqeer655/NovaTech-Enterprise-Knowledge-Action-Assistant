from pathlib import Path
import json

import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from app.document_loader import load_documents

load_dotenv()

client = OpenAI()

STORAGE_DIR = Path("data/vector_store")
INDEX_FILE = STORAGE_DIR / "company_knowledge.index"
CHUNKS_FILE = STORAGE_DIR / "chunks.json"
EMBEDDING_MODEL = "text-embedding-3-small"


def create_chunks(documents):

    chunks = []

    for document in documents:

        text = document["text"]

        chunk_size = 800
        overlap = 100

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "text": chunk_text,
                        "source": document["source"],
                        "filename": document["filename"],
                        "page": document.get("page", 1),
                    }
                )

            start += chunk_size - overlap

    return chunks


def create_embeddings(texts):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    embeddings = [
        item.embedding
        for item in response.data
    ]

    return np.array(
        embeddings,
        dtype="float32"
    )


def rebuild_index():

    print("Loading original documents...")

    documents = load_documents()

    print(
        f"Loaded {len(documents)} document sections."
    )

    if not documents:
        print("No documents found.")
        return

    chunks = create_chunks(
        documents
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print("Creating embeddings...")

    embeddings = create_embeddings(
        texts
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        embeddings
    )

    STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    with open(
        CHUNKS_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            chunks,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("Clean FAISS index created.")

    print(
        f"Total vectors: {index.ntotal}"
    )

    print(
        f"Total chunks: {len(chunks)}"
    )


if __name__ == "__main__":
    rebuild_index()