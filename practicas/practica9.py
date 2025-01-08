import tokelib as tk
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Input
import os

def get_corpus():
    textos = list()

    for i in range(1, 4):
        ruta_archivo = os.path.join("practicas/etc", f'corpus_{i}.txt')
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            textos = tk.append_cpp(textos, archivo.read())
    return textos
        
def pre_built(n_gram_size: int):
    sentences = get_corpus()
    
    corpus = [tk.tokenize(sentence, parser=' ') for sentence in sentences]

    corpus = [tk.remove_stopwords(doc) for doc in corpus]

    vocabulary = tk.get_vocabulary(corpus=corpus, is_nested=True)
    
    #print(vocabulary)

    n_grams = tk.get_n_grams(n=n_gram_size, corpus=corpus)
    
    vocab_index = tk.get_word_index(vocabulary=vocabulary)

    n_grams = tk.convert_ngrams_numbers(ngrams=n_grams, vocab_index=vocab_index)


    #print(n_grams)

    vocab_size = len(vocabulary)
    
    X = [ngram[:-1] for ngram in n_grams]
    Y = [ngram[-1] for ngram in n_grams]

    X_one_hot = np.array([tk.one_hot_encode(ngram, vocab_size) for ngram in X])
    Y_one_hot = np.array([tk.one_hot_encode([y], vocab_size)[0] for y in Y]) #[0] para quitar dimensión extra

    return X_one_hot, Y_one_hot, vocab_size, vocab_index

def build_model(X_one_hot, Y_one_hot, vocab_size):
    pass

n = 2
X_one_hot, Y_one_hot, vocab_size, vocab_index = pre_built(n_gram_size=n)
