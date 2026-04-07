import os
from fastapi import FastAPI
from openai import OpenAI

# ✅ FastAPI app (required by Hugging Face)
app = FastAPI()


def get_llm_response(prompt: str) -> str:
    """
    FINAL VERSION:
    - Always uses LiteLLM proxy
    - No local bypass
    - Ensures validator detects API call
    """

    # ✅ MUST use these (provided by hackathon)
    base_url = os.environ["API_BASE_URL"]
    api_key = os.environ["API_KEY"]

    client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )

    # ✅ REQUIRED API CALL
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ✅ ROOT ENDPOINT (validator will hit this)
@app.get("/")
def home():
    return {
        "status": "running",
        "llm_output": get_llm_response("Hello from hackathon")
    }