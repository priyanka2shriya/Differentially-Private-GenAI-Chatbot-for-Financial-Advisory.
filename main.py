from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Backend"}

@app.get("/hello")
def read_root():
    return {"message": "Hello from Backend"}

@app.get("/chat")
def chat(msg: str):
    # For now, just return a simple echo response
    return {"reply": f"You said: {msg}. This is a test response from backend."}
