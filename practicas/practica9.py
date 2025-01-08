import tokelib as tk
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Input, Flatten
import os

def get_corpus():
    sentences = []
    directory = "practicas/etc/corpus_1.txt"
    with open(directory, 'r', encoding='utf-8') as file:
        sentences.append(file.read())
    return sentences

def pre_built(n_gram_size: int):
    sentences = get_corpus()
    corpus = [tk.tokenize(sentence, parser=' ') for sentence in sentences]
    corpus = [tk.remove_stopwords(doc) for doc in corpus]

    vocabulary = tk.get_vocabulary(corpus=corpus, is_nested=True)
    n_grams = tk.get_n_grams(n=n_gram_size, corpus=corpus)
    vocab_index = tk.get_word_index(vocabulary=vocabulary)
    n_grams = tk.convert_ngrams_numbers(ngrams=n_grams, vocab_index=vocab_index)

    vocab_size = len(vocabulary)
    
    X = [ngram[:-1] for ngram in n_grams]
    Y = [ngram[-1] for ngram in n_grams]

    X_one_hot = np.array([tk.one_hot_encode(ngram, vocab_size) for ngram in X])
    Y_one_hot = np.array([tk.one_hot_encode([y], vocab_size)[0] for y in Y]) #[0] para quitar dimensión extra

    return X_one_hot, Y_one_hot, vocab_size, vocab_index, vocabulary

def build_model(X_one_hot, Y_one_hot, vocab_size):
    model = Sequential([
        Input(shape=(X_one_hot.shape[1], vocab_size)),  # Ajusta la entrada al tamaño correcto
        Flatten(),  # Asegura que la salida sea plana
        Dense(128, activation='relu'),  # Capa oculta con 128 neuronas
        Dense(vocab_size, activation='softmax')  # Salida ajustada al vocabulario
    ])

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_one_hot, Y_one_hot, epochs=110, batch_size=256, verbose=True)
    return model

# Entrenamiento
n = 2
X_one_hot, Y_one_hot, vocab_size, vocab_index, vocabulary = pre_built(n_gram_size=n)
model = build_model(X_one_hot, Y_one_hot, vocab_size)

##
weights = model.get_weights()[0]

word_embeddings = {}
for word in vocabulary:
    word_embeddings[word] = weights[vocab_index[word]]

print(word_embeddings)

import matplotlib.pyplot as plt

# plt.figure(figsize = (10, 10))
for word in list(vocab_index.keys()):
    coord = word_embeddings.get(word)
    plt.scatter(coord[0], coord[1])
    plt.annotate(word, (coord[0], coord[1]))
    plt.show()