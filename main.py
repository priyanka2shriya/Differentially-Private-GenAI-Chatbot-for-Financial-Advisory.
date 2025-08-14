from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS so your browser page (index.html) can call the API during dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # OK for local dev; we'll tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
def hello():
    return {"message": "Hello from Backend"}

@app.get("/chat")
def chat(msg: str):
    # simple echo for now
    return {"reply": f"You said: {msg}. This is a test response from backend."}
