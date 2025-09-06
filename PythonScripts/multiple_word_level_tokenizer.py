def build_vocab(words):
    vocab = {}
    id_counter = 1
    for word in words:
        if word not in vocab:
            vocab[word] = id_counter
            id_counter += 1
    return vocab

