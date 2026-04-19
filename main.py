import glob
import os

from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI()

# Load model once (important)
model_path = os.getenv("MODEL_PATH")
if not model_path:
    gguf_files = sorted(glob.glob("*.gguf"))
    if not gguf_files:
        raise FileNotFoundError("No .gguf model file found in the working directory")
    model_path = gguf_files[0]

llm = Llama(
    model_path=model_path,
    n_ctx=1024,
    n_threads=6
)

class Request(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/chat")
def chat(req: Request):
    output = llm(
        req.prompt,
        max_tokens=200,
        temperature=0.7
    )
    return {
        "response": output["choices"][0]["text"]
    }