# ---------------------------------------------------------
# Company AI Agent - Document Loader
#
# This file loads company documents from the documents/
# directory.
#
# The loaded documents are later:
# 1. Split into chunks
# 2. Converted into embeddings
# 3. Stored in the vector store
# 4. Retrieved by the RAG system
# ---------------------------------------------------------

from pathlib import Path


# ---------------------------------------------------------
# Find the project root.
#
# __file__ = app/document_loader.py
# parent    = app/
# parent    = project root
# ---------------------------------------------------------

DOCUMENTS_DIR = (
    Path(__file__).resolve().parent.parent / "documents"
)


def load_documents():
    """
    Load all .txt documents from the documents directory.

    Returns:
        A list of dictionaries containing:
        - filename
        - content
    """

    documents = []

    # -----------------------------------------------------
    # Find every .txt file in the documents directory.
    # -----------------------------------------------------

    for file_path in DOCUMENTS_DIR.glob("*.txt"):

        # Read the document using UTF-8 encoding.
        text = file_path.read_text(
            encoding="utf-8"
        )

        # Store document metadata and content.
        documents.append({
            "filename": file_path.name,
            "content": text
        })

    return documents


# ---------------------------------------------------------
# Local testing
# ---------------------------------------------------------

if __name__ == "__main__":

    documents = load_documents()

    print(f"Loaded {len(documents)} documents\n")

    for document in documents:

        print("=" * 60)
        print(f"Document: {document['filename']}")
        print("=" * 60)

        print(document["content"])
        print()