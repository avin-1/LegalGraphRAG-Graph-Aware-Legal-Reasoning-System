import os
import requests


# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") <-- REMOVED

def web_search(query: str, k: int = 5):
    api_key = os.getenv("TAVILY_API_KEY")
    if api_key:
        print(f"--- [SEARCH] Using Key: {api_key[:5]}... ---")
    
    if not api_key or "your_tavily_key" in api_key:
        print("--- [SEARCH] Warning: TAVILY_API_KEY not set. Skipping search. ---")
        return []

    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": api_key,
                "query": query,
                "max_results": k,
                "include_raw_content": False,
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        results = []
        for r in data.get("results", []):
            results.append({
                "content": r.get("content", ""),
                "url": r.get("url", ""),
                "source": "web"
            })
        print(f"--- [SEARCH] Found {len(results)} results for {query} ---")
        return results

    except Exception as e:
        print(f"--- [SEARCH] Failed to search web: {e} ---")
        # Return empty list so the graph can continue (maybe with just retrieval data)
        return []


