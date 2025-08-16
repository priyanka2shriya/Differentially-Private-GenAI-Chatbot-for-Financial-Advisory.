import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # loads OPENAI_API_KEY from .env
print("DEBUG: OPENAI_API_KEY present?", os.getenv("OPENAI_API_KEY") is not None)

client = OpenAI()  # uses env var by default

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # OK for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = (
    "You are a helpful assistant for consumer financial education. "
    "Answer simply and safely. Do not give personalized investment, tax, or legal advice. "
    "If asked for personal advice, give general education and suggest consulting a professional."
)

@app.get("/hello")
def hello():
    return {"message": "Hello from Backend"}

@app.get("/chat")
def chat(msg: str):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"reply": "OpenAI API key not configured. Ask Hema to add it to .env."}

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # fast & affordable general model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": msg},
            ],
            temperature=0.7,
            max_tokens=200,
        )
        reply = completion.choices[0].message.content
        return {"reply": reply}
    except Exception as e:
        # Don’t leak internals to users; return a friendly error for the UI
        return {"reply": "Sorry, I had trouble generating a response. Please try again."}
