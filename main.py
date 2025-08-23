from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load a free Hugging Face model (small, runs locally)
generator = pipeline(
    "text-generation",
    model="gpt2",  # Can swap for "distilgpt2" for lighter size
    device=-1       # CPU only (set to 0 for GPU if you have one)
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
    try:
        # Generate response
        text = f"{SYSTEM_PROMPT}\nUser: {msg}\nAssistant:"
        result = generator(text, max_length=100, num_return_sequences=1)
        reply = result[0]["generated_text"].split("Assistant:")[-1].strip()
        return {"reply": reply}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"reply": "Sorry, I had trouble generating a response. Try again."}
