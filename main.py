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

# Load a small text generation model
generator = pipeline("text-generation", model="gpt2")  # Small model

@app.get("/hello")
def hello():
    return {"message": "Hello from Backend"}

@app.get("/chat")
def chat(msg: str):
    # Generate text
    result = generator(msg, max_length=50, num_return_sequences=1)
    reply = result[0]['generated_text']
    return {"reply": reply}
