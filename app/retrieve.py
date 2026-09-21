from pathlib import Path
import faiss
import numpy as np
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

storage_dir = Path("data/vector_store")

index = faiss.read_index(
    str(storage_dir / "company_knowledge.index")
)

with open(
    storage_dir / "chunks.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)


def search(query, top_k=5):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query,
    )

    query_embedding = np.array(
        [response.data[0].embedding],
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        if idx < 0 or idx >= len(chunks):
            continue

        results.append(
            {
                "chunk_id": int(idx),
                "text": chunks[idx]["text"],
                "source": chunks[idx]["source"],
                "filename": chunks[idx]["filename"],
                "distance": float(distance),
            }
        )

    return results


if __name__ == "__main__":

    query = "How many annual leaves does a confirmed employee get?"

    results = search(query, top_k=5)

    print(f"\nQuery: {query}\n")

    for i, result in enumerate(
        results,
        start=1
    ):

        print(f"--- Result {i} ---")
        print(f"File: {result['filename']}")
        print(f"Distance: {result['distance']:.4f}")
        print(result["text"][:500])
        print()