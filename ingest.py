import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_PATH = "data"
VECTORSTORE_PATH = "vectorstore"

def ingest_documents():
    print("📚 Loading PDFs...")
    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} pages")

    print("✂️ Splitting text...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")

    print("🔢 Creating embeddings & saving to ChromaDB...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vectorstore = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=VECTORSTORE_PATH
    )
    print("✅ Vectorstore saved!")

if __name__ == "__main__":
    ingest_documents()