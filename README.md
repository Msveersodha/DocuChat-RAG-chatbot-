# DocuChat-RAG-chatbot-
✨ What is DocuChat?
DocuChat is a Retrieval‑Augmented Generation (RAG) chatbot that turns any short PDF ( ≤ 5 pages ) into a live Q&A assistant.
Upload a document, ask anything, and DocuChat responds with grounded, citation‑worthy answers—no manual skimming required.

Typical uses	Résumé review, policy documents, research papers, lab protocols, meeting notes
Tech stack	Streamlit · LangChain · OpenAI · Pinecone · PyMuPDF
Live demo	docuchat-live.streamlit.app
Status	Beta v0.5 – feedback welcome 🙌
🚀 Key Features
Feature	Details
📥 Drag‑and‑Drop PDFs	Accepts one PDF up to 5 pages / 10 k words for fast indexing
🔎 Semantic Chunking & Search	Uses LangChain + Pinecone to embed 500‑token chunks with overlap, ensuring query‑time recall
💬 GPT‑4o‑mini Answers	Combines retrieved context with OpenAI’s GPT‑4o‑mini for accurate, concise responses
🔄 Duplicate Detection	SHA‑256 hash prevents re‑indexing of the same document
🖥 Zero‑Install Front‑End	Pure Streamlit interface—runs locally or on Streamlit Cloud
📝 Extensible RAG Prompt	Self‑contained prompt template in pdf_utils.py for easy tweaking
⚙️ Quick Start (Run Locally)
🧑‍💻 1. Clone the Repository
git clone https://github.com/your-username/DocuChat.git
cd DocuChat
📦 2. Create a Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
📂 3. Install Dependencies
pip install -r requirements.txt
🔐 4. Add Your API Keys
Create a .env file in the root directory of the project and add the following:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PINECONE_API_KEY=pcd-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
⚠️ Make sure your .env file is listed in .gitignore to avoid committing sensitive keys.

🚀 5. Run the Streamlit App
streamlit run app.py
The app will open in your browser at:

http://localhost:8501
📄 How to Use
Upload a PDF file (up to 5 pages, max 10,000 words).
DocuChat will validate the PDF and extract chunks.
Ask any question based on the PDF's content.
Get instant, accurate answers from the LLM, grounded in your document.
