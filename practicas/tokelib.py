import numpy as np

def is_special(word):
    """
    Verifica si un carácter es especial (acentos o 'ñ').
    
    Parámetros:
    word (str): Carácter a verificar.
    
    Retorna:
    bool: True si el carácter es especial, False en caso contrario.
    """
    sc = ["Á", "É", "Í", "Ó", "Ú", "á", "é", "í", "ó", "ú", "ñ", "Ñ"]

    return word in sc

def is_alpha(word):
    """
    Verifica si un carácter es alfabético (A-Z, a-z).

    Parámetros:
    word (str): Carácter a verificar.
    
    Retorna:
    bool: True si el carácter es alfabético, False en caso contrario.
    """
    return (65 <= ord(word) <= 90) or (97 <= ord(word) <= 122)

def is_stopword(word, english=False):
    """
    Verifica si una palabra es una stopword (palabra común que no aporta significado en un análisis de texto).

    Parámetros:
    word (str): La palabra a verificar.
    english (bool): Opcional. Si es True, verifica si la palabra es una stopword en inglés. Si es False, usa stopwords en español. El valor predeterminado es False.

    Retorna:
    bool: True si la palabra es una stopword en el idioma especificado, False en caso contrario.
    """
    if english == False:
        stopwords = ["el", "y", "eso", "la", "los", "las", "de", "en", "a", "un", "uno", "una", "es", "con", "para", "al", "del"]
    else:
        stopwords = ["him","on","in","to","her","then", "she", "his", "the", "and", "that", "the", "this", "those", "these", "a", "an", "is", "with", "for", "of"]
    return word in stopwords

def to_lower(letter):
    """
    Convierte un carácter a su versión en minúscula. Si es un carácter especial con acento, lo convierte también.
    
    Parámetros:
    letter (str): Carácter a convertir.
    
    Retorna:
    str: Carácter en minúscula.
    """
    special = ["Á", "É", "Í", "Ó", "Ú", "Ñ"]
    special_lower = ["á", "é", "í", "ó", "ú", "ñ"]
    
    # Si es una letra mayúscula regular
    if 65 <= ord(letter) <= 90:
        return chr(ord(letter) + 32)
    # Si es una letra especial
    elif letter in special:
        return special_lower[special.index(letter)]
    else:
        return letter

def is_numeric(letter):
    """
    Verifica si un carácter es numérico (0-9).
    
    Parámetros:
    letter (str): Carácter a verificar.
    
    Retorna:
    bool: True si el carácter es numérico, False en caso contrario.
    """
    if 48 <= ord(letter) <= 57:
        return True
    else:
        return False

def tf_idf(documents, test_word):
    """
    Calcula la puntuación TF-IDF para una palabra específica en una colección de documentos.
    
    Parámetros:
    documents (list): Lista de documentos (listas de palabras).
    test_word (str): Palabra para la cual calcular el TF-IDF.
    
    Retorna:
    list: Lista de puntuaciones TF-IDF para cada documento.
    """
    tf_idf = []
    word_count = 0  # Cantidad de documentos que contienen la palabra test_word
    
    # Calcular la frecuencia de la palabra en cada documento
    for doc in documents:
        cont = 0
        for word in doc:
            if word == test_word:
                cont += 1
        if cont > 0:
            word_count += 1
        tf = cont / len(doc)  # Frecuencia de la palabra en el documento
        tf_idf.append(tf)
    
    # Calcular el IDF (Inverso de la frecuencia de documentos)
    if word_count > 0:
        idf = np.log10(len(documents) / word_count)
    else:
        idf = 0
    # Multiplicar TF por IDF
    for i in range(len(tf_idf)):
        tf_idf[i] = tf_idf[i] * idf
    
    return tf_idf

def remove_stopwords(doc, english = False):
    """
    Elimina las stopwords de un documento.
    
    Parámetros:
    doc (list): Lista de palabras que conforman el documento.
    
    Retorna:
    list: Nueva lista de palabras sin las stopwords.
    """
    new_doc = []
    for word in doc:
        if not is_stopword(word, english):
            new_doc.append(word)
    return new_doc

def append_cpp(array, element):
    """
    Simula la operación de 'append' en C++, creando una nueva lista con un nuevo elemento.
    
    Parámetros:
    array (list): Lista a la cual añadir el elemento.
    element (any): Elemento a añadir.
    
    Retorna:
    list: Nueva lista con el elemento añadido.
    """
    current_length = len(array)
    
    # Crear una nueva lista de tamaño incrementado en 1
    new_array = [None] * (current_length + 1)
    
    # Copiar elementos de la lista original
    for i in range(current_length):
        new_array[i] = array[i]
    
    # Añadir el nuevo elemento
    new_array[current_length] = element
    
    return new_array

def tokenize(texto, parser=' ', include_numbers=False):
    """
    Tokeniza un texto en una lista de palabras, con la opción de incluir números como parte de los tokens.
    
    Parámetros:
    texto (str): Texto a tokenizar.
    parser (str): Carácter que indica cómo separar las palabras (por defecto, espacio).
    include_numbers (bool): Si se debe incluir números en los tokens.
    
    Retorna:
    list: Lista de tokens extraídos del texto.
    """
    i = 0
    tokens = []
    token = ""
    
    if include_numbers:
        # Tokenización incluyendo números
        while i < len(texto):
            if is_special(texto[i]) or is_alpha(texto[i]) or is_numeric(texto[i]):
                token += to_lower(texto[i])
            elif texto[i] == parser:
                if token != "":
                    tokens += [token]
                token = ""
            i += 1
    else:
        # Tokenización sin incluir números
        while i < len(texto):
            if is_special(texto[i]) or is_alpha(texto[i]):
                token += to_lower(texto[i])
            elif texto[i] == parser:
                if token != "":
                    tokens += [token]
                token = ""
            i += 1
    
    # Añadir el último token si existe
    if token:    
        tokens += [token]
        
    return tokens

def get_tf_idf(corpus):
    words_dict = {} # diccionario a retornar

    for doc in corpus:
        for word in doc:
            # no se repiten las palabras
            if word not in words_dict.keys():
                # se guarda la palabra como llave y una lista de dos TF-IDF como valor
                words_dict[word] = [tf_idf(corpus,word)[0],tf_idf(corpus,word)[1]]
    
    return words_dict

def get_vocabulary(corpus: list, is_nested=True) -> list:
    vocabulary = []
    vocabulary_dict = {}
    
    if (is_nested):
        for document in corpus:
            for word in document:
                if word not in vocabulary_dict:
                    vocabulary_dict[word] = []
                    vocabulary = append_cpp(vocabulary, word)
    else:
        for word in corpus:
                if word not in vocabulary_dict:
                    vocabulary_dict[word] = []
                    vocabulary = append_cpp(vocabulary, word)
    return vocabulary

def bag_of_words_sentence(vocabulary: list, corpus: list) -> list:
    print(f'Vocabulario-------{vocabulary}')
    bag = []

    for doc in corpus:
        vocabulary_vector_token = [0]*len(vocabulary)
        for token in doc:
            print(token)
            vocabulary_vector_token[vocabulary.index(token)] += 1
        print(vocabulary_vector_token)
        bag += [vocabulary_vector_token]

    return bag

def bag_of_words_w(vocabulary: list, corpus: list) -> list:
    print(f'Vocabulario-------{vocabulary}')
    bag = []
    words_already = []

    for word in vocabulary:
        # Una fila por palabra unica
        # En caso de que la palabra ya haya sido contada, se incrementa el contador en la fila correspondiente y columna correspondiente
        # Cada columna es una palabra del vocabulario
        # Cada fila es una palabra unica del documento -> token
        # Cada celda es el contador de la palabra en el documento
        vocabulary_vector_token = [0]*len(vocabulary)
        for doc in corpus:
            for token in doc:
                if token == word:
                    vocabulary_vector_token[vocabulary.index(token)] += 1
        bag += [vocabulary_vector_token]

        print(f'Conteo para la palabra "{word}": {vocabulary_vector_token}')

    return bag

def co_ocurrence_matrix(corpus) -> list:
    """
        Retorna la matriz de co-ocurrencia por palabras a partir de un corpus

        Parámetros:
        corpus: str -> Cuerpo de documentos

        Retorno
        matrix: list -> Matriz de co-ocurrencia
    """
    vocabulary = get_vocabulary(corpus, is_nested=True, repeat_words=True)

    len_cor = len(corpus)
    indx = [0]*len_cor
    
    index_map = {}
    c = 0
    for i in range(len_cor):
        element = corpus[i]
        if element not in index_map:
            index_map[element] = c 
            c += 1
        indx[i] = index_map[element]
    
    n = len(vocabulary) 

    matrix = [[0] * n for _ in range(n)]
    for k in range(len_cor-1):
        i = indx[k]
        j = indx[i+1]
        matrix[i][j] += 1
    return matrix

def get_n_grams(n: int, corpus: list):
    """
        Retorna una lista con los n-grams para un corpus

        Parametros:
        n: int -> Numero de elementos en cada conjunto
        corpus: list -> Cuerpo tokenizado
    """
    n_grams = []
    
    for sentence in corpus:
        for i in range(len(sentence) - n + 1):
            n_grams = append_cpp(n_grams, (sentence[i:i + n]))
        
    return n_grams

