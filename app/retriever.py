import json
import math
from pathlib import Path

from .embedding import create_embedding

VECTOR_STORE_FILE = Path(__file__).resolve().parent.parent / "vector_store.json"


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))

    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)


def load_vector_store():

    with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def keyword_similarity(question, text):
    question_words = set(question.lower().split())
    text_words = set(text.lower().split())

    if not question_words:
        return 0

    matching_words = question_words.intersection(text_words)

    return len(matching_words) / len(question_words)


def retrieve_documents(question, top_k=3, similarity_threshold=0.50):

    vector_store = load_vector_store()

    question_embedding = create_embedding(question)

    results = []

    for item in vector_store:

        semantic_score = cosine_similarity(question_embedding, item["embedding"])

        keyword_score = keyword_similarity(question, item["text"])

        combined_score = 0.8 * semantic_score + 0.2 * keyword_score

        results.append(
            {
                "filename": item["filename"],
                "chunk_id": item["chunk_id"],
                "text": item["text"],
                "similarity": semantic_score,
                "keyword_score": keyword_score,
                "combined_score": combined_score,
            }
        )

    results.sort(key=lambda x: x["combined_score"], reverse=True)

    relevant_results = [
        result for result in results if result["combined_score"] >= similarity_threshold
    ]

    return relevant_results[:top_k]


if __name__ == "__main__":

    question = input("Ask a question: ")

    results = retrieve_documents(question)

    print("\nMost relevant chunks:\n")

    for result in results:

        print("=" * 60)
        print(f"File: {result['filename']}")
        print(f"Chunk: {result['chunk_id']}")
        print(f"Similarity: {result['similarity']:.4f}")
        print()
        print(result["text"])
