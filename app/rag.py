import os

from dotenv import load_dotenv
from google import genai

from .retriever import retrieve_documents


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_rag(question):

    # 1. Retrieve relevant documents
    results = retrieve_documents(
        question,
        top_k=3
    )

    # 2. If nothing relevant was found
    if not results:
        return {
            "answer": "I don't have enough information in the company documents.",
            "sources": []
        }

    # 3. Build context
    context = "\n\n".join(
        result["text"]
        for result in results
    )

    # 4. Ask Gemini using retrieved context
    prompt = f"""
You are a company knowledge assistant.

Answer the user's question using ONLY the company
information provided in the context below.

If the answer is not present in the context, say:
"I don't have enough information in the company documents."

Do not make up information.

Company Context:
----------------
{context}
----------------

User Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    # 5. Prepare source information
    sources = [
        {
            "filename": result["filename"],
            "chunk_id": result["chunk_id"],
            "similarity": round(result["similarity"], 4)
        }
        for result in results
    ]

    return {
        "answer": response.text,
        "sources": sources
    }