import tokelib as tk



corpus = ["Hola, mi nombre es Port", "Hola, soy Mong", "Hola, soy Gsu"]

tokens = list()

for document in corpus:
    document = tk.tokenize(document, parser=' ', include_numbers=True)
    tokens = tk.append_cpp(tokens, tk.remove_stopwords(document))

print(tokens)

vocabulario = tk.get_vocabulary(tokens, is_nested=True, repeat_words=True)