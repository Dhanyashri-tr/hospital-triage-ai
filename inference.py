import os
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()


def get_llm_response(prompt: str) -> str:
    base_url = os.environ.get("API_BASE_URL")
    api_key = os.environ.get("API_KEY")

    if not base_url or not api_key:
        return "Local test response"

    client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


@app.get("/")
def home():
    return {
        "response": get_llm_response("Hello from HF")
    }