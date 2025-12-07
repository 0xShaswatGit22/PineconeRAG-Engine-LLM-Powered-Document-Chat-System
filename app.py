from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings  # Your custom helper
from langchain_pinecone import PineconeVectorStore  # New Pinecone integration
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain  # From core langchain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain  # Legacy chain from langchain-classic
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *  # Your prompts
from pinecone import PineconeClient   # ← ONLY change this line
import os

load_dotenv()

app = Flask(__name__)

# Example: Initialize Pinecone (updated syntax)
from pinecone import Pinecone   # ← now works again!
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("your-index-name")  # Or create if needed
embeddings = download_hugging_face_embeddings()  # Your function
vectorstore = PineconeVectorStore(index=index, embedding=embeddings)

# Rest of your code (chains, routes) stays mostly the same
prompt = ChatPromptTemplate.from_template("Your prompt here {context}")
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
document_chain = create_stuff_documents_chain(llm, prompt)
retriever = vectorstore.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Flask route example
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.json.get("query")
        result = retrieval_chain.invoke({"input": query})
        return jsonify({"answer": result["answer"]})
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)