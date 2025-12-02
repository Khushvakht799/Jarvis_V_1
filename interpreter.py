import json
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
import numpy as np

from .embeddings_manager import VerbEmbeddings

# Пробуем импортировать config разными способами
try:
    import config
except ImportError:
    # Если config не найден в корне, создаем минимальный
    import os
    from pathlib import Path
    
    class Config:
        BASE_DIR = Path(__file__).parent.parent.parent
        DATA_DIR = BASE_DIR / "data"
        EMBEDDINGS_DIR = DATA_DIR / "embeddings"
        PATTERNS_FILE = DATA_DIR / "patterns.json"
        ERROR_DB_FILE = DATA_DIR / "error_db.json"
        SIMILARITY_THRESHOLD = 0.7
    
    config = Config()

class EmbeddingInterpreter:
    def __init__(self):
        self.embeddings = VerbEmbeddings(config.EMBEDDINGS_DIR)
        self.similarity_threshold = config.SIMILARITY_THRESHOLD
        self.cache = {}
        self.load_patterns()
    
    def load_patterns(self):
        self.patterns = []
        if config.PATTERNS_FILE.exists():
            with open(config.PATTERNS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.patterns = data.get('patterns', [])
    
    def interpret(self, user_input: str) -> Optional[Tuple[str, Dict, float]]:
        cache_key = user_input.lower()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        if not self.patterns:
            return None
        
        best_pattern = None
        best_similarity = 0
        
        for pattern in self.patterns:
            for trigger in pattern.get('triggers', []):
                trigger_embedding = self.embeddings.get_embedding(trigger)
                user_embedding = self.embeddings.get_embedding(user_input)
                
                similarity = np.dot(trigger_embedding, user_embedding) / (
                    np.linalg.norm(trigger_embedding) * np.linalg.norm(user_embedding) + 1e-10
                )
                
                if similarity > best_similarity and similarity >= self.similarity_threshold:
                    best_similarity = similarity
                    best_pattern = pattern
        
        if best_pattern:
            variables = self.extract_variables_from_input(user_input, best_pattern.get('template', ''))
            response = (best_pattern.get('template', ''), variables, best_similarity)
            self.cache[cache_key] = response
            return response
        
        return None
    
    def extract_variables_from_input(self, user_input: str, template: str) -> Dict:
        variables = {}
        numbers = re.findall(r'\b\d+\b', user_input)
        if numbers:
            if '{n}' in template or '{count}' in template or '{number}' in template:
                variables['n'] = int(numbers[0])
                variables['count'] = int(numbers[0])
                variables['number'] = int(numbers[0])
        
        strings = re.findall(r'[\"\'](.*?)[\"\']', user_input)
        if strings and '{text}' in template:
            variables['text'] = strings[0]
            variables['string'] = strings[0]
        
        return variables
    
    def learn_new_command(self, user_input: str, python_code: str) -> Dict:
        print(f\"🎓 Изучаю новую команду: '{user_input}'\")
        
        new_pattern = {
            \"id\": f\"cmd_{len(self.patterns) + 1}\",
            \"triggers\": [user_input],
            \"template\": python_code,
            \"variables\": {},
            \"category\": \"user_defined\"
        }
        
        self.patterns.append(new_pattern)
        self.save_patterns()
        
        words = user_input.lower().split()
        for word in words:
            if len(word) > 3:
                self.embeddings.add_new_verb(word)
        
        self.cache.clear()
        return new_pattern
    
    def get_verb_similarities(self, verb: str, top_k: int = 5):
        return self.embeddings.find_similar_verbs(verb, top_k)
    
    def get_vocab_size(self) -> int:
        return len(self.embeddings.vocab)
    
    def save_patterns(self):
        data = {
            \"patterns\": self.patterns,
            \"statistics\": {\"total_uses\": 0, \"last_updated\": \"\"}
        }
        with open(config.PATTERNS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)