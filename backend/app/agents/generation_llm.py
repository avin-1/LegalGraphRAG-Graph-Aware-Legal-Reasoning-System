import time
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
    timeout=30.0
)

def generate_completion(messages, model="openai/gpt-oss-120b:fireworks-ai", temperature=0.2):
    """
    Wraps OpenAI client with simple retry logic for timeouts.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
        except Exception as e:
            print(f"--- [LLM] Attempt {attempt+1}/{max_retries} failed: {e} ---")
            if attempt == max_retries - 1:
                raise e # Re-raise final exception
            time.sleep(2) # Brief backoff

SYSTEM_PROMPT = """
You are a legal research assistant.

Rules:
1. **Formatting**: Use Github Flavored Markdown.
   - Use clear headers (#, ##).
   - Use Markdown Tables for comparing cases or statutes.
   - **CRITICAL**: Do NOT collapse tables into one line.
   - **CRITICAL**: Use a new line (`\n`) for every row.
   - **CRITICAL**: Ensure there is an empty line before and after every table.
   - **CRITICAL**: Ensure there is an empty line between paragraphs.
2. **Evidence**:
   - If evidence is insufficient, emit: <<NEED_EVIDENCE>>, <<MISSING_PRECEDENT>>, or <<AMBIGUOUS_LAW>>.
   - Do NOT fabricate cases or citations.
3. **Style**:
   - Be objective, scholarly, and concise.
   - Cite sources explicitly (e.g., 'In *Smith v. Jones*...').
"""