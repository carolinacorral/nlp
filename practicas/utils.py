import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import numpy as np
from scipy.spatial.distance import cdist
import tokelib as tk
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
from word2vec import Word2Vec

def read(filepath):
    import tokelib as tk
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()
    
    tokens = tk.tokenize(text)
    tokens = tk.remove_stopwords(tokens, english=True)
    return tokens

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
    vocabulary_clean = tk.remove_stopwords(vocabulary,english=True)
        
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

def graph(model, method, title, highlight_word, dimensions):

    vectors = model.embeddings
    words = [model.idx_to_word[i] for i in range(len(model.idx_to_word))]
    
    if method.lower() == 'pca':
        reducer = PCA(n_components=dimensions)
    else:
        reducer = TSNE(n_components=dimensions, random_state=42)
    
    reduced_vectors = reducer.fit_transform(vectors)
    
    df = {
        'x': reduced_vectors[:, 0],
        'y': reduced_vectors[:, 1],
        'word': words,
        'size': [8] * len(words),
        'color': ['lightblue'] * len(words),
    }

    fig = go.Figure()

    if highlight_word:
        word_idx = model.word_to_idx[highlight_word]
        df['size'][word_idx] = 20
        df['color'][word_idx] = 'red'

    fig.add_trace(go.Scatter(
        x=df['x'],
        y=df['y'],
        mode='markers+text',
        marker=dict(
            size=df['size'],
            color=df['color'],
            line=dict(width=1, color='DarkSlateGrey')
        ),
        text=df['word'],
        textposition="top center",
        hoverinfo='text',
        textfont=dict(size=10),
        name='Words'
    ))
    
    fig.update_layout(
        title=f'{method.upper()}',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=True, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=True, zeroline=False, showticklabels=False),
        template='plotly_white'
    )
    
    fig.show()

def main():
    rutas = [
        '/workspaces/nlp/practicas/etc/corpus_1.txt',
        '/workspaces/nlp/practicas/etc/corpus_2.txt',
        '/workspaces/nlp/practicas/etc/corpus_3.txt'
    ]
    
    corpus_list = [read(path) for path in rutas]
    
    model = Word2Vec(window_size=5, embedding_dim=100, learning_rate=0.01)

    model.build_vocabulary(corpus_list)
    
    model.train(corpus_list, epochs=100)
    
    while True:
        palabra = input("\nPalabra: ")
        if palabra.lower() == 'exit':
            break
            
        if palabra in model.word_to_idx:
            graph(model, method='pca', title='PCA', highlight_word=palabra, dimensions=2)
            graph(model, method='tsne', title='TSNE', highlight_word=palabra, dimensions=2)
        else:
            print(f"La palabra '{palabra}' no se encuentra en el vocabulario.")
            all_words = []
            for corpus in corpus_list:
                all_words.extend(corpus)
        
            vocabulary = tk.get_vocabulary(all_words, is_nested=False)
            max_similarity_score_word, max_similarity, max_sim_row = closest_word(palabra, vocabulary)
            print(max_similarity_score_word, max_similarity, max_sim_row)
            graph(model, method='pca', title='PCA', highlight_word=max_similarity_score_word, dimensions=2)
            graph(model, method='tsne', title='TSNE', highlight_word=max_similarity_score_word, dimensions=2)

if __name__ == "__main__":
    main()
