from dotenv import load_dotenv
from openai import OpenAI
import faiss
import numpy as np
import json
from pathlib import Path

from chunk_document import create_chunks, load_documents

load_dotenv()

# OpenAI client
client = OpenAI()

# Load documents and create chunks
documents = load_documents()
chunks = create_chunks(documents)

print(f"Documents loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")

# Prepare chunk texts
texts = [chunk["text"] for chunk in chunks]

print("Creating embeddings...")

# Create embeddings in one API request
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)

embeddings = np.array(
    [item.embedding for item in response.data],
    dtype="float32"
)

print(f"Embeddings created: {len(embeddings)}")
print(f"Embedding dimension: {embeddings.shape[1]}")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add embeddings
index.add(embeddings)

print(f"FAISS index size: {index.ntotal}")

# Create storage directory
storage_dir = Path("data/vector_store")
storage_dir.mkdir(parents=True, exist_ok=True)

# Save FAISS index
faiss.write_index(
    index,
    str(storage_dir / "company_knowledge.index")
)

# Save chunk metadata/text separately
with open(
    storage_dir / "chunks.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print("\nVector store created successfully!")
print(f"Index: {storage_dir / 'company_knowledge.index'}")
print(f"Metadata: {storage_dir / 'chunks.json'}")