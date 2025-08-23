from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load a real, free open-source chat model
MODEL_NAME = "HuggingFaceH4/zephyr-7b-alpha"

print("Loading model, this may take a few minutes...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
chatbot = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.get("/hello")
def hello():
    return {"message": "Hello from Backend"}

@app.get("/chat")
def chat(msg: str):
    try:
        response = chatbot(
            msg,
            max_length=200,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7
        )
        reply = response[0]["generated_text"]
        return {"reply": reply}
    except Exception as e:
        print("Error:", e)
        return {"reply": "Sorry, I couldn't generate a reply."}
