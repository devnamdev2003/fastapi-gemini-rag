import os

from dotenv import load_dotenv
from google import genai

from .chunker import chunk_text
from .document_loader import load_documents


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def create_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )

    return response.embeddings[0].values


if __name__ == "__main__":

    documents = load_documents()

    for document in documents:

        chunks = chunk_text(document["content"])

        for index, chunk in enumerate(chunks):

            embedding = create_embedding(chunk)

            print("=" * 60)
            print(f"Document: {document['filename']}")
            print(f"Chunk: {index + 1}")
            print(f"Embedding dimensions: {len(embedding)}")
            print(f"First 5 values: {embedding[:5]}")