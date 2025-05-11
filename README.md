# 📚Study Consultancy Assistant (University Info Retrieval System)

This project is a **Study Consultancy Assistant** designed to help students explore global universities and their academic offerings through natural language queries. It retrieves relevant university data from structured JSON files and provides accurate, concise answers using Retrieval-Augmented Generation (RAG).

---

## Purpose

This tool is intended for use in a **study consultancy** or **student advisory platform**, helping students make informed decisions about where to study based on course availability, location, and degree types.

---

## Key Features

- ✅ **Web Scraping**: University information scraped from [WHED.net](https://www.whed.net) using `Selenium` and `BeautifulSoup`.
- ✅ **Structured Storage**: Collected data stored as structured `.json` files for easy indexing.
- ✅ **Vector Search**: JSON documents embedded using `all-MiniLM-L6-v2` and stored in **Pinecone** for fast retrieval.
- ✅ **RAG with Gemini**: Combines LangChain + Gemini 2.0 LLM to generate context-aware, human-readable responses.
- ✅ **Flask API**: Backend powered by Flask to connect with a chatbot interface or front-end system.

---

##  Tech Stack

| Component     | Tool/Library                         |
|--------------|--------------------------------------|
| Web Scraping | `Selenium`, `BeautifulSoup`          |
| Embeddings   | `HuggingFaceEmbeddings` (`sentence-transformers/all-MiniLM-L6-v2`) |
| LLM          | `Google Gemini 2.0 Flash` via `langchain-google-genai` |
| Vector DB    | `Pinecone`                           |
| Backend API  | `Flask`                              |
| RAG Engine   | `LangChain`                          |
| Environment  | `Python 3.10+`, `dotenv`, `venv`     |

---
## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/wix-buddy.git
cd wix-buddy

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
