import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)
def msg(ms)->str:
    completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3.2:fireworks-ai",
    messages=[
        {
            "role": "user",
            "content": ms
        }
    ],
    )
    print(completion.choices[0].message.content)

def queryHandler(query:str)->None:
    msg(query)