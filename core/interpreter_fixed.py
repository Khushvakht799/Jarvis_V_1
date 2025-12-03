# Добавь в начало файла core/interpreter.py после импортов:

import json
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
import numpy as np

from .embeddings_manager import VerbEmbeddings
import config

class EmbeddingInterpreter:
    """Исправленный интерпретатор"""
    
    def __init__(self):
        self.embeddings = VerbEmbeddings(config.EMBEDDINGS_DIR)
        self.similarity_threshold = getattr(config, 'SIMILARITY_THRESHOLD', 0.3)
        self.cache = {}
        self.load_patterns()
    
    def load_patterns(self):
        """Загружает ВСЕ паттерны из файла"""
        self.patterns = []
        
        if not config.PATTERNS_FILE.exists():
            print("⚠️  patterns.json не найден")
            return
        
        try:
            with open(config.PATTERNS_FILE, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            
            self.patterns = data.get("patterns", [])
            print(f"✅ Загружено {len(self.patterns)} паттернов")
            
        except Exception as e:
            print(f"❌ Ошибка загрузки patterns.json: {e}")
    
    def interpret(self, user_input: str):
        """Упрощенный поиск - сначала точное совпадение, потом эмбеддинги"""
        user_input_lower = user_input.lower()
        
        # 1. Точное совпадение по подстроке
        for pattern in self.patterns:
            for trigger in pattern.get("triggers", []):
                if trigger.lower() in user_input_lower:
                    variables = self.extract_variables(user_input, pattern.get("template", ""))
                    return pattern.get("template", ""), variables, 1.0
        
        # 2. Если не нашли, возвращаем None
        return None
    
    def extract_variables(self, user_input: str, template: str):
        """Извлекает переменные"""
        variables = {}
        import re
        
        numbers = re.findall(r'\b\d+\b', user_input)
        if numbers:
            if "{n}" in template:
                variables["n"] = int(numbers[0])
            if "{start}" in template:
                variables["start"] = int(numbers[0])
            if "{end}" in template and len(numbers) > 1:
                variables["end"] = int(numbers[1])
        
        return variables
    
    def get_vocab_size(self):
        return self.embeddings.get_vocab_size()
