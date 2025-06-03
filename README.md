🤖 HR Policy Assistant Chatbot
An intelligent HR assistant powered by Weaviate, Flask, and Gradio that enables semantic search and natural language question-answering over HR policy PDF documents using LLMs (via Ollama) and vector embeddings.

🚀 Features
📄 Upload HR policy documents (PDF)

🔍 Perform semantic search on document chunks

💬 Ask HR-related queries in natural language

🤖 LLM-generated answers based on document context

🧠 Uses Weaviate's text2vec-ollama and generative-ollama modules

🌐 Simple web-based UI using Gradio

📁 Project Structure
bash
Copy
Edit
HR-Policy-Assistant-Chatbot/
│
├── backend.py            # Flask backend handling upload, search, and chat
├── chunks.py             # PDF text extraction and chunking logic
├── connection.py         # Weaviate connection and collection setup
├── frontend.py           # Gradio interface
├── docker-compose.yml    # Weaviate local setup
├── .env                  # Environment variables for model endpoints
└── README.md             # You're here!
🛠️ Technologies Used
Python 3.10+

Flask

Gradio

PyPDF2

LangChain

Weaviate (with Ollama for vectorization & LLMs)

Docker (for Weaviate deployment)

⚙️ Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/hr-policy-assistant-chatbot.git
cd hr-policy-assistant-chatbot
2. Set up the Environment
Install Python dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file:

env
Copy
Edit
DOCKER_API_ENDPOINT=http://localhost:8080
VECTORIZER=llama2
LLM=llama2
Ensure the model names match your local Ollama setup (e.g., LLaMA2, Mistral, etc.)

3. Run Weaviate
Start Weaviate via Docker Compose:

bash
Copy
Edit
docker-compose up -d
4. Run Backend Server
bash
Copy
Edit
python backend.py
5. Launch the Frontend
bash
Copy
Edit
python frontend.py
Gradio UI will open in your browser at: http://localhost:7860

🧪 How It Works
Upload PDF: The document is parsed and split into text chunks.

Data Insertion: Chunks are stored in a Weaviate collection with embeddings.

Semantic Query: The user's question is matched with the most relevant chunk.

LLM Answer: The top chunk is used as context to generate a helpful answer.
