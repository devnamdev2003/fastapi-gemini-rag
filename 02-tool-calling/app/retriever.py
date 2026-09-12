# ---------------------------------------------------------
# Company AI Agent - Retriever
#
# This file is responsible for finding the most relevant
# document chunks for a user's question.
#
# ---------------------------------------------------------

import json
import math
from pathlib import Path

from .embedding import create_embedding


# ---------------------------------------------------------
# Location of our local vector store.
# ---------------------------------------------------------

VECTOR_STORE_FILE = (
    Path(__file__).resolve().parent.parent
    / "vector_store.json"
)


def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.

    Formula:

        A · B
    -----------
    |A| × |B|

    A higher value means the vectors are more similar.
    """

    # Calculate the dot product.
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    # Calculate magnitude of vector A.
    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    # Calculate magnitude of vector B.
    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    # Prevent division by zero.
    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return (
        dot_product
        / (magnitude_a * magnitude_b)
    )


def load_vector_store():
    """
    Load the previously generated vector store.
    """

    with open(
        VECTOR_STORE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def keyword_similarity(question, text):
    """
    Calculate a simple keyword-overlap score.

    This is not a sophisticated NLP technique.
    It is included to complement semantic similarity.
    """

    # Convert both question and document to lowercase
    # and split them into words.
    question_words = set(
        question.lower().split()
    )

    text_words = set(
        text.lower().split()
    )

    if not question_words:
        return 0

    # Find words appearing in both the question
    # and the document chunk.
    matching_words = (
        question_words.intersection(text_words)
    )

    return (
        len(matching_words)
        / len(question_words)
    )


def retrieve_documents(
    question,
    top_k=3,
    similarity_threshold=0.65
):
    """
    Retrieve the most relevant document chunks.

    Parameters:
        question:
            User's question.

        top_k:
            Maximum number of chunks to return.

        similarity_threshold:
            Minimum combined relevance score.
    """

    # Load stored document embeddings.
    vector_store = load_vector_store()

    # Convert the user's question into an embedding.
    question_embedding = create_embedding(
        question
    )

    results = []

    # -----------------------------------------------------
    # Compare the question with every stored chunk.
    # -----------------------------------------------------

    for item in vector_store:

        # Semantic similarity using embeddings.
        semantic_score = cosine_similarity(
            question_embedding,
            item["embedding"]
        )

        # Simple lexical/keyword similarity.
        keyword_score = keyword_similarity(
            question,
            item["text"]
        )

        # -------------------------------------------------
        # Hybrid retrieval:
        #
        # 80% semantic similarity
        # 20% keyword similarity
        # -------------------------------------------------

        combined_score = (
            0.8 * semantic_score
            + 0.2 * keyword_score
        )

        results.append({
            "filename": item["filename"],
            "chunk_id": item["chunk_id"],
            "text": item["text"],
            "similarity": semantic_score,
            "keyword_score": keyword_score,
            "combined_score": combined_score
        })

    # -----------------------------------------------------
    # Highest-scoring chunks come first.
    # -----------------------------------------------------

    results.sort(
        key=lambda result: result["combined_score"],
        reverse=True
    )

    # -----------------------------------------------------
    # Remove chunks that are below our relevance threshold.
    # -----------------------------------------------------

    relevant_results = [
        result
        for result in results
        if result["combined_score"]
        >= similarity_threshold
    ]

    # Return only the requested number of chunks.
    return relevant_results[:top_k]


# ---------------------------------------------------------
# Local testing
# ---------------------------------------------------------

if __name__ == "__main__":

    question = input(
        "Ask a company question: "
    )

    results = retrieve_documents(
        question
    )

    print("\nMost relevant chunks:\n")

    for result in results:

        print("=" * 60)

        print(
            f"File: {result['filename']}"
        )

        print(
            f"Chunk: {result['chunk_id']}"
        )

        print(
            f"Semantic similarity: "
            f"{result['similarity']:.4f}"
        )

        print(
            f"Keyword score: "
            f"{result['keyword_score']:.4f}"
        )

        print(
            f"Combined score: "
            f"{result['combined_score']:.4f}"
        )

        print()
        print(result["text"])