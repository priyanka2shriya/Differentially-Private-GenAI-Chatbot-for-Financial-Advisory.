from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load a small free model (first time takes time to download)
generator = pipeline("text-generation", model="distilgpt2")

SYSTEM_PROMPT = (
    "You are a helpful chatbot for financial education. "
    "Answer simply, avoid giving personal investment or legal advice."
)

@app.get("/hello")
def hello():
    return {"message": "Hello from Backend"}

@app.get("/chat")
def chat(msg: str):
    try:
        result = generator(f"{SYSTEM_PROMPT} User: {msg}\nBot:", 
                           max_length=80, num_return_sequences=1)
        reply = result[0]['generated_text'].split("Bot:")[-1].strip()
        return {"reply": reply}
    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "Sorry, I had trouble generating a response."}
