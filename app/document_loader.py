from pathlib import Path

from pypdf import PdfReader
from docx import Document

DOCUMENTS_DIRECTORY = Path("data/documents")


def load_txt(file_path):

    text = file_path.read_text(
        encoding="utf-8"
    )

    if not text.strip():
        return []

    return [
        {
            "text": text.strip(),
            "source": str(file_path),
            "filename": file_path.name,
            "page": 1,
        }
    ]


def load_pdf(file_path):

    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text() or ""

        if not text.strip():
            continue

        documents.append(
            {
                "text": text.strip(),
                "source": str(file_path),
                "filename": file_path.name,
                "page": page_number,
            }
        )

    return documents


def load_docx(file_path):

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    if not paragraphs:
        return []

    return [
        {
            "text": "\n".join(paragraphs),
            "source": str(file_path),
            "filename": file_path.name,
            "page": 1,
        }
    ]


def load_documents():

    documents = []

    DOCUMENTS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    for file_path in DOCUMENTS_DIRECTORY.rglob("*"):

        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()

        try:
            if extension == ".txt":
                documents.extend(
                    load_txt(file_path)
                )

            elif extension == ".pdf":
                documents.extend(
                    load_pdf(file_path)
                )

            elif extension == ".docx":
                documents.extend(
                    load_docx(file_path)
                )

        except Exception as e:
            print(
                f"Could not load {file_path.name}: {e}"
            )

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print(
        f"Loaded {len(documents)} document sections"
    )

    for document in documents:
        print(
            f"{document['filename']} "
            f"(page {document['page']})"
        )