import json
from pathlib import Path

from .document_loader import load_documents
from .chunker import chunk_text
from .embedding import create_embedding


VECTOR_STORE_FILE = Path(__file__).resolve().parent.parent / "vector_store.json"


def build_vector_store():

    documents = load_documents()

    vector_store = []

    for document in documents:

        chunks = chunk_text(document["content"])

        for index, chunk in enumerate(chunks):

            print(
                f"Creating embedding: "
                f"{document['filename']} - Chunk {index + 1}"
            )

            embedding = create_embedding(chunk)

            vector_store.append({
                "filename": document["filename"],
                "chunk_id": index,
                "text": chunk,
                "embedding": embedding
            })

    with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as file:
        json.dump(vector_store, file)

    print()
    print(f"Vector store created: {VECTOR_STORE_FILE}")
    print(f"Total chunks stored: {len(vector_store)}")


if __name__ == "__main__":
    build_vector_store()