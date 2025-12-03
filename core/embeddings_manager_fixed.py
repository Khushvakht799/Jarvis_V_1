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
        
        verbs = {
            "создать": ["create", "make"],
            "выполнить": ["execute", "run"],
            "посчитать": ["calculate", "compute"],
            "импортировать": ["import", "load"],
            "показать": ["show", "display"],
            "сохранить": ["save", "store"],
            "удалить": ["delete", "remove"],
            "найти": ["find", "search"],
            "привет": ["hello", "hi"],
            "старт": ["start", "begin"]
        }
        
        vocab = {}
        reverse_vocab = {}
        emb_list = []
        
        for idx, (verb, synonyms) in enumerate(verbs.items()):
            vocab[verb] = idx
            reverse_vocab[idx] = verb
            
            # ИСПРАВЛЕННЫЙ ЭМБЕДДИНГ
            verb_hash = hashlib.md5(verb.encode()).digest()
            seed = int.from_bytes(verb_hash[:4], "little")
            
            np.random.seed(seed)
            emb = np.random.randn(384).astype(np.float32)
            
            norm = np.linalg.norm(emb)
            if norm > 0:
                emb = emb / norm
            else:
                emb = emb * 0.0 + 0.1
            
            emb_list.append(emb)
        
        embeddings = np.array(emb_list)
        
        np.save("data/embeddings/verb_embeddings_fixed.npy", embeddings)
        with open("data/embeddings/verb_vocab_fixed.pkl", "wb") as f:
            pickle.dump({"vocab": vocab, "reverse_vocab": reverse_vocab}, f)
        
        print(f"✅ Создано {len(vocab)} нормализованных эмбеддингов")
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
            norm = np.linalg.norm(emb)
            if norm > 0:
                emb = emb / norm
        
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm
        
        return emb
    
    def find_similar(self, query, top_k=5):
        q_emb = self.get_embedding(query)
        
        q_norm = np.linalg.norm(q_emb)
        if q_norm > 0:
            q_emb = q_emb / q_norm
        
        similarities = []
        for i, emb in enumerate(self.embeddings):
            emb_norm = np.linalg.norm(emb)
            if emb_norm > 0:
                emb_normalized = emb / emb_norm
            else:
                emb_normalized = emb
            
            similarity = np.dot(q_emb, emb_normalized)
            similarities.append((i, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, similarity in similarities[:top_k]:
            if similarity > 0.1:
                verb = self.reverse_vocab[idx]
                results.append((verb, float(similarity)))
        
        return results
    
    def get_vocab_size(self):
        return len(self.vocab)
