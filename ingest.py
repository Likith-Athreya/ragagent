import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

def process_documents(directory="data"):
    # Load documents
    documents = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(path)
            documents.extend(loader.load())
        elif filename.endswith(".txt"):
            loader = TextLoader(path)
            documents.extend(loader.load())
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)
    
    # Create vector store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="mistral"),
        persist_directory="db"
    )
    return vector_store

if __name__ == "__main__":
    process_documents()
    print("Documents processed and vectorized!")