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
        stopwords = ["the", "and", "that", "the", "this", "those", "these", "a", "an", "is", "with", "for", "of"]
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
    idf = np.log10(len(documents) / word_count)
    
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

def tokenize(texto, parser=' ', include_numbers=False, english = False):
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

if __name__ == '__main__':
    print(to_lower("Á"))
