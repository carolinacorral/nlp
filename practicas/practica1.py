import tokelib

def toke_acentos(document) -> list:
    """
    Objetivo general:
    La función `toke_acentos` procesa un texto (documento) para dividirlo en una lista de tokens
    mientras maneja correctamente caracteres especiales (acentos), mayúsculas, y minúsculas.
    """
        
    i = 0  # Inicializa el índice `i` en 0, para recorrer el documento.
    tokens = []  # Lista vacía que almacenará los tokens (palabras extraídas).
    actual = ""  # Variable que acumulará caracteres para formar el token actual.

    # Bucle para recorrer el documento carácter por carácter.
    while i < len(document):
        aux = tokelib.to_lower(document[i])  # Convierte el carácter actual a minúscula.
        
        # Verifica si el carácter es especial o alfabético.
        if tokelib.is_special(aux) or tokelib.is_alpha(aux):
            actual += aux  # Si es especial o alfabético, lo añade al token actual.
        elif aux == " " and actual != "":
            # Si encuentra un espacio y el token actual no está vacío,
            # lo añade a la lista de tokens y resetea la variable `actual`.
            tokens = tokelib.append_cpp(tokens, actual)
            actual = ""  # Resetea el token actual para empezar uno nuevo.
        
        i += 1  # Incrementa el índice para seguir al siguiente carácter.
    
    # Si al final del documento queda un token sin procesar, lo añade a los tokens.
    if actual != "":
        tokens = tokelib.append_cpp(tokens, actual)
    
    return tokens  # Devuelve la lista de tokens.


def is_symbol(character: str) -> bool:
    # Verifica si el carácter es un símbolo (no alfabético ni numérico)
    decimal = ord(character)  # Obtiene el valor ASCII del carácter
    # Retorna True si el carácter es un símbolo basado en rangos ASCII
    return (33 <= decimal <= 47) or (58 <= decimal <= 64) or (91 <= decimal <= 96) or (123 <= decimal <= 126)


def is_number_word(word) -> bool:
    # Verifica si una palabra está compuesta completamente de números
    flag = True
    for char in word:
        if not is_number_char(ord(char)):  # Si algún carácter no es numérico, cambia el flag a False
            flag = False
    return flag  # Retorna True si todos los caracteres son numéricos


def is_number_char(ascii) -> bool:
    # Verifica si un carácter es un número basándose en su valor ASCII
    return 48 <= ascii <= 57  # Retorna True si el valor ASCII corresponde a un número (0-9)


def number_remove(word) -> str:
    # Elimina los números al principio o al final de la palabra, si no está compuesta enteramente por números
    if not is_number_word(word):
        if is_number_char(ord(word[-1])):  # Verifica si el último carácter es un número
            return word[0:-1]  # Si es número, lo elimina
        elif is_number_char(ord(word[0])):  # Verifica si el primer carácter es un número
            return word[1:]  # Si es número, lo elimina
    return word  # Retorna la palabra original si no hay cambios


def toke_acentos_numeros(document) -> list:
    # Tokeniza un documento, considerando símbolos, espacios y números
    tokens = [None] * len(document)  # Inicializa una lista de tokens con el tamaño del documento
    i = 0  # Inicializa el índice `i`
    flag = 0  # Inicializa el marcador de posición `flag`

    # Recorre el documento carácter por carácter
    for letter in document:
        if ord(letter) == 32 or is_symbol(letter):  # Si se detecta un espacio o símbolo
            tokens[i] = document[flag:i]  # Agrega la palabra completa hasta el índice actual
            flag = i + 1  # Actualiza el marcador `flag` al siguiente índice
        i += 1

    # Agrega la última parte del documento a los tokens
    tokens += [document[flag:i]]

    # Filtra los tokens para eliminar los vacíos o nulos
    tokens = [x for x in tokens if x is not None and x != '']

    # Remueve números al principio o final de cada token
    for idx_token in range(len(tokens) - 1):
        tokens[idx_token] = number_remove(tokens[idx_token])

    # Filtra los tokens nuevamente para eliminar los vacíos o nulos
    tokens = [x for x in tokens if x is not None and x != '']

    return tokens  # Retorna la lista de tokens procesados


def remove_nums_start_final(word):
    # Elimina los números al principio y al final de una palabra
    i = 0
    j = len(word) - 1
    # Recorre la palabra desde el principio eliminando los números
    while i < len(word) and tokelib.is_numeric(word[i]):
        i += 1
    # Recorre la palabra desde el final eliminando los números
    while j >= 0 and tokelib.is_numeric(word[i]):
        j -= 1
    # Si toda la palabra es numérica, retorna la palabra completa
    if i > j:
        return word
    else:
        # Retorna la palabra sin los números al principio o final
        return word[i:j+1]


def toke_remove_nums(document):
    # Función para tokenizar eliminando números al principio o al final de cada token
    i = 0  # Inicializa el índice `i` en 0, para recorrer el documento.
    tokens = []  # Lista vacía que almacenará los tokens (palabras extraídas).
    actual = ""  # Variable que acumulará caracteres para formar el token actual.

    while i < len(document):
        aux = tokelib.to_lower(document[i])  # Convierte el carácter actual a minúscula.
        if tokelib.is_special(aux) or tokelib.is_alpha(aux):
            actual += aux  # Si es especial o alfabético, lo añade al token actual.
        elif aux == " " and actual != "":
            actual = remove_nums_start_final(actual)  # Elimina los números al inicio y final del token
            tokens = tokelib.append_cpp(tokens, actual)  # Añade el token procesado a la lista
            actual = ""  # Resetea el token actual para procesar el siguiente
        i += 1
        
    if actual != "":
        actual = remove_nums_start_final(actual)  # Elimina los números al final si los hay
        tokens = tokelib.append_cpp(tokens, actual)  # Añade el token final a la lista
    return tokens  # Retorna la lista de tokens


def run():
    # Ejemplo de ejecución: tokenizar y remover números de un documento
    document = "[ÉsTE Es UN te1xto para probar 111tokenizació. aTTE 12 EL PEJE"
    print(toke_remove_nums(document))  # Imprime los tokens procesados

if __name__ == '__main__':
    run()  # Llama a la función `run` si se ejecuta este script
