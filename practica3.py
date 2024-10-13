import numpy as np
def is_special(word):
    sc = ["Á", "É", "Í", "Ó", "Ú", "á", "é", "í", "ó","ñ","ú"]
    
    if word in sc : 
        return True 
    else:
        return False

def is_alpha(word):
    return (65 <= ord(word) <= 90) or (97 <= ord(word) <= 122)

def is_stopword(word):
    stopwords = ["el", "y", "eso", "la", "los", "las" ,"de","en","a","un","uno","una","es","con","es","con","para","al","del"]

    if word in stopwords:
        return True
    else:
        return False  
    

def to_lower(letter):
    if(65 <= ord(letter) <= 90):
        return chr(ord(letter) + 32)
    else:
        return letter

def is_numeric(letter):
    if(48 <= ord(letter) <= 57):
        return True
    else:
        return False
    

def tf_idf(documents,test_word):
    tf_idf = []
    word_count = 0
    for doc in documents:
        cont = 0
        for word in doc:
            if word == test_word:
                cont+=1      
        if cont > 0 :
            word_count += 1       
        tf = cont/len(doc)
        tf_idf.append(tf)
    
    idf = np.log10(len(documents)/word_count)

    for i in range(0,len(tf_idf)):
        tf_idf[i] = tf_idf[i]*idf
    
    return tf_idf

def remove_stopwords(doc):
    new_doc = []
    for word in doc:
        if not is_stopword(word):
            new_doc.append(word)
    return new_doc


def tokenize(texto):
    i = 0
    tokens = []
    token = ""
    
    while i < len(texto):
        if is_special(texto[i]) or is_alpha(texto[i]) or is_numeric(texto[i]):
            
            token += to_lower(texto[i])
        elif texto[i] == ' ':
            if token != "":
                
                tokens += [token]
            token = ""
        i += 1
    
    if token:    
        tokens += [token]
        
    return tokens

def practica1(docs,inciso):

    if inciso == "a":
        new_docs =[]
        for doc in docs:
            new_doc = []
            for word in doc:
                if tf_idf(docs,word)[0] != 0 or tf_idf(docs,word)[1] != 0:
                    new_doc.append(word)
            new_docs.append(new_doc)

    elif inciso == "b":
        new_docs =[]
        for doc in docs:
            new_doc = []
            for word in doc:
                if tf_idf(docs,word)[0] >= 0.1 or tf_idf(docs,word)[1] >= 0.1:
                    new_doc.append(word)
            new_docs.append(new_doc)

    else:
        new_docs =[]
        for doc in docs:
            new_doc = []
            for word in doc:
                if tf_idf(docs,word)[0] >= 0.5 or tf_idf(docs,word)[1] >= 0.5:
                    new_doc.append(word)
            new_docs.append(new_doc)
    return new_docs

def practica2(corpus):
    corpus = remove_stopwords(corpus)
    vocabulary = {}
    
    for word in corpus:
        if word not in vocabulary:
            vocabulary[word] = None
    
    cont = 0
    for key in vocabulary.keys():
        one_hot = [0]*len(vocabulary)
        one_hot[cont] = 1
        vocabulary[key] = one_hot
        cont += 1
    return vocabulary

if __name__ == "__main__":
    #doc_1 = input("Inserte oración 1: ")
    doc_1 = "Caro pregunta por una oración que pueda contener bajos puntajes para cada una de las oraciones. Caro pregunta bien."
    #doc_2 = input("Inserte oración 1: ")
    doc_2 = "Nadie preguntó lo que Caro si hizo, Caro y su equipo terminarán. Lo que otros no. Lo que le dará ventaja"
    inciso = "b"
    corpus = tokenize(doc_1) + tokenize(doc_2)

    print(" -- Ejercicio 1  --")
    new = practica1([tokenize(doc_1),tokenize(doc_2)],inciso)
    print(new)

    print(" -- Ejercicio 2  --")
    vocab = practica2(tokenize(doc_1))
    for key in vocab.keys():
        print(f'{key}: {vocab[key]}')
    
