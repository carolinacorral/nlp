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
    elif is_special(letter):
        special = ["Á", "É", "Í", "Ó", "Ú","Ñ"]
        special_lower = ["á","é","í","ó","ú","ñ"]
        return special_lower[special.index(letter)]
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

def append_cpp(array, element):
    current_length = len(array)
    
    new_array = [None] * (current_length + 1)
    
    for i in range(current_length):
        new_array[i] = array[i]
    
    new_array[current_length] = element
    
    return new_array

def tokenize(texto,parser = ' ',include_numbers = False):
    i = 0
    tokens = []
    token = ""
    
    if include_numbers:
        while i < len(texto):
            if is_special(texto[i]) or is_alpha(texto[i]) or is_numeric(texto[i]):

                token += to_lower(texto[i])
            elif texto[i] == parser:
                if token != "":
                    
                    tokens += [token]
                token = ""
            i += 1
    else:
        while i < len(texto):
            if is_special(texto[i]) or is_alpha(texto[i]):

                token += to_lower(texto[i])
            elif texto[i] == parser:
                if token != "":

                    tokens += [token]
                token = ""
            i += 1
    
    if token:    
        tokens += [token]
        
    return tokens

if __name__ == '__main__':
    print(to_lower("Á"))