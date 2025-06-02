from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
tokenizer = Tokenizer(BPE())
tokenizer.pre_tokenizer = Whitespace()
trainer = BpeTrainer(vocab_size=100, special_tokens=["<unk>"])
corpus = [
    "internationalization and internalization",
    "internationalization",
    "internalization",
    "inter", "national", "internal", "and"
]
tokenizer.train_from_iterator(corpus, trainer)
class SentenceRequest(BaseModel):
    text: str
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    with open("static/tokens.html", "r") as f:
        html_content = f.read()
        return HTMLResponse(content=html_content)
@app.post("/tokenize")
async def tokenize_text(request: SentenceRequest):
    encoded = tokenizer.encode(request.text)
    return {
        "tokens": encoded.tokens,
        "ids": encoded.ids
    }

if __name__ == "__main__":
    uvicorn.run(app, port=5004)