import json
import re
import numpy as np
from .embeddings_manager import VerbEmbeddings
import config

class EmbeddingInterpreter:
    def __init__(self):
        self.embeddings = VerbEmbeddings(config.EMBEDDINGS_DIR)
        self.threshold = config.SIMILARITY_THRESHOLD
        self.load_patterns()
    
    def load_patterns(self):
        self.patterns = [
            {
                "id": "hello",
                "triggers": ["РїСЂРёРІРµС‚", "hello"],
                "template": "result = 'РџСЂРёРІРµС‚! РЇ Jarvis.'"
            },
            {
                "id": "create_list",
                "triggers": ["СЃРѕР·РґР°Р№ СЃРїРёСЃРѕРє", "create list"],
                "template": "result = list(range(5))"
            }
        ]
    
    def interpret(self, user_input):
        best_match = None
        best_score = 0
        
        for pattern in self.patterns:
            for trigger in pattern["triggers"]:
                t_emb = self.embeddings.get_embedding(trigger)
                u_emb = self.embeddings.get_embedding(user_input)
                
                score = np.dot(t_emb, u_emb) / (np.linalg.norm(t_emb) * np.linalg.norm(u_emb) + 1e-10)
                
                if score > best_score and score >= self.threshold:
                    best_score = score
                    best_match = pattern
        
        if best_match:
            # РР·РІР»РµРєР°РµРј С‡РёСЃР»Р°
            vars = {}
            nums = re.findall(r'\b\d+\b', user_input)
            if nums and '{n}' in best_match["template"]:
                vars['n'] = int(nums[0])
            
            return best_match["template"], vars, best_score
        
        return None
    
    def get_verb_similarities(self, verb, top_k=5):
        return self.embeddings.find_similar(verb, top_k)
    
    def get_vocab_size(self):
        return self.embeddings.get_vocab_size()
