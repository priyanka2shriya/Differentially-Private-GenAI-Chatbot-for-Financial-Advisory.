import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from transformers import pipeline

# Load token from .env
load_dotenv()
hf_token = os.getenv("HUGGINGFACE_TOKEN")

# Use a small model for now
generator = pipeline(
    "text-generation", 
    model="distilgpt2", 
    token=hf_token
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
def hello():
    return {"message": "Hello from Backend"}

@app.get("/chat")
def chat(msg: str):
    try:
        result = generator(msg, max_length=50, num_return_sequences=1)
        reply = result[0]['generated_text']
        return {"reply": reply}
    except Exception as e:
        print("Error:", e)
        return {"reply": "Sorry, I couldn't generate a reply."}
