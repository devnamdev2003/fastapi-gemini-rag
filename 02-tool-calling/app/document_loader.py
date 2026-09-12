from pathlib import Path


DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "documents"


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "filename": file_path.name,
            "content": text
        })

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded {len(documents)} documents\n")

    for document in documents:
        print("=" * 50)
        print(document["filename"])
        print("=" * 50)
        print(document["content"])