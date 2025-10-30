import os
from settings import settings
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from store import Store


PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    documents = load() # le o pdf
    chunks = split(documents) # separa
    enriched = enrich_metadata(chunks) #enriquece os metadados
    ids = build_ids(enriched) # gera os ids

    embeddings = OpenAIEmbeddings(model=settings.openai_embedding_model, api_key=settings.openai_api_key)

    store = Store(embeddings)
    store.add_documents(documents=enriched, ids=ids)
    
def load() -> list[Document]:
    current_dir = Path(__file__).parent.parent
    pdf_path = current_dir / "relatorio_bairros.pdf"
    return PyPDFLoader(str(pdf_path)).load()  

def enrich_metadata(chunks: list[Document]) -> list[Document]:
    return [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)},
        )
        for d in chunks
    ]


def build_ids(documents: list[Document]) -> list[str]:
    return [f"doc-{index}" for index in range(len(documents))]


def split(documents:  list[Document]) -> list[Document]:
    splits = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=150, add_start_index=False).split_documents(documents)
    if not splits:
        raise SystemExit(0)
    return splits


if __name__ == "__main__":
    ingest_pdf()
