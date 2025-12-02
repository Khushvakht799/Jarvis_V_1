import numpy as np
import pickle
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import hashlib
from sklearn.metrics.pairwise import cosine_similarity

class VerbEmbeddings:
    def __init__(self, embeddings_dir: Path):
        self.embeddings_dir = embeddings_dir
        self.embeddings_dir.mkdir(exist_ok=True)
        self.embeddings, self.vocab, self.reverse_vocab = self.load_or_create_embeddings()
        self.embedding_cache = {}
    
    def load_or_create_embeddings(self) -> Tuple[np.ndarray, Dict, Dict]:
        embeddings_file = self.embeddings_dir / \"verb_embeddings.npy\"
        vocab_file = self.embeddings_dir / \"verb_vocab.pkl\"
        
        if embeddings_file.exists() and vocab_file.exists():
            embeddings = np.load(embeddings_file)
            with open(vocab_file, 'rb') as f:
                vocab_data = pickle.load(f)
                vocab = vocab_data['vocab']
                reverse_vocab = vocab_data['reverse_vocab']
            print(f\"✅ Загружено {len(vocab)} эмбеддингов глаголов\")
            return embeddings, vocab, reverse_vocab
        else:
            return self.create_initial_embeddings()
    
    def create_initial_embeddings(self) -> Tuple[np.ndarray, Dict, Dict]:
        print(\"🔄 Создание embedding-ового словаря глаголов...\")
        
        base_verbs = {
            'создать': ['create', 'make', 'build'],
            'выполнить': ['execute', 'run', 'perform'],
            'посчитать': ['calculate', 'compute', 'count'],
            'импортировать': ['import', 'load', 'include'],
            'показать': ['show', 'display', 'print'],
            'сохранить': ['save', 'store', 'write'],
            'удалить': ['delete', 'remove', 'erase'],
            'найти': ['find', 'search', 'locate'],
            'отфильтровать': ['filter', 'sort', 'organize'],
            'объединить': ['merge', 'combine', 'join'],
            'create': ['создать', 'сделать'],
            'execute': ['выполнить', 'запустить'],
            'calculate': ['посчитать', 'вычислить'],
            'import': ['импортировать', 'загрузить'],
        }
        
        vocab = {}
        reverse_vocab = {}
        embeddings_list = []
        
        for idx, (verb, synonyms) in enumerate(base_verbs.items()):
            vocab[verb] = idx
            reverse_vocab[idx] = verb
            verb_hash = hashlib.md5(verb.encode()).digest()
            embedding = np.frombuffer(verb_hash[:16], dtype=np.float32)
            embedding = np.pad(embedding, (0, 384 - len(embedding)), 'constant')
            embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
            embeddings_list.append(embedding)
        
        embeddings = np.array(embeddings_list)
        self.save_embeddings(embeddings, vocab, reverse_vocab)
        
        print(f\"✅ Создано {len(vocab)} начальных эмбеддингов\")
        return embeddings, vocab, reverse_vocab
    
    def save_embeddings(self, embeddings: np.ndarray, vocab: Dict, reverse_vocab: Dict):
        np.save(self.embeddings_dir / \"verb_embeddings.npy\", embeddings)
        with open(self.embeddings_dir / \"verb_vocab.pkl\", 'wb') as f:
            pickle.dump({'vocab': vocab, 'reverse_vocab': reverse_vocab}, f)
    
    def get_embedding(self, text: str) -> np.ndarray:
        if text in self.embedding_cache:
            return self.embedding_cache[text]
        
        words = text.lower().split()
        verb_embeddings = []
        for word in words:
            if word in self.vocab:
                idx = self.vocab[word]
                verb_embeddings.append(self.embeddings[idx])
        
        if verb_embeddings:
            embedding = np.mean(verb_embeddings, axis=0)
        else:
            embedding = np.random.randn(384).astype(np.float32)
            embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
        
        embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
        self.embedding_cache[text] = embedding
        return embedding
    
    def find_similar_verbs(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        query_embedding = self.get_embedding(query)
        similarities = cosine_similarity(
            query_embedding.reshape(1, -1),
            self.embeddings
        )[0]
        
        similar_indices = np.argsort(similarities)[::-1][:top_k]
        results = []
        for idx in similar_indices:
            if similarities[idx] > 0.3:
                verb = self.reverse_vocab[idx]
                results.append((verb, float(similarities[idx])))
        
        return results
    
    def add_new_verb(self, verb: str, synonyms: List[str] = None):
        if verb in self.vocab:
            return
        
        idx = len(self.vocab)
        self.vocab[verb] = idx
        self.reverse_vocab[idx] = verb
        embedding = self.get_embedding(verb)
        self.embeddings = np.vstack([self.embeddings, embedding])
        self.save_embeddings(self.embeddings, self.vocab, self.reverse_vocab)
        print(f\"✅ Добавлен новый глагол: '{verb}'\")
        
        if synonyms:
            for synonym in synonyms:
                if synonym not in self.vocab:
                    self.add_new_verb(synonym)