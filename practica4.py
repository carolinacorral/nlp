def toke_stop_words(texto: str) -> list:
    i = 0
    tokens = []
    actual = ""
    stopwords = ["el", "y", "eso", "la", "los", "las" ,"de","en","a","un","uno","una","es","con","es","con","para","al","del"]

    while i < len(texto):
        if es_acento(texto[i]) or es_letra(texto[i]) or es_numero(texto[i]):
            actual += mayusToMinus(texto[i])
        elif texto[i] == ' ':
            if actual != "" and not(actual in stopwords):
                actual = remove_nums(actual)
                tokens += [actual]
            actual = ""
        i += 1

    if actual != "" and not(actual in stopwords):
        actual = remove_nums(actual)
        tokens += [actual]

    return tokens

def bag_of_words(corpus: list) -> list:
    vocab = [] #Contener las palabras unicas segun el orden de aparicion
    bag = []
    for tokens in corpus:
        for token in tokens:
            if token not in vocab:
                vocab.append(token)

    for tokens in corpus:
        vec = [0] * len(vocab)
        for token in tokens:
            vec[vocab.index(token)] += 1
        bag += vec

def run():
    texto1 = "Gsu es god"
    texto2 = "Caro es sigma"

    corpus = [texto1,texto2]


if __name__ == '__main__':
    run()


        
