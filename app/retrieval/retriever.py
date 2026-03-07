from pathlib import Path
from pypdf import PdfReader

from app.config import settings


def load_documents() -> list[dict]:
    docs = []
    docs_path = Path(settings.docs_path)

    for pdf_file in docs_path.glob("*.pdf"):
        reader = PdfReader(str(pdf_file))
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                docs.append(
                    {
                        "source": pdf_file.name,
                        "page": page_number,
                        "text": text,
                    }
                )
    return docs


def retrieve_relevant_chunks(query: str, top_k: int = 3) -> list[dict]:
    query_terms = set(query.lower().split())
    scored = []

    for doc in load_documents():
        text_lower = doc["text"].lower()
        score = sum(1 for term in query_terms if term in text_lower)
        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:top_k]]