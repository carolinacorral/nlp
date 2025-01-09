import tokelib 
from nltk.corpus import wordnet

#) Ingressar un corpus que contega palabras con números al final y los elimine, 
# con signos de puntuación que pueden ser repetidos múltiples veces y los elimine, 
# que elimine stopwords y que se visualice bonito la matriz de co-concurrencia. 
#Le van a pedir al usuario una palabra relacionada al tema del corpus y van a predecir 
# las 2 siguientes palabras que podrían seguirle. 
#
#En caso de que la palabra no esta:
#Verificar si tiene que ver con el tema (con wordnet). 
# Si no tiene que ver (grado de similitud <= .5 pedir al usuario que diga otra palabra. 
# Si si tiene que ver, asignarle la palabra mas cercana posible. 
# 1. Preprocessing
# 2. Co-Concurrency



def coocurrency_matrix(corpus: list[str], vocabulary: list[str]=None) -> list[list[int]]:
    """
    Obtiene la matriz de co-ocurrencia dado un corpus tokenizado y un vocabulario.

    Parameters
    ----------
    corpus : list[str]
        Corpus tokenizado.

    vocabulary : list[str], optional
        Vocabulario del corpus. En caso de no ser especificado, se obtiene internamente con 
        `tokelib.get_vocabulary()`. Por defecto es `None`.

    Returns
    -------
    matrix : list[list[str]]
        Matriz de co-ocurrencia.
    """

    if vocabulary is None:
        vocabulary = tokelib.get_vocabulary(corpus,is_nested=False)

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
        j = indx[k+1]
        matrix[i][j] += 1
    return matrix

def similarity(word1: str,word2: str) -> float:
    """ 
    Regresa la similitud Wu-Palmer entre dos palabras.
    Si alguna de las palabras no existe en wordnet, regresa 0. 

    Parameters
    ----------
    word1 : str
        Primera palabra.
    word2: str 
        Segunda palabra.

    Returns
    ---------
    similarity: float
        Similitud Wu-Palmer entre ambas palabras.
    """
    if wordnet.synsets(word2) and wordnet.synsets(word1):
        syn1 = wordnet.synsets(word1)[0]
        syn2 = wordnet.synsets(word2)[0]
        similarity = syn1.wup_similarity(syn2)
    else:
        similarity = 0
    
    return similarity

def closest_word(target_word: str,vocabulary: list[str]) -> tuple[str, float, int]:
    """
    Obtiene la palabra en el vocabulario más cercada a la palabra objetivo.

    Parameters
    ----------
    target_word : str
        Palabra objetivo
    vocabulary : list[str]
        Palabras del corpus (sin repetir)
    
    Returns
    ---------
    max_similarity_score_word: str
        Palabra con similitud Wu-Palmer máxima.
    max_similarity: float
        Similitud Wu-Palmer  máxima encontrada.
    max_sim_row: int
        Índice de la palabra elegida en el vocabulario.
    """
    vocabulary_clean = tokelib.remove_stopwords(vocabulary,english=True)
        
    similarities = [0]*len(vocabulary_clean)
    max_similarity = -1
    max_similarity_score_word = ""
    for j in range(len(vocabulary_clean)):
        similarities[j] = similarity(target_word,vocabulary_clean[j])
        if similarities[j] > max_similarity:
            max_similarity_score_word = vocabulary_clean[j]
            max_similarity = similarities[j]
    max_sim_row = vocabulary.index(max_similarity_score_word)
    return max_similarity_score_word,max_similarity, max_sim_row

def is_in_vocabulary(target_word: str,vocabulary: list[str]) -> int: 
    """ 
    Regresa el índice de la palabra en el vocabulario. En caso de que no exista, regresa -1.

    Parameters
    ----------
    target_word : str
        Palabra a buscar.

    vocabulary : list[str]
        Lista de palabras (sin repetir).

    Returns
    ---------
    word_row: int
        Índice de la palabra en el vocabulario.
    """

    word_row = -1
    for i in range(len(vocabulary)):
        if vocabulary[i] == target_word:
            word_row = i
    return word_row 


def get_next_word(corpus: list[str],target_word: str,matrix: list[list[int]] = None,sim_tol: float=0.7)-> str:
    """
    Obtiene la palabra siguiente a partir de una matriz de co-ocurrencia. En caso de que la palabra no se encuentre 
    en el vocabulario del corpus, se busca la palabra dentro del vocabulario con mayor similitud Wu-Palmer con la 
    palabra ingresada. Si la similitud es mayor a la tolerancia de similitud, se sustituye la palabra ingresada 
    por la palabra con mayor similitud. En caso de que sea menor, se le pide al usuario ingresar otra palabra. 
    
    Parameters 
    -----
    corpus : list[str]
        Corpus tokenizado.

    target_word: str
        Palabra objetivo de la cual se obtendrá la palabra siguiente.

    matrix: list[list[int]]
        Matriz de co-ocurrencia del corpus. Si no se incluye, se calcula dentro de la función con coocurrency_matrix()
        Por defecto None. 

    sim_tol: float
        Tolerancia de similitud Wu-Palmer. Por defecto 0.7.

    Returns 
    -----
    top_word: str
        Palabra predicha a seguir la palabar objetivo.

    """  
    vocabulary = tokelib.get_vocabulary(corpus,is_nested=False)

    if matrix is None:
        matrix = coocurrency_matrix(corpus,vocabulary)
    
    word_row = is_in_vocabulary(target_word,vocabulary)

    while word_row < 0:
        max_sim_word, max_sim, max_sim_row = closest_word(target_word,vocabulary)
        if max_sim > sim_tol:
            word_row = max_sim_row
            print(f"'{target_word}' sustituida por '{max_sim_word}'")
            target_word = max_sim_word
        else:
            print(f"'{target_word}' no esta relacionada con el tema")
            target_word = input("Ingrese una palabra relacionada con el tema: \n")
            word_row = is_in_vocabulary(target_word,vocabulary)
        
    if word_row >= 0:
        word_vec = matrix[word_row]
        max_val = word_vec[0]
        max_index = 0
        for n in range(1,len(word_vec)):
            if max_val < word_vec[n]:
                max_index = n
                max_val = word_vec[n]

        top_word = vocabulary[max_index] 
        return top_word

def read_string_from_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        text = file.read().strip()  
    return text
        
if __name__ == "__main__": 
    tema_heart = read_string_from_file('practicas\\text_heart.txt')
    test = tokelib.tokenize(tema_heart)
    test_words = ["tools","surgery","dancer","person"]
    for test_word in test_words:
        pred = get_next_word(test,test_word,sim_tol=0.7)
        print(f"Palabra predicha para {test_word}: {pred}")
    



