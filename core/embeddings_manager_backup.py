import numpy as np
import pickle
import hashlib
from sklearn.metrics.pairwise import cosine_similarity

class VerbEmbeddings:
    def __init__(self, embeddings_dir):
        import os
        os.makedirs(embeddings_dir, exist_ok=True)
        self.embeddings, self.vocab, self.reverse_vocab = self.create_embeddings()
    
    def create_embeddings(self):
        print("🔄 Создание embedding-ового словаря глаголов...")
        
        # ПРАВИЛЬНЫЙ словарь с нормальной кодировкой
        verbs = {
            'создать': ['create', 'make', 'build', 'generate'],
            'выполнить': ['execute', 'run', 'perform', 'do'],
            'посчитать': ['calculate', 'compute', 'count', 'sum'],
            'импортировать': ['import', 'load', 'include', 'require'],
            'показать': ['show', 'display', 'print', 'output'],
            'сохранить': ['save', 'store', 'write', 'export'],
            'удалить': ['delete', 'remove', 'erase', 'clear'],
            'найти': ['find', 'search', 'locate', 'discover'],
            'отсортировать': ['sort', 'order', 'filter', 'arrange'],
            'объединить': ['merge', 'combine', 'join', 'concatenate'],
            'проверить': ['check', 'verify', 'test', 'validate'],
            'генерировать': ['generate', 'produce', 'create', 'make'],
            'привет': ['hello', 'hi', 'greet', 'welcome'],
            'запустить': ['start', 'launch', 'begin', 'initiate'],
            'остановить': ['stop', 'halt', 'end', 'finish']
        }
        
        vocab = {}
        reverse_vocab = {}
        emb_list = []
        
        for idx, (verb, synonyms) in enumerate(verbs.items()):
            vocab[verb] = idx
            reverse_vocab[idx] = verb
            
            # Простой эмбеддинг
            h = hashlib.md5(verb.encode()).digest()
            emb = np.frombuffer(h[:16], dtype=np.float32)
            emb = np.pad(emb, (0, 384 - len(emb)), 'constant')
            emb = emb / (np.linalg.norm(emb) + 1e-10)
            emb_list.append(emb)
        
        embeddings = np.array(emb_list)
        
        # Сохраняем
        np.save("data/embeddings/verb_embeddings.npy", embeddings)
        with open("data/embeddings/verb_vocab.pkl", 'wb') as f:
            pickle.dump({'vocab': vocab, 'reverse_vocab': reverse_vocab}, f)
        
        print(f"✅ Создано {len(vocab)} эмбеддингов")
        return embeddings, vocab, reverse_vocab
    
    def get_embedding(self, text):
        words = text.lower().split()
        verb_embs = []
        
        for word in words:
            if word in self.vocab:
                idx = self.vocab[word]
                verb_embs.append(self.embeddings[idx])
        
        if verb_embs:
            emb = np.mean(verb_embs, axis=0)
        else:
            emb = np.random.randn(384).astype(np.float32)
            emb = emb / (np.linalg.norm(emb) + 1e-10)
        
        return emb / (np.linalg.norm(emb) + 1e-10)
    
    def find_similar(self, query, top_k=5):
        q_emb = self.get_embedding(query)
        sims = cosine_similarity(q_emb.reshape(1, -1), self.embeddings)[0]
        
        indices = np.argsort(sims)[::-1][:top_k]
        results = []
        for idx in indices:
            if sims[idx] > 0.3:
                verb = self.reverse_vocab[idx]
                results.append((verb, float(sims[idx])))
        
        return results
    
    def get_vocab_size(self):
        return len(self.vocab)