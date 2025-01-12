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
        
        self.embeddings = np.random.uniform(-0.1, 0.1, (self.vocabulary_size, self.embedding_dim))
        self.context_weights = np.random.uniform(-0.1, 0.1, (self.vocabulary_size, self.embedding_dim))
    
    def get_context_words(self, sentence, position):
        start = max(0, position - self.window_size)
        end = min(len(sentence), position + self.window_size + 1)
        context = []
        for i in range(start, end):
            if i != position:
                context.append(sentence[i])
        return context
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -10, 10)))
    
    def train_step(self, target_idx, context_idx):
        hidden_layer = self.embeddings[target_idx]
        output = np.dot(self.context_weights[context_idx], hidden_layer)
        output = self.sigmoid(output)
        print(output)
        
        error = output - 1.0
        
        grad_weights = error * hidden_layer
        grad_hidden = error * self.context_weights[context_idx]
        
        self.embeddings[target_idx] -= self.learning_rate * grad_hidden
        self.context_weights[context_idx] -= self.learning_rate * grad_weights
    
    def train(self, corpus_list, epochs=5):
        for epoch in range(epochs):
            word_pairs = 0
            
            for corpus in corpus_list:
                for i in range(len(corpus)):
                    target_word = corpus[i]
                    context_words = self.get_context_words(corpus, i)
                    
                    if target_word in self.word_to_idx:
                        target_idx = self.word_to_idx[target_word]
                        for context_word in context_words:
                            if context_word in self.word_to_idx:
                                context_idx = self.word_to_idx[context_word]
                                self.train_step(target_idx, context_idx)
                                word_pairs += 1
            
            print(f'Epoch {epoch + 1}/{epochs}')
