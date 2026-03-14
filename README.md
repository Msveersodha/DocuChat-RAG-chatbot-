# 📄✨ DocuChat — AI Chatbot for Your PDFs

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![OpenAI](https://img.shields.io/badge/LLM-GPT--4o--mini-green)
![LangChain](https://img.shields.io/badge/Framework-LangChain-purple)
![Status](https://img.shields.io/badge/Status-Beta%20v0.5-orange)

DocuChat is a **Retrieval-Augmented Generation (RAG) chatbot** that turns any short PDF *(≤ 5 pages)* into a **live Q&A assistant**.

Upload a document, ask questions, and **DocuChat generates accurate answers grounded in the document itself** — eliminating the need to manually read or skim long PDFs.

🌐 **Live Demo:**  
https://docuchat-live.streamlit.app

---

# 🚀 Key Features

| Feature | Description |
|------|-------------|
| 📥 Drag-and-Drop PDFs | Upload a PDF up to **5 pages / 10k words** for fast indexing |
| 🔎 Semantic Search | Uses **LangChain + Pinecone** embeddings for high-quality retrieval |
| 💬 GPT-4o-mini Answers | Combines retrieved context with OpenAI LLM responses |
| 🔄 Duplicate Detection | SHA-256 hashing prevents re-indexing the same document |
| 🖥 Streamlit UI | Clean, lightweight interface with zero installation |
| 📝 Custom RAG Prompt | Easily modify the prompt template in `pdf_utils.py` |

---

# 🧠 How DocuChat Works

DocuChat follows a **Retrieval-Augmented Generation (RAG) pipeline**:


This ensures answers are **accurate, contextual, and grounded in the document**.

---

# 📦 Tech Stack

| Layer | Technology |
|------|-------------|
| Frontend | Streamlit |
| LLM | OpenAI GPT-4o-mini |
| Framework | LangChain |
| Vector Database | Pinecone |
| PDF Processing | PyMuPDF |
| Language | Python |

---

# ⚙️ Quick Start (Run Locally)

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/DocuChat.git
cd DocuChat

2️⃣ Create Virtual Environment

Recommended for clean dependency management.
python -m venv venv

Windows
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Add API Keys

Create a .env file in the project root:
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
PINECONE_API_KEY=pcd-xxxxxxxxxxxxxxxxxxxx

⚠️ Make sure .env is included in .gitignore

5️⃣ Run the App
streamlit run app.py

Open in your browser:
http://localhost:8501

📄 How to Use

1️⃣ Upload a PDF document (max 5 pages / 10k words)
2️⃣ DocuChat extracts and indexes the document
3️⃣ Ask questions about the content
4️⃣ Receive instant AI-generated answers grounded in the PDF

📸 Example Use Cases

DocuChat is useful for analyzing:

• 📄 Résumés
• 📑 Research papers
• 📘 Policy documents
• 🧪 Lab protocols
• 📝 Meeting notes
• 📚 Study materials

📂 Project Structure

DocuChat
│
├── app.py
├── pdf\_utils.py
├── requirements.txt
├── README.md
├── .env
│
└── assets/
screenshots

🔮 Future Improvements

Multi-document support

Chat history memory

Source citations in answers

PDF highlighting for referenced text

Deployment via Docker

🤝 Contributing

Contributions are welcome.

Fork the repository

Create a new branch

Submit a pull request

📜 License

This project is licensed under the MIT License.
