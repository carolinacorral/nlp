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


    print(vocab_index)

    n_grams = tk.convert_ngrams_numbers(ngrams=n_grams, vocab_index=vocab_index)

    #print(n_grams)


    ### Red Neuronal Pre (Many-One)

    X = [ngram[:-1] for ngram in n_grams]
    Y = [ngram[-1] for ngram in n_grams]

    #print(X)
    #print(Y)


    vocab_size = len(vocabulary)

    X_one_hot = np.array([tk.one_hot_encode(ngram, vocab_size) for ngram in X])
    Y_one_hot = np.array([tk.one_hot_encode([y], vocab_size)[0] for y in Y]) #[0] para quitar dimensión extra

    print(X_one_hot)

    return X_one_hot, Y_one_hot, vocab_size, vocab_index

def build_model(X_one_hot, Y_one_hot, vocab_size):
    #X_reshaped = X_one_hot.reshape(X_one_hot.shape[0], 1, X_one_hot.shape[1])

    model = Sequential()
    model.add(LSTM(128, input_shape=(X_one_hot.shape[1], X_one_hot.shape[2]), return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(vocab_size, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(X_one_hot, Y_one_hot, epochs=50, batch_size=32)

    return model

def similar_word():
    pass

def predict(input_text, model, vocab_index, vocab_size, n_gram_size):
    tokens = tk.tokenize(input_text, parser=' ')

    #if len(tokens) < n_gram_size - 1:
    #    tokens = ['<PAD>'] * (n_gram_size - 1 - len(tokens)) + tokens

    input_tokens = tokens[-(n_gram_size-1):]

    input_indices = [vocab_index.get(token, vocab_index.get('<UNK>', 0)) for token in input_tokens]

    X_input = np.array([tk.one_hot_encode(input_indices, vocab_size)])

    predicted_phrase = ""

    predictions = model.predict(X_input)

    predicted_index = np.argmax(predictions)

    vocab_index = {v: k for k, v in vocab_index.items()}

    predicted_word = vocab_index.get(predicted_index, '<UNK>')
    #print(predictions)
    return predicted_word

base = input("Ingresa tu oración: ")
n = 4

X_one_hot, Y_one_hot, vocab_size, vocab_index = pre_built(n_gram_size=n)
model = build_model(X_one_hot, Y_one_hot, vocab_size)
predicted_word = ""
for i in range(10):
    predicted_word = predict(base, model, vocab_index, vocab_size, n)
    base = base + " " + predicted_word
print(base)
