import math
from nltk.corpus import wordnet as wn
import nltk

nltk.download('wordnet')
nltk.download('punkt')

def tokenize(text):
    return text.lower().replace('.', '').replace(',', '').split()

def compute_tf(document):
    tf = {}
    total_words = len(document)
    for word in document:
        if word in tf:
            tf[word] += 1
        else:
            tf[word] = 1
    for word in tf:
        tf[word] /= total_words
    return tf

def compute_idf(documents):
    idf = {}
    total_documents = len(documents)
    for document in documents:
        for word in set(document):
            if word in idf:
                idf[word] += 1
            else:
                idf[word] = 1
    for word in idf:
        idf[word] = math.log10(total_documents / idf[word])
    return idf

def compute_tf_idf(document, idf):
    tf = compute_tf(document)
    tf_idf = {}
    for word in tf:
        tf_idf[word] = tf[word] * idf.get(word, 0)
    return tf_idf

def cosine_similarity(vec1, vec2):
    dot_product = sum(vec1[word] * vec2.get(word, 0) for word in vec1)
    norm1 = math.sqrt(sum(value ** 2 for value in vec1.values()))
    norm2 = math.sqrt(sum(value ** 2 for value in vec2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)

tema = "Nurse"
corpus = "I give some medical treatment to another people."

toke_corpus = tokenize(corpus)

synsets = wn.synsets(tema)
definitions = [synset.definition() for synset in synsets]

tokenized_definitions = [tokenize(definition) for definition in definitions]

documents = [toke_corpus] + tokenized_definitions

idf = compute_idf(documents)

tf_idf_corpus = compute_tf_idf(toke_corpus, idf)
tf_idf_definitions = [compute_tf_idf(definition, idf) for definition in tokenized_definitions]

max_similarity = -1
best_definition = ""

for idx, definition in enumerate(tf_idf_definitions):
    cosine_sim = cosine_similarity(tf_idf_corpus, definition)
    if cosine_sim > max_similarity:
        max_similarity = cosine_sim
        best_definition = definitions[idx]

print(f"Best definition: {best_definition}")
print(f"Maximum cosine similarity: {max_similarity}")
