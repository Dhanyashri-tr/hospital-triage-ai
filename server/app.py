from fastapi import FastAPI
from inference import get_llm_response  # ✅ IMPORT LLM FUNCTION

app = FastAPI()


@app.get("/")
def home():
    # ✅ THIS LINE IS CRITICAL (triggers API call)
    response = get_llm_response("Hello from API")

    return {
        "status": "Server is running",
        "llm_response": response
    }
@app.post("/reset")
def reset():
    return {"status": "reset successful"}


# ✅ REQUIRED MAIN FUNCTION
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# ✅ REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()