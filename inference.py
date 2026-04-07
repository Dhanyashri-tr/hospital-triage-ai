import os
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()


def get_llm_response(prompt: str) -> str:
    base_url = os.environ.get("API_BASE_URL")
    api_key = os.environ.get("API_KEY")

    # ✅ Use proxy in hackathon
    if base_url and api_key:
        client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    # ✅ HF fallback
    return "Server running (proxy will be used during evaluation)"


# ✅ ROOT ENDPOINT
@app.get("/")
def home():
    return {
        "status": "running",
        "llm_output": get_llm_response("Hello from hackathon")
    }


# 🔥🔥 REQUIRED FOR PHASE 1
@app.post("/reset")
def reset():
    return {"status": "reset successful"}