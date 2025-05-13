from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
load_dotenv()

def search_google(query):
    api_key = os.getenv("SERP_API_KEY")
    print("SerpAPI Key:", api_key)  # DEBUGGING
    if not api_key:
        return "SerpAPI key not found."
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    print("SerpAPI Raw Response:", results)  # DEBUGGING

    top_results = results.get("organic_results", [])[:10]
    if not top_results:
        return "No results found."

    response = []
    for result in top_results:
        title = result.get("title")
        link = result.get("link")
        if title and link:
            response.append(f"{title}\n{link}")

    return "\n\n".join(response)
