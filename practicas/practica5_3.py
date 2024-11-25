import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
import tokelib

nltk.download('wordnet')

def construir_lista_adyacencia(palabra):
    print(palabra)
    stack = [wn.synsets(palabra)[0]]
    lista_adyacencia = {}
    while stack:
        actual = stack.pop()
        lista_adyacencia[actual] = []
        for hiper in actual.hypernyms():
            lista_adyacencia[actual].append(hiper)
            stack.append(hiper)
    return lista_adyacencia

def construir_grafo(lista_adyacencia):
    G = nx.DiGraph()
    for key in lista_adyacencia.keys():
        G.add_node(key)
        for hijo in lista_adyacencia[key]:
            G.add_edge(key, hijo)  # Invertir la dirección de la arista
    return G

def unir_listas(lista_adyacencia1, lista_adyacencia2):
    lista_final = {}
    nodos = set(list(lista_adyacencia1.keys()) + list(lista_adyacencia2.keys()))
    for nodo in nodos:
        hijos = list(set(lista_adyacencia1.get(nodo, []) + lista_adyacencia2.get(nodo, [])))
        lista_final[nodo] = hijos
    return lista_final

def plot_graph(G):
    plt.figure(figsize=(10,10))
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_size=10)
    plt.show()

def plot_graph_hierarchy(G):
    plt.figure(figsize=(10, 10))
    pos = graphviz_layout(G, prog='dot')  # 'dot' genera una disposición jerárquica
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_size=10)
    plt.show()

def get_path_to_root(synset, adj_list):
    path = [synset]
    while True:
        parents = adj_list.get(synset, [])
        if not parents:
            break
        synset = parents[0]
        path.insert(0, synset)
    return path

def calculate_lca_depth(synset1, synset2, adj_list):
    path1 = get_path_to_root(synset1, adj_list)
    path2 = get_path_to_root(synset2, adj_list)
    
    lca = None
    depth = 0
    for s1, s2 in zip(path1, path2):
        if s1 == s2:
            lca = s1
            depth += 1
        else:
            break
    return lca, depth - 1

def profundidad_synset(synset, adj_list):

    path = get_path_to_root(synset, adj_list)
    return len(path) - 1

def similitud(profundidad1, profundidad2, profundidad_lca):
    return (2 * profundidad_lca) / (profundidad1 + profundidad2)

def run():
    oracion1 = "The cat sits on the mat."
    oracion2 = "The dog barks at the moon."
    oracion3 = "Birds are flying in the sky."
    oracion4 = "Fish swim in the water."

    palabra_usuario = "Dog"
    listaA_palabra_usuario = construir_lista_adyacencia(palabra_usuario)

    oraciones = [oracion1,oracion2, oracion3, oracion4]
    for oracion in oraciones:
        oracion = tokelib.tokenize(oracion)
        oracion = tokelib.remove_stopwords(oracion, english=True)
        vector_similitud = []
        for letra in oracion:
            listaA_letra = construir_lista_adyacencia(letra)
            lista = unir_listas(listaA_palabra_usuario, listaA_letra)
            lca, profundidad_lca = calculate_lca_depth(wn.synsets(palabra_usuario)[0],wn.synsets(letra)[0], lista)
            profundidad_letra = profundidad_synset(wn.synsets(letra)[0], lista)
            profundidad_usuario = profundidad_synset(wn.synsets(palabra_usuario)[0], lista)
            sim = similitud(profundidad_letra, profundidad_usuario, profundidad_lca)
            vector_similitud = tokelib.append_cpp(vector_similitud, sim)

        print(vector_similitud)

if __name__ == '__main__':
    run()
