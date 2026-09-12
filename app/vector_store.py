# ---------------------------------------------------------
# Company AI Agent - Vector Store
#
# This file creates our simple local vector store.
#
# NOTE:
# JSON is being used here for learning.
# In production, we would normally use a proper vector
# database such as PostgreSQL + pgvector, Pinecone,
# Weaviate, Qdrant, etc.
# ---------------------------------------------------------

import json
from pathlib import Path

from .document_loader import load_documents
from .chunker import chunk_text
from .embedding import create_embedding


# ---------------------------------------------------------
# Location of the vector store.
# ---------------------------------------------------------

VECTOR_STORE_FILE = (
    Path(__file__).resolve().parent.parent
    / "vector_store.json"
)


def build_vector_store():
    """
    Create embeddings for all document chunks and save
    them into vector_store.json.
    """

    # Load all company documents.
    documents = load_documents()

    # This list will contain every chunk and its embedding.
    vector_store = []

    # -----------------------------------------------------
    # Process every document.
    # -----------------------------------------------------

    for document in documents:

        # Split the document into smaller chunks.
        chunks = chunk_text(
            document["content"]
        )

        # -------------------------------------------------
        # Create an embedding for every chunk.
        # -------------------------------------------------

        for index, chunk in enumerate(chunks):

            print(
                f"Creating embedding: "
                f"{document['filename']} - "
                f"Chunk {index + 1}"
            )

            # Convert the chunk into a numerical vector.
            embedding = create_embedding(chunk)

            # Store both the original text and its vector.
            vector_store.append({
                "filename": document["filename"],
                "chunk_id": index,
                "text": chunk,
                "embedding": embedding
            })

    # -----------------------------------------------------
    # Save the vector store as JSON.
    # -----------------------------------------------------

    with open(
        VECTOR_STORE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            vector_store,
            file
        )

    print()
    print(
        f"Vector store created: {VECTOR_STORE_FILE}"
    )

    print(
        f"Total chunks stored: {len(vector_store)}"
    )


# ---------------------------------------------------------
# Run this file directly to rebuild the vector store.
# ---------------------------------------------------------

if __name__ == "__main__":

    build_vector_store()