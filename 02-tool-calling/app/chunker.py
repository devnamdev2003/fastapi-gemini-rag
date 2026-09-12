# ---------------------------------------------------------
# Company AI Agent - Text Chunker
#
# This file splits large documents into smaller pieces
# called "chunks".
#
# Why do we need chunks?
#
# Instead of sending an entire document to the LLM,
# RAG retrieves only the relevant pieces.
# ---------------------------------------------------------

from .document_loader import load_documents


def chunk_text(text, max_chunk_size=500):
    """
    Split document text into smaller chunks.

    Parameters:
        text:
            Complete document text.

        max_chunk_size:
            Maximum approximate character size of a chunk.

    Returns:
        A list of text chunks.
    """

    # -----------------------------------------------------
    # Split the document using blank lines.
    #
    # Each paragraph becomes a candidate piece of text.
    # -----------------------------------------------------

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []

    # Temporary chunk that we are currently building.
    current_chunk = ""

    # -----------------------------------------------------
    # Combine paragraphs until the maximum chunk size
    # would be exceeded.
    # -----------------------------------------------------

    for paragraph in paragraphs:

        # Check whether the paragraph can fit into the
        # current chunk.
        if (
            len(current_chunk)
            + len(paragraph)
            + 2
            <= max_chunk_size
        ):

            if current_chunk:
                current_chunk += "\n\n"

            current_chunk += paragraph

        else:

            # Save the current chunk before starting
            # a new one.
            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = paragraph

    # -----------------------------------------------------
    # Save the final chunk.
    # -----------------------------------------------------

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


# ---------------------------------------------------------
# Local testing
# ---------------------------------------------------------

if __name__ == "__main__":

    documents = load_documents()

    for document in documents:

        chunks = chunk_text(
            document["content"]
        )

        print("=" * 60)
        print(f"Document: {document['filename']}")
        print(f"Number of chunks: {len(chunks)}")

        for index, chunk in enumerate(chunks):

            print(f"\n--- Chunk {index + 1} ---")
            print(chunk)