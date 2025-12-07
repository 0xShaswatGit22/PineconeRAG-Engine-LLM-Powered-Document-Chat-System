
# 🩺 Medical Chatbot – LangChain, Pinecone, Flask & AWS 🚀  

End‑to‑end medical chatbot that reads a medical PDF book, builds a vector index with Pinecone, and serves an interactive chat UI over Flask, with CI/CD deployment to AWS using GitHub Actions.[2][1]

***

## ⚙️ How to Run Locally  

1. **Clone the repo** 🧬  
   ```bash
   git clone https://github.com/entbappy/Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS.git
   cd Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS
   ```

2. **Create & activate Conda env** 🐍  
   ```bash
   conda create -n medibot python=3.10 -y
   conda activate medibot
   ```

3. **Install dependencies** 📦  
   ```bash
   pip install -r requirements.txt
   ```
   Make sure any LangChain packages are version‑compatible if you hit dependency errors.[3]

4. **Create `.env` with keys** 🔐  
   In the project root, create a `.env` file:
   ```env
   PINECONE_API_KEY="your_pinecone_key"
   OPENAI_API_KEY="your_openai_key"
   ```
   These are used for vector storage (Pinecone) and LLM calls (OpenAI GPT).[4][1]

5. **Build embeddings & index** 🧠➡️📦  
   ```bash
   python store_index.py
   ```
   This script chunks the medical book, creates embeddings, and uploads them to your Pinecone index.[4]

6. **Run the Flask app** 🌐  
   ```bash
   python app.py
   ```
   Then open `http://127.0.0.1:5000` (or the shown URL) in your browser to chat with the bot.[1]

***

## 🧰 Tech Stack  

- 🐍 Python  
- 🧠 LLMs (OpenAI GPT)  
- 🔗 LangChain  
- 📚 Pinecone (vector DB)  
- 🌐 Flask (backend + simple frontend)  
- ☁️ AWS (EC2, ECR)  
- 🤖 GitHub Actions (CI/CD to AWS)[5][1]

***

## ☁️ AWS CI/CD Deployment (High‑Level)  

1. **Create IAM deploy user** 👤🔑  
   - Grant EC2 and ECR permissions with AWS managed policies like `AmazonEC2FullAccess` and `AmazonEC2ContainerRegistryFullAccess` (for demo only; tighten later for least privilege).[6][7]

2. **Create ECR repository** 📦  
   - Example URI pattern:  
     `ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/medicalbot`  
   - This will store your Docker image.[7][1]

3. **Provision EC2 (Ubuntu)** 💻  
   - Install Docker on the instance and add `ubuntu` user to the `docker` group so GitHub Actions can run containers.[8]

4. **Register EC2 as self‑hosted runner** 🏃  
   - In GitHub: `Settings → Actions → Runners → New self-hosted runner`  
   - Choose Linux, then run the provided commands on EC2 to register and start the runner.[9][10]

5. **Add GitHub secrets** 🔑  
   Configure these in repo settings so the workflow can deploy:  
   - `AWS_ACCESS_KEY_ID`  
   - `AWS_SECRET_ACCESS_KEY`  
   - `AWS_DEFAULT_REGION`  
   - `ECR_REPO` (your ECR URI)  
   - `PINECONE_API_KEY`  
   - `OPENAI_API_KEY`[5][1]

6. **CI/CD flow in GitHub Actions** 🔄  
   - Build Docker image from the project.  
   - Push image to ECR.  
   - On EC2 runner, pull the image from ECR and run the container exposing the Flask app.[11][1]
