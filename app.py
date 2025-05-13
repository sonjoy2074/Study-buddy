from flask import Flask, render_template, jsonify, request
from src.helper import download_huggingface_model_embedding
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os
from src.search import search_google
app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
embeddings = download_huggingface_model_embedding()


index_name = "wixbuddy"

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.4, 
    max_tokens=500, 

)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print("User Input:", msg)

    # Try RAG response first
    response = rag_chain.invoke({"input": msg})

    # Extract string content from AIMessage or dict
    if isinstance(response, dict) and "answer" in response:
        answer = response["answer"]
    elif hasattr(response, "content"):  # if it's an AIMessage
        answer = response.content
    else:
        answer = str(response)

    print("RAG Response:", answer)

    # Fallback if RAG fails or gives insufficient response
    if "I don't" in answer or "I am sorry" in answer or not answer.strip():
        print("Using Google search as fallback...")
        fallback = search_google(msg)

        if hasattr(fallback, "content"):
            answer = fallback.content
        else:
            answer = str(fallback)

        print("Google Search Response:", answer)

    return answer  # Must return a string here!




if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)