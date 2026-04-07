from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Server is running"}


# ✅ REQUIRED MAIN FUNCTION
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# ✅ REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()