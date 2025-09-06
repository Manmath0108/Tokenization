# PythonScripts/word_level_tokenizer.py
# Corrected word-level tokenizer (Level 3: handles <UNK>)

from typing import List, Dict

def build_vocab(sentences: List[str]) -> Dict[str, int]:
    """
    Build a word-level vocabulary from a list of sentences.
    Reserve ID 0 for the special token '<UNK>'.
    Returns: vocab dict mapping word -> id
    """
    vocab: Dict[str, int] = {"<UNK>": 0}   # Reserve 0 for unknown tokens
    id_counter = 1

    # For each sentence, split into words (lowercased) and add new words to vocab
    for sentence in sentences:
        words = sentence.lower().split()   # IMPORTANT: split into words
        for word in words:
            if word not in vocab:
                vocab[word] = id_counter
                id_counter += 1

    return vocab


def encode(sentence: str, vocab: Dict[str, int]) -> List[int]:
    """
    Encode a single sentence into a list of integer IDs using the provided vocab.
    Unknown words map to 0 (<UNK>).
    """
    words = sentence.lower().split()
    # For each word, use vocab.get(word, 0) so unknown words map to 0 instead of crashing
    return [vocab.get(word, 0) for word in words]


def decode(encoded: List[int], vocab: Dict[str, int]) -> List[str]:
    """
    Decode a list of IDs back into words using the provided vocab.
    """
    # Build reverse mapping id -> word
    id_to_word = {idx: word for word, idx in vocab.items()}
    # For safety, if an id is missing from reverse mapping, map to '<UNK>'
    return [id_to_word.get(idx, "<UNK>") for idx in encoded]


# Simple self-test when this file is run directly
if __name__ == "__main__":
    sample_sentences = [
        "I love learning NLP",
        "NLP is fun",
        "I love Python"
    ]

    v = build_vocab(sample_sentences)
    print("Vocab:", v)

    tests = ["I love NLP", "I enjoy AI"]
    for t in tests:
        e = encode(t, v)
        d = decode(e, v)
        print("Sentence:", t, "Encoded:", e, "Decoded:", d)
