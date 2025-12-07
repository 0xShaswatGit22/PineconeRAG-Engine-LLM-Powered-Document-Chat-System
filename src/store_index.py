from dotenv import load_dotenv
import os
from src.helper import (
    load_pdf_file,
    filter_to_minimal_docs,
    text_split,
    download_hugging_face_embeddings
)
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# ----------------------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------------------
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# ----------------------------------------------------------------
# Load & Process PDF documents
# ----------------------------------------------------------------
extracted_data = load_pdf_file("data/")
filtered_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filtered_data)

# ----------------------------------------------------------------
# Load Embeddings (384-dim HuggingFace)
# ----------------------------------------------------------------
embeddings = download_hugging_face_embeddings()

# ----------------------------------------------------------------
# Initialize Pinecone client
# ----------------------------------------------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"

# Check if index exists
existing_indexes = [idx["name"] for idx in pc.list_indexes()]

# Create index if not already created
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,     # All-MiniLM-L6-v2 = 384 dims
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the index
index = pc.Index(index_name)

# ----------------------------------------------------------------
# Store Documents in Pinecone
# ----------------------------------------------------------------
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name=index_name
)

print("🎉 Successfully stored all embeddings into Pinecone index:", index_name)
