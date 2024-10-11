import numpy as np
from tokelib import tokenize, append_cpp, remove_stopwords
    

def tf_idf(documents,test_word):
    tfs = []
    tf_idf = [] #lista a regresar 
    word_count = 0 
    for doc in documents:
        cont = 0
        for word in doc:
            # cont cuenta número de apariciones en documento i
            if word == test_word: 
                cont+=1      
        # word_count registra número de documentos donde aparece
        if cont > 0 :
            word_count += 1    
        # TF de palabra en documento i
        tf = cont/len(doc)
        # se guarda en la lista tfs
        tfs = append_cpp(tfs,tf)
    
    # valor de IDF con numpy
    idf = np.log10(len(documents)/word_count)

    # se crean valores de TF-IDF multiplicando cada TF por el IDF
    for i in range(0,len(tfs)):
        tf_idf = append_cpp(tf_idf,tfs[i]*idf)
    
    return tf_idf


def get_tf_idf(corpus):
    words_dict = {} # diccionario a retornar

    for doc in corpus:
        for word in doc:
            # no se repiten las palabras
            if word not in words_dict.keys():
                # se guarda la palabra como llave y una lista de dos TF-IDF como valor
                words_dict[word] = [tf_idf(corpus,word)[0],tf_idf(corpus,word)[1]]
    
    return words_dict

def ejercicio1_a(corpus):
    # obtenemos un dict con los dos TF-IDF por palabra
    tf_idfs = get_tf_idf(corpus)

    new_docs = [] # lista de documentos a regresar
    for doc in corpus:
        new_doc =[]  # nuevo documento
        for word in doc:
            # verificar que no se agreguen palabras duplicadas
            if word not in new_doc:
                i = 0
                cont = 0
                # se itera la lista de TF-IDFs de la palabra en el diccionario
                while i < len(tf_idfs[word]): 
                    # se registra el número de veces que aparece algo diferente de cero
                    if tf_idfs[word][i] == 0:    
                        cont +=1
                    i += 1
                    
                # si algun los TF-IDF es diferente de cero, se agrega a la lista de palabras
                if cont < len(tf_idfs[word]):
                    new_doc = append_cpp(new_doc,word)
        # se agrega el documento a la lista de documentos
        new_docs = append_cpp(new_docs,new_doc)
    
    return new_docs

def ejercicio1_byc(corpus,thresh):
    # obtenemos un dict con los dos TF-IDF por palabra
    tf_idfs = get_tf_idf(corpus)

    new_docs = [] # lista de documentos a regresar
    for doc in corpus:
        new_doc =[] # nuevo documento
        for word in doc:
            # verificar que no se agreguen palabras duplicadas
            if word not in new_doc:
                i = 0
                cont = 0
                # se itera la lista de TF-IDFs de la palabra en el diccionario
                while i < len(tf_idfs[word]): 
                    # se registra el número de veces que aparece algo mayor a thresh
                    if tf_idfs[word][i] >= thresh:
                        cont +=1
                    i += 1
                # si se encontró al menos un TF-IDF mayor a thresh, se agrega la palabra
                if cont > 0:
                    new_doc = append_cpp(new_doc,word)
        # se agrega el documento a la lista de documentos
        new_docs = append_cpp(new_docs,new_doc)
    
    return new_docs



def practica2(document):

    # se remueven las stopwords del documento
    document = remove_stopwords(document)
    vocabulary = {}
    
    for word in document:
        # crear diccionario de palabras
        if word not in vocabulary.keys():
            vocabulary[word] = None
    
    # contador para mantener índice
    cont = 0
    for key in vocabulary.keys():
        # se crea vector de ceros
        one_hot = [0]*len(vocabulary)
        # se coloca un 1 en el índice de one-hot correspondiente a la palabra 
        one_hot[cont] = 1
        # se le asigna el vector al vocabulario en la llave de la palabra 
        vocabulary[key] = one_hot
        cont += 1
    return vocabulary

if __name__ == "__main__":
    #doc_1 = input("Inserte oración 1: ")
    doc_1 = "Caro pregunta por una oración que pueda contener bajos puntajes para cada una de las oraciones. Caro pregunta bien."
    #doc_2 = input("Inserte oración 1: ")
    doc_2 = "Nadie preguntó lo que Caro si hizo, Caro y su equipo terminarán. Lo que otros no. Lo que le dará ventaja"
    
    corpus = [tokenize(doc_1),tokenize(doc_2)]
    tf_idfs = get_tf_idf(corpus)

    

    print(" -- Ejercicio 1  a) --")
    print(ejercicio1_a(corpus))

    print("\nPalabras eliminadas: ")
    for word in tf_idfs.keys():
        if np.sum(tf_idfs[word]) ==0:
            print(word)
    


    print("\n -- Ejercicio 1 b) --")
    print(ejercicio1_byc(corpus,0.01))
    print("\nPalabras eliminadas: ")
    for word in tf_idfs.keys():
        if tf_idfs[word][0] < 0.01 and tf_idfs[word][1] < 0.01:
            print(word)

    print("\n -- Ejercicio 1 c) --")
    print(ejercicio1_byc(corpus,0.5))
    print("\nPalabras eliminadas: ")
    list = []
    for word in tf_idfs.keys():
        if tf_idfs[word][0] < 0.5 and tf_idfs[word][1] < 0.5:
            list = append_cpp(list,word)
    print(list)          

    print("\n -- Ejercicio 2 --")
    print("Oración original: ",doc_1,"\n")
    vocabulary = practica2(tokenize(doc_1))
    for key in vocabulary.keys():
        print(key,vocabulary[key],"\n")
    