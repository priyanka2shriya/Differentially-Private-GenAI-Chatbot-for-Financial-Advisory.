from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Backend"}

@app.get("/hello")
def read_root():
    return {"message": "Hello from Backend"}
