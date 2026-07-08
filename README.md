# ⚖️ Law LLM — Pakistani Legal Assistant

A plain-English legal query application for laymen and lawyers, powered by Retrieval-Augmented Generation (RAG).

## 🎯 Project Overview

This application answers questions about Pakistani criminal law in **simple English**. It searches a curated database of verified legal texts and generates clear, cited answers using a language model — never guessing, always citing the exact Section or Article.

### Legal Sources Covered
| # | Legal Source | Coverage |
|---|---|---|
| 1 | **Pakistan Penal Code, 1860 (PPC)** | All chapters: offences against human body, property, and public order |
| 2 | **Code of Criminal Procedure, 1898 (CrPC)** | Arrest, bail, FIR registration, and investigation procedures |
| 3 | **Constitution of Pakistan, 1973** | Fundamental Rights — Articles 8 to 28 |

All content is sourced exclusively from [pakistancode.gov.pk](https://pakistancode.gov.pk) and [na.gov.pk](https://na.gov.pk).

---

## 🛠️ Technology Stack

| Component | Tool | Purpose |
|---|---|---|
| Language | Python 3.11 | Core development |
| LLM | Groq API — Llama 3.3 70B Versatile (free tier) | Answer generation |
| Embeddings | `BAAI/bge-small-en-v1.5` (384 dimensions) | Text vectorization |
| Vector DB | ChromaDB (local) | Chunk storage & retrieval |
| Orchestration | Plain Python (no LangChain/LlamaIndex) | Transparent pipeline |
| Frontend | Streamlit | Chat-style web UI |
| Deployment | Streamlit Community Cloud | Free public hosting |

---

## 📁 Repository Structure

```
law-llm/
├── data/
│   ├── raw/              # Original source documents
│   │   ├── ppc/          # Pakistan Penal Code
│   │   ├── crpc/         # Code of Criminal Procedure
│   │   └── constitution/ # Constitution of Pakistan
│   ├── clean/            # Cleaned text files (one per Section/Article)
│   └── chunks/           # Chunked text blocks (~500 words each)
├── scripts/
│   ├── test_env.py       # Library verification script
│   ├── test_groq.py      # Groq API connectivity test
│   ├── download_sources.py # Data collection helper
│   ├── clean_data.py     # Data cleaning & splitting
│   ├── chunking.py       # Text chunking script
│   ├── embed.py          # Embedding generation
│   ├── load_db.py        # ChromaDB population
│   ├── llm_call.py       # Groq API wrapper
│   └── rag_pipeline.py   # End-to-end RAG pipeline
├── notebooks/            # Jupyter notebooks for exploration
├── app/
│   └── app.py            # Streamlit application
├── .env.example          # API key template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/abdul-raheem-fast/law-llm.git
cd law-llm
```

### 2. Set Up the Environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure API Key
```bash
cp .env.example .env
# Edit .env and add your Groq API key from https://console.groq.com/
```

### 4. Run the Application
```bash
streamlit run app/app.py
```

---

## 📅 Development Schedule

| Week | Phase | Focus |
|---|---|---|
| **Week 1** | Data Engineering | Collection, cleaning, chunking of legal texts |
| **Week 2** | Knowledge Base | Embeddings, ChromaDB, retrieval testing |
| **Week 3** | RAG Pipeline | LLM integration, prompt engineering, accuracy testing |
| **Week 4** | Deployment | Streamlit UI, cloud deployment, user testing |

---

## 📝 Working Standards
- All code committed daily with descriptive messages
- No hardcoded API keys — `.env` only
- All scripts must run from a clean `requirements.txt` install
- The app must **never fabricate** a Section, Article, or citation
- If retrieval finds no match, the app says so honestly

---

## 👥 Team
- **Project Lead:** Abdul Raheem
- **Supervisor:** Dr. Aasim Qureshi, FAST-NUCES Lahore

## 📄 License
This project is for academic/research purposes under FAST-NUCES Lahore.
