document1 = "asd asd asd"
document2 = "asd asd asd"


def es_acento(letra):
    acentos = ["Á", "É", "Í", "Ó", "Ú", "á", "é", "í", "ó", "ú"]
    
    l = 0
    r = len(acentos) - 1
    
    # Binary search
    while l <= r:
        mid = (l + r) // 2
        if acentos[mid] == letra:
            return True
        elif letra < acentos[mid]:
            r = mid - 1
        else:
            l = mid + 1
    
    return False

def es_letra(letra: str) -> bool:
    return (65 <= ord(letra) <= 90) or (97 <= ord(letra) <= 122)

def es_numero(letra: str) -> bool:
    return (48 <= ord(letra) <= 57)

def mayusToMinus(letra: str):
    if (65 <= ord(letra) <= 90):
        return chr(ord(letra) + 32)
    else:
        return letra
    
def toke_acentos(texto: str) -> list:
    i = 0
    tokens = []
    actual = ""
    
    while i < len(texto):
        if es_acento(texto[i]) or es_letra(texto[i]):
            actual += mayusToMinus(texto[i])
        elif texto[i] == ' ':
            if actual:
                tokens += [actual]
                actual = ""
        i += 1
    
    if actual:
        tokens += [actual]

    return tokens

def TF_IDF(docs, palabra):
    import numpy as np


    tokens = []
    veces_palabra_en_documentos = []

    #Tokenizar los documentos
    for doc in docs:
        tokens.append(toke_acentos(doc))



    for token in tokens:
        contador = 0
        for word in token:
            if word == palabra:
                contador += 1
        veces_palabra_en_documentos.append(contador)


    #print(veces_palabra_en_documentos)
    tf = [round(veces_palabra_en_documentos[x] / len(tokens[x]),4) for x in range(0,len(docs))]
    
    #print(len(docs))
    #print(len([x for x in tf if x > 0]))
    idf = np.log10(len(docs) / len([x for x in tf if x > 0]))
    
    tf_idf = [round(x * idf,4) for x in tf]
    return tf_idf


def run():
    doc1 = "Vamos a criticar a los senores. Los senores son personas alegres."
    doc2 = "Vamos a criticar a los jovenes. Los jovenes son muy callados."

    print(TF_IDF([doc1,doc2], "senores"))

if __name__ == "__main__":
    run()