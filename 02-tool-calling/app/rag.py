import os

from dotenv import load_dotenv
from google import genai

from .retriever import retrieve_documents


# Load environment variables from .env.
load_dotenv()


# Create Gemini client.
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_rag(question):
    """
    Answer a question using information retrieved
    from the company knowledge base.
    """

    # -----------------------------------------------------
    # Step 1:
    # Retrieve the most relevant document chunks.
    # -----------------------------------------------------

    results = retrieve_documents(
        question,
        top_k=3
    )

    # -----------------------------------------------------
    # Step 2:
    # If nothing relevant was found, don't ask the LLM
    # to guess an answer.
    # -----------------------------------------------------

    if not results:

        return {
            "answer": (
                "I don't have enough information "
                "in the company documents."
            ),
            "sources": []
        }

    # -----------------------------------------------------
    # Step 3:
    # Combine retrieved chunks into the context that
    # will be given to Gemini.
    # -----------------------------------------------------

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    # -----------------------------------------------------
    # Step 4:
    # Create a grounded prompt.
    #
    # The model must answer ONLY using the retrieved
    # company information.
    # -----------------------------------------------------

    prompt = f"""
You are a company knowledge assistant.

Answer the user's question using ONLY the company
information provided in the context below.

Rules:
1. Do not make up information.
2. Do not use information that is not present
   in the provided context.
3. If the answer is not present in the context,
   say exactly:
   "I don't have enough information in the company documents."
4. Give a clear and concise answer.

Company Context:
----------------
{context}
----------------

User Question:
{question}
"""

    # -----------------------------------------------------
    # Step 5:
    # Ask Gemini to generate the final grounded answer.
    # -----------------------------------------------------

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    # -----------------------------------------------------
    # Step 6:
    # Return the answer together with source information.
    # -----------------------------------------------------

    sources = [
        {
            "filename": result["filename"],
            "chunk_id": result["chunk_id"],
            "similarity": round(
                result["similarity"],
                4
            )
        }
        for result in results
    ]

    return {
        "answer": response.text,
        "sources": sources
    }


# ---------------------------------------------------------
# Local testing
# ---------------------------------------------------------

if __name__ == "__main__":

    question = input(
        "Ask a company question: "
    )

    result = ask_rag(question)

    print("\nAI Answer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(source)