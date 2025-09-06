# APIs/tokenizer_api.py
# FastAPI app for Word-Level Tokenizer (Level 3: with <UNK>)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import platform
import os

# Import tokenizer functions from package
from PythonScripts.word_level_tokenizer import build_vocab, encode, decode

APP_VERSION = "0.1.0"

app = FastAPI(title="Word-Level Tokenizer API", version=APP_VERSION)

# Build vocab once at startup (training sentences)
sentences = [
    "I love learning NLP",
    "NLP is fun",
    "I love Python"
]
vocab = build_vocab(sentences)

class SentenceRequest(BaseModel):
    sentence: str


@app.get("/health", tags=["meta"])
def health() -> Dict[str, Any]:
    """Simple health check."""
    return {"status": "ok"}


@app.get("/version", tags=["meta"])
def version() -> Dict[str, Any]:
    """Returns version + environment info."""
    return {
        "service": "word-level-tokenizer",
        "version": APP_VERSION,
        "python": platform.python_version(),
        "cwd": os.getcwd()
    }


@app.post("/tokenize", tags=["tokenize"])
def tokenize(request: SentenceRequest):
    if not request.sentence:
        raise HTTPException(status_code=400, detail="`sentence` must be provided")
    encoded = encode(request.sentence, vocab)
    decoded = decode(encoded, vocab)
    return {
        "input_sentence": request.sentence,
        "encoded": encoded,
        "decoded": decoded,
        "vocab_size": len(vocab)
    }

    