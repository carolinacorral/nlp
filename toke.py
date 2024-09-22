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

def toke_numeros(texto: str) -> list:
    i = 0
    tokens = []
    actual = ""
    
    while i < len(texto):
        if es_acento(texto[i]) or es_letra(texto[i]):
            actual += texto[i]
        elif es_numero(texto[i]):
            if actual:
                tokens += [actual,texto[i]]
            else:
                tokens += [texto[i]]
            actual = ""
        elif texto[i] == ' ':
            if actual:
                tokens += [actual]
                actual = ""
        
        i += 1
    
    if actual:
        tokens += [actual]

    return tokens

def remove_nums(word):
    i =0
    j = len(word) - 1
    while i < len(word) and not es_letra(word[i]):
        i += 1

    while j >= 0 and not es_letra(word[j]):
        j -= 1

    if i > j:
        return word
    else:
        return word[i:j+1]

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

if __name__ == "__main__":
    texto = "EsTE Es UN te1xto para probar tokenización11"
    #texto2 = "Hola mi nombre es marco y yo estudie en la upitta!Saludos. Las dudas de los compañeros "
    ans = toke_stop_words(texto)
    
    for token in ans:
        print(token)

