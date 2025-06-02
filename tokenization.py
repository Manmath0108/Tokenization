from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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

@app.post('/tokenize')
def tokenize_text(request: SentenceRequest):
    encoded = tokenizer.encode(request.text)
    return {
        "tokens": encoded.tokens,
        "ids": encoded.ids
    }