import tokelib
import nltk
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
import networkx as nx

nltk.download('wordnet')

#a) Dadas al menos 4 oraciones, determinar con wordnet el grado de similitud de cada palabra con 1 ingresada
#por el usuario.

def construir_lista_adyacencia(palabra):
    stack = [wn.synsets(palabra)[0]]
    lista_adyacencia = {}
    while stack:
        actual = stack.pop()
        lista_adyacencia[actual] = []
        for hiper in actual.hypernyms():
            lista_adyacencia[actual].append(hiper)
            stack.append(hiper)
    print(f"---{palabra}---")
    for key in lista_adyacencia.keys():
        print(key, lista_adyacencia[key])
    return lista_adyacencia

def run():
    oracion1 = "The cat sits on the mat."
    oracion2 = "The dog barks at the moon."
    oracion3 = "Birds are flying in the sky."
    oracion4 = "Fish swim in the water."

    palabra_usuario = "Dog"

    palabra_lower = ""
    for c in palabra_usuario:
        palabra_lower += tokelib.to_lower(c)

    oraciones = [oracion1,oracion2,oracion3,oracion4]

    oraciones_toke = [tokelib.tokenize(oracion) for oracion in oraciones]
    oraciones_stopwords = [tokelib.remove_stopwords(oracion, english=True) for oracion in oraciones_toke]

    lista_adyacencia_palabra = construir_lista_adyacencia(palabra_usuario)
    
    for oracion in oraciones_stopwords:
        listas = []
        for palabra in oracion:
            listas.append(construir_lista_adyacencia(palabra))

if __name__ == '__main__':
    run()