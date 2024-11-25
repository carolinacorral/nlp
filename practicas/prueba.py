import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


nltk.download('wordnet')

def construir_lista_adyacencia(palabra):
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
            G.add_edge(hijo, key)
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
    pos = graphviz_layout(G, prog='dot')
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
    palabra1 = "doctor"
    palabra2 = "nurse"

    palabra1 = "dog"
    palabra2 = "birds"

    la1 = construir_lista_adyacencia(palabra1)
    la2 = construir_lista_adyacencia(palabra2)
    lista = unir_listas(la1,la2)

    lca, profundidad = calculate_lca_depth(wn.synsets(palabra1)[0],wn.synsets(palabra2)[0], lista)
    profundidad1 = profundidad_synset(wn.synsets(palabra1)[0],lista)
    profundidad2 = profundidad_synset(wn.synsets(palabra2)[0],lista)

    print("Profundidad1: ", palabra1, profundidad1)
    print("Profundidad2: ", palabra2, profundidad2)
    print("Profundidad lca: ", profundidad)
    print("LCA: ",lca)
    print("Similitud: ", similitud(profundidad1, profundidad2, profundidad))
    g = construir_grafo(lista)
    plot_graph_hierarchy(g)

if __name__ == '__main__':
    run()