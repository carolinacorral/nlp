import numpy as np
import tokelib as tk

sentences = [
    "Hola, yo soy Caro y me gustan las focas",
    "Soy Gsu y me gusta comer hamburguesas de pavo",
    "Hola, soy Porto y me gusta comer chocolates de foca"
]

corpus = [tk.tokenize(sentence, parser=' ') for sentence in sentences]

vocabulary = tk.get_vocabulary(corpus=corpus, is_nested=True)

n_grams = tk.get_n_grams(n=2, corpus=corpus)

print(n_grams)