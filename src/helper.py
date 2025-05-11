import os
import json
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
def load_json_files(directory):
    documents = []

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    content = json.dumps(data, indent=2)  # Customize as needed

                    doc = Document(
                        page_content=content,
                        metadata={"source": filename}
                    )
                    documents.append(doc)
            except json.JSONDecodeError as e:
                print(f"Skipping {filename} — JSON decode error: {e}")
            except Exception as e:
                print(f"Skipping {filename} — Unexpected error: {e}")

    return documents

# Split long documents into chunks
def split_documents(documents, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(documents)

def download_huggingface_model_embedding():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings