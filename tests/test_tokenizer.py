# tests/test_tokenizer.py
# pytest unit tests for word_level_tokenizer

import pytest
from PythonScripts.word_level_tokenizer import build_vocab, encode, decode


@pytest.fixture
def sample_sentences():
    """Fixture providing sample training sentences"""
    return [
        "I love learning NLP",
        "NLP is fun",
        "I love Python"
    ]


def test_build_vocab_contains_unk(sample_sentences):
    """Check that vocab contains <UNK> with ID=0 and known words"""
    vocab = build_vocab(sample_sentences)
    # <UNK> must exist and be 0
    assert vocab.get("<UNK>") == 0
    # vocab must contain some known words
    assert "i" in vocab and "nlp" in vocab


def test_encode_known_and_unknown(sample_sentences):
    """Check that known words are encoded correctly and unknown words map to <UNK>"""
    vocab = build_vocab(sample_sentences)
    encoded = encode("I enjoy AI", vocab)
    # 'i' should map to its ID
    assert encoded[0] == vocab["i"]
    # 'enjoy' and 'ai' are not in vocab → map to 0 (<UNK>)
    assert encoded[1] == 0 and encoded[2] == 0


def test_roundtrip_decode(sample_sentences):
    """Check that encode → decode returns the original words (lowercased)"""
    vocab = build_vocab(sample_sentences)
    s = "I love NLP"
    encoded = encode(s, vocab)
    decoded = decode(encoded, vocab)
    assert decoded == ["i", "love", "nlp"]
