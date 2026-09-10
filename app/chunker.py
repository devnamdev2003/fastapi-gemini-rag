from .document_loader import load_documents


def chunk_text(text, max_chunk_size=500):

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        if len(current_chunk) + len(paragraph) + 2 <= max_chunk_size:

            if current_chunk:
                current_chunk += "\n\n"

            current_chunk += paragraph

        else:

            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


if __name__ == "__main__":

    documents = load_documents()

    for document in documents:

        chunks = chunk_text(document["content"])

        print("=" * 60)
        print(f"Document: {document['filename']}")
        print(f"Number of chunks: {len(chunks)}")

        for index, chunk in enumerate(chunks):

            print(f"\n--- Chunk {index + 1} ---")
            print(chunk)