import json
from app.agents.generation_llm import generate_completion

EXTRACT_PROMPT = """
You are a legal data specialist. Analyze the following document text (first page/header) and extract the following metadata in JSON format:

1. "title": The official name of the case or document (e.g., "Brown v. Board of Education").
2. "court": The court name (e.g., "Supreme Court of the United States"). If not applicable, use "Unknown Court".
3. "year": The year of the decision/document (integer). If not found, use 0.
4. "citations": A list of other case names or legal statutes cited in the text.

Output ONLY valid JSON. Do not include markdown formatting.
"""

def extract_legal_metadata(text: str) -> dict:
    """
    Extracts title, court, year, citations from the document text.
    """
    messages = [
        {"role": "system", "content": EXTRACT_PROMPT},
        {"role": "user", "content": f"Document Text:\n{text[:2000]}..."} # Limit context
    ]

    print("--- [METADATA] Calling LLM for extraction... (Timeout=30s) ---")
    try:
        response = generate_completion(messages, temperature=0.0)
        print("--- [METADATA] LLM responded. Parsing JSON... ---")
        content = response.choices[0].message.content.strip()
        
        # Cleanup potential markdown wrapping
        if content.startswith("```json"):
            content = content.split("```json")[1]
        if content.endswith("```"):
            content = content.split("```")[0]
            
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"--- [METADATA] Extraction failed: {e} ---")
        return {
            "title": "Unknown Document",
            "court": "Unknown Court",
            "year": 0,
            "citations": []
        }
