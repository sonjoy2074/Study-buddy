from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
load_dotenv()

from serpapi import GoogleSearch
from langchain_google_genai import ChatGoogleGenerativeAI

def search_google(query):
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        return "SerpAPI key not found."

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 5
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    organic_results = results.get("organic_results", [])
    if not organic_results:
        return "No results found."

    # Step 1: Gather snippets into a context paragraph
    snippets = []
    for result in organic_results:
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        link = result.get("link", "")
        if snippet:
            snippets.append(f"{title}\n{snippet}\n{link}\n")

    context = "\n\n".join(snippets)

    # Step 2: Send to LLM for summarization
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.4, 
        max_tokens=500, 
    )

    prompt = (
        "You're a friendly chatbot helping students compare universities. "
        "Using the search snippets below, create a clear, student-friendly comparison. "
        "Respond in an informal but professional tone, and include emojis where helpful. "
        "Cover these points: location, type (public/private), focus areas, reputation, tuition, and admissions. "
        "End with a question to keep the conversation going."
        "\n\n"
        f"Search results:\n{context}"
    )


    response = llm.invoke(prompt)
    return response
