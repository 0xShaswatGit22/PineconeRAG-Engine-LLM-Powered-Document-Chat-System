from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List



from typing import List


# ------------------------------
# 1. Load PDF Files
# ------------------------------
def load_pdf_file(folder_path: str):
    """
    Loads all PDF files from a given folder path and returns a list of Documents.
    """
    loader = DirectoryLoader(
        folder_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    return documents


# ------------------------------
# 2. Filter to minimal Document objects
# ------------------------------
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Removes unnecessary metadata from the Document objects
    and keeps only 'source' + page_content.
    """
    minimal_docs: List[Document] = []

    for doc in docs:
        source = doc.metadata.get("source", None)
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": source}
            )
        )

    return minimal_docs


# ------------------------------
# 3. Split text into chunks
# ------------------------------
def text_split(documents: List[Document]):
    """
    Splits documents into text chunks using RecursiveCharacterTextSplitter.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
    )

    text_chunks = splitter.split_documents(documents)
    return text_chunks


# ------------------------------
# 4. Load HuggingFace Embedding Model
# ------------------------------
def download_hugging_face_embeddings():
    """
    Downloads the 'all-MiniLM-L6-v2' embedding model (384 dimensions).
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings
