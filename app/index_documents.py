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
EMBEDDING_DIMENSION = 1536  # text-embedding-3-small output size


def load_existing_data():

    STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if INDEX_FILE.exists() and CHUNKS_FILE.exists():

        index = faiss.read_index(
            str(INDEX_FILE)
        )

        with open(
            CHUNKS_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            chunks = json.load(f)

        return index, chunks

    # No existing index yet — start fresh
    index = faiss.IndexFlatL2(EMBEDDING_DIMENSION)
    chunks = []

    return index, chunks


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


def index_new_documents():

    print("Loading documents...")

    documents = load_documents()

    index, existing_chunks = (
        load_existing_data()
    )

    indexed_files = {
        chunk["filename"]
        for chunk in existing_chunks
    }

    new_documents = [
        document
        for document in documents
        if document["filename"]
        not in indexed_files
    ]

    print(
        f"Loaded document sections: "
        f"{len(documents)}"
    )

    print(
        f"Already indexed files: "
        f"{len(indexed_files)}"
    )

    print(
        f"New document sections: "
        f"{len(new_documents)}"
    )

    if not new_documents:
        print("No new documents to index.")
        return

    new_chunks = create_chunks(
        new_documents
    )

    print(
        f"Created {len(new_chunks)} new chunks."
    )

    texts = [
        chunk["text"]
        for chunk in new_chunks
    ]

    print("Creating embeddings...")

    embeddings = create_embeddings(
        texts
    )

    index.add(
        embeddings
    )

    existing_chunks.extend(
        new_chunks
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
            existing_chunks,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("Incremental indexing completed.")

    print(
        f"Total FAISS vectors: "
        f"{index.ntotal}"
    )

    print(
        f"Total chunks: "
        f"{len(existing_chunks)}"
    )


if __name__ == "__main__":
    index_new_documents()