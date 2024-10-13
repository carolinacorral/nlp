from tokelib import to_lower, is_alpha, is_special, append_cpp, is_numeric

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
        aux = to_lower(document[i])  # Convierte el carácter actual a minúscula.
        
        # Verifica si el carácter es especial o alfabético.
        if is_special(aux) or is_alpha(aux):
            actual += aux  # Si es especial o alfabético, lo añade al token actual.
        elif aux == " " and actual != "":
            # Si encuentra un espacio y el token actual no está vacío,
            # lo añade a la lista de tokens y resetea la variable `actual`.
            tokens = append_cpp(tokens, actual)
            actual = ""  # Resetea el token actual para empezar uno nuevo.
        
        i += 1  # Incrementa el índice para seguir al siguiente carácter.
    
    # Si al final del documento queda un token sin procesar, lo añade a los tokens.
    if actual != "":
        tokens = append_cpp(tokens, actual)
    
    return tokens  # Devuelve la lista de tokens.


def toke_acentos_numeros(document) -> list:
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
        aux = to_lower(document[i])  # Convierte el carácter actual a minúscula.
        
        # Verifica si el carácter es especial o alfabético.
        if is_special(aux) or is_alpha(aux) or is_numeric(aux):
            actual += aux  # Si es especial o alfabético, lo añade al token actual.
        elif aux == " " and actual != "":
            # Si encuentra un espacio y el token actual no está vacío,
            # lo añade a la lista de tokens y resetea la variable `actual`.
            tokens = append_cpp(tokens, actual)
            actual = ""  # Resetea el token actual para empezar uno nuevo.
        
        i += 1  # Incrementa el índice para seguir al siguiente carácter.
    
    # Si al final del documento queda un token sin procesar, lo añade a los tokens.
    if actual != "":
        tokens = append_cpp(tokens, actual)
    
    return tokens  # Devuelve la lista de tokens.


def remove_nums_start_final(word):
    # Elimina los números al principio y al final de una palabra
    i = 0
    j = len(word) - 1
    # Recorre la palabra desde el principio eliminando los números
    while i < len(word) and is_numeric(word[i]):
        i += 1
    # Recorre la palabra desde el final eliminando los números
    while j >= 0 and is_numeric(word[i]):
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
        aux = to_lower(document[i])  # Convierte el carácter actual a minúscula.
        if is_special(aux) or is_alpha(aux):
            actual += aux  # Si es especial o alfabético, lo añade al token actual.
        elif aux == " " and actual != "":
            actual = remove_nums_start_final(actual)  # Elimina los números al inicio y final del token
            tokens = append_cpp(tokens, actual)  # Añade el token procesado a la lista
            actual = ""  # Resetea el token actual para procesar el siguiente
        i += 1
        
    if actual != "":
        actual = remove_nums_start_final(actual)  # Elimina los números al final si los hay
        tokens = append_cpp(tokens, actual)  # Añade el token final a la lista
    return tokens  # Retorna la lista de tokens


def run():
    # Ejemplo de ejecución: tokenizar y remover números de un documento
    document = "[ÉsTE Es UN te1xto para probar 111tokenizació. aTTE 12 EL PEJE"
    print(toke_acentos(document))  # Imprime los tokens procesados

if __name__ == '__main__':
    run()  # Llama a la función `run` si se ejecuta este script
