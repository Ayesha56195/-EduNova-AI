# 🎓 EduNova AI Pro

An intelligent RAG-based educational chatbot trained on 9,763+ pages of CISSP study material.

## 🚀 Features
- RAG pipeline using LangChain
- ChromaDB vector database
- HuggingFace embeddings
- Groq LLaMA 3.3 70B LLM
- Beautiful Streamlit UI with Dark/Light theme
- Response time, confidence score, and source display

## 🛠️ Tech Stack
- LangChain
- ChromaDB
- HuggingFace (all-MiniLM-L6-v2)
- Groq (LLaMA 3.3 70B)
- Streamlit

## 📦 Installation

```bash
git clone https://github.com/Ayesha56195/-EduNova-AI.git
cd EduNova-AI
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ Setup
Create a `.env` file and add your Groq API key:## 🗄️ Ingest Documents
```bash
python ingest.py
```

## ▶️ Run Application
```bash
streamlit run app.py
```

## 👩‍💻 Developed By
Ayesha — BS Computer Science, LCWU
Internship at Neo-Teric Technologies
