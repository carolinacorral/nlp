import tokelib as tk
import numpy as np


sentences = [
    "Hola, yo soy Caro y soy sigma, ademas soy una foca",
    "Soy Gsu, yo soy god y me gustan los pavos ademas soy una nutria",
    "hola, yo soy ismael, y me gustan los pavos"
]

corpus = [tk.tokenize(sentence, parser=' ') for sentence in sentences]

vocabulary = tk.get_vocabulary(corpus=corpus, is_nested=True)

n_grams = tk.get_n_grams(n=5, corpus=corpus)

print(f"Corpus: {corpus}\n")

print(f"Vocabulary: {vocabulary}\n")

print(f'N grams {n_grams}')

vocab_index = tk.get_word_index(vocabulary=vocabulary)

print(vocab_index)

n_grams = tk.convert_ngrams_numbers(ngrams=n_grams, vocab_index=vocab_index)

print(n_grams)


### Red Neuronal Pre (Many-One)

X = [ngram[:-1] for ngram in n_grams]
Y = [ngram[-1] for ngram in n_grams]

#print(X)
print(Y)


vocab_size = len(vocabulary)

X_one_hot = np.array([tk.one_hot_encode(ngram, vocab_size) for ngram in X])
Y_one_hot = np.array([tk.one_hot_encode([y], vocab_size)[0] for y in Y]) #[0] para quitar dimensión extra

print(X_one_hot)