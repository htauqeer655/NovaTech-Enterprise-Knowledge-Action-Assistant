from document_loader import load_documents


def split_text(text, chunk_size=800, chunk_overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap

    return chunks


def create_chunks(documents):
    all_chunks = []

    for document in documents:
        chunks = split_text(document["text"])

        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "source": document["source"],
                "filename": document["filename"],
            })

    return all_chunks


if __name__ == "__main__":
    documents = load_documents()
    chunks = create_chunks(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Created chunks: {len(chunks)}")

    print(f"First chunk length: {len(chunks[0]['text'])}")
    print(f"First chunk preview:\n{chunks[0]['text'][:300]}")