import numpy as np
import tokelib as tk

class Word2Vec:
    def __init__(self, window_size, embedding_dim, learning_rate):
        self.window_size = window_size
        self.embedding_dim = embedding_dim
        self.learning_rate = learning_rate
        self.word_to_idx = {}
        self.idx_to_word = {}
        self.vocabulary_size = 0
        self.embeddings = None
        self.context_weights = None
    
    def build_vocabulary(self, corpus_list):
        all_words = []
        for corpus in corpus_list:
            all_words.extend(corpus)
        
        vocabulary = tk.get_vocabulary(all_words, is_nested=False)
        
        self.word_to_idx = tk.get_word_index(vocabulary)
        self.idx_to_word = {idx: word for word, idx in self.word_to_idx.items()}
        self.vocabulary_size = len(vocabulary)
        
        # Random iniciales, dist uniforme dim vocabulario y embeddings
        self.embeddings = np.random.uniform(-0.1, 0.1, (self.vocabulary_size, self.embedding_dim))
        self.context_weights = np.random.uniform(-0.1, 0.1, (self.vocabulary_size, self.embedding_dim))
    
    def get_context_words(self, sentence, position):
        start = max(0, position - self.window_size) # max para no salirse del window size
        end = min(len(sentence), position + self.window_size + 1) # same
        context = []
        for i in range(start, end):
            if i != position:
                context.append(sentence[i])
        return context
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -10, 10)))
    
    def train_step(self, target_idx, context_idx):
        """
            vector de destino
            vector de contexto

            score alto -> vectores parecidos ||
            score bajo -> vectores no parecidos -|
        """
        vector_target = self.embeddings[target_idx]
        score = np.dot(self.context_weights[context_idx], vector_target)
        score = self.sigmoid(score)
        #print(score)
        
        error = score - 1.0 # goal -> 1, - f + n
        
        grad_weights = error * vector_target
        grad_hidden = error * self.context_weights[context_idx]
        
        self.embeddings[target_idx] -= self.learning_rate * grad_hidden
        self.context_weights[context_idx] -= self.learning_rate * grad_weights
    
    def train(self, corpus_list, epochs=5):
        for epoch in range(epochs):            
            for corpus in corpus_list:
                for i in range(len(corpus)):
                    target_word = corpus[i]
                    context_words = self.get_context_words(corpus, i)
                    target_idx = self.word_to_idx[target_word]
                    for context_word in context_words:
                        context_idx = self.word_to_idx[context_word]
                        self.train_step(target_idx, context_idx)
            
            print(f'Epoch {epoch + 1}/{epochs}')
