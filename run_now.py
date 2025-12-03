import sys
import os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))

# Своя реализация cosine_similarity
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2 + 1e-10)

# Монопатим embeddings_manager.py
import core.embeddings_manager as em
em.cosine_similarity = cosine_similarity

print("🚀 Запуск Jarvis (упрощенный)...")

from core.interpreter import EmbeddingInterpreter
from core.executor import CodeExecutor
from utils.file_manager import ensure_data_files

# Минимальный config
class Config:
    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(BASE_DIR, "data")
    EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")
    SIMILARITY_THRESHOLD = 0.7

config = Config()

ensure_data_files()
interpreter = EmbeddingInterpreter()
executor = CodeExecutor()

print(f"✅ Словарь: {interpreter.get_vocab_size()} глаголов")

while True:
    cmd = input("\nJarvis> ").strip()
    if cmd.lower() == 'exit':
        break
    
    result = interpreter.interpret(cmd)
    if result:
        template, vars, score = result
        print(f"✅ ({score:.1%}): {template}")
        
        code = template
        for k, v in vars.items():
            code = code.replace(f"{{{k}}}", str(v))
        
        success, output, res = executor.execute(code)
        if success:
            print(f"Результат: {res}")
        else:
            print(f"Ошибка: {output}")
    else:
        print("❌ Не распознано")