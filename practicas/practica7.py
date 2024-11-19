import tokelib as tk
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import numpy as np

def get_corpus():
    sentences = []
    directory = "practicas/corpus_7.txt" 
    with open(directory, 'r', encoding='utf-8') as file:
        sentences.append(file.read())
    return sentences

def pre_built(n_gram_size: int):

    sentences = get_corpus()

    corpus = [tk.tokenize(sentence, parser=' ') for sentence in sentences]

    vocabulary = tk.get_vocabulary(corpus=corpus, is_nested=True)

    n_grams = tk.get_n_grams(n=n_gram_size, corpus=corpus)

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

    return X_one_hot, Y_one_hot, vocab_size, vocab_index

def build_model(X_one_hot, Y_one_hot, vocab_size):
    model = Sequential()

    model.add(LSTM(50, input_shape=(X_one_hot.shape[1], X_one_hot.shape[2]), return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(vocab_size, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(X_one_hot, Y_one_hot, epochs=50, batch_size = 1)

    return model



def predict(input, vocab_index, model):
    # Tokenizar entrada
    input = tk.tokenize(input, parser=' ')
    
    #+ Implementación palabra not in vocabulario (wordnet)

    # Buscar el indice de cada palabra en el vocabulario
    input_indices = [vocab_index[word] for word in input]

    # Vectorizar
    X_input = np.array([tk.one_hot_encode(input_indices, len(vocab_index))])
    
    X_input = X_input.reshape((X_input.shape[0], X_input.shape[1], len(vocab_index)))
    
    # Predicciones
    predictions = model.predict(X_input)
    
    predicted_index = np.argmax(predictions)
    
    # obtener palabra por indice (probabilidad mayor)
    predicted_word = [word for word, index in vocab_index.items() if index == predicted_index][0]
    
    return predicted_word

base = input("Ingresa tu oración: ")
n = len(tk.tokenize(base))

X_one_hot, Y_one_hot, vocab_size, vocab_index = pre_built(n_gram_size=n)
model = build_model(X_one_hot, Y_one_hot, vocab_size)

while base != 'esc':
    predicted_word = predict(input=base, vocab_index=vocab_index, model=model)

    print("######")
    print(f'{base}...{predicted_word}')

    new_n = len(tk.tokenize(base))
    if new_n != n:
        print(f"**Longitud necesaria de la oración: {n} palabras")
        X_one_hot, Y_one_hot, vocab_size, vocab_index = pre_built(n_gram_size=n)
        model = build_model(X_one_hot, Y_one_hot, vocab_size)

    print(f'Longitud previa: {n}')
    base = input(f"Ingresa la siguiente oración: ")

