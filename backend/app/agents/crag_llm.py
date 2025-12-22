import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

SYSTEM_PROMPT = """
You are a legal relevance classifier.
Given a user query and a document chunk, decide if the chunk is useful
for answering the query.

Rules:
- Output ONLY one word
- Either: RELEVANT or IRRELEVANT
- No explanations
"""

def grade_chunk_llm(query: str, chunk: str) -> bool:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:fireworks-ai",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Query:
{query}

Document:
{chunk}
"""
            }
        ],
        temperature=0.0
    )

    verdict = response.choices[0].message.content.strip().upper()
    print(f"--- [GRADER] Query: {query[:30]}... | Chunk: {chunk[:30]}... | Verdict: {verdict} ---")
    
    # Relaxed check: logic often returns "The chunk is RELEVANT" or "RELEVANT."
    return "RELEVANT" in verdict