# debug_interpreter.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("🔍 Диагностика интерпретатора...")

class Config:
    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(BASE_DIR, "data")
    EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")
    PATTERNS_FILE = os.path.join(DATA_DIR, "patterns.json")
    ERROR_DB_FILE = os.path.join(DATA_DIR, "error_db.json")
    SIMILARITY_THRESHOLD = 0.3

config = Config()

# 1. Проверяем patterns.json
print("\n1. Проверка patterns.json...")
import json
if os.path.exists(config.PATTERNS_FILE):
    with open(config.PATTERNS_FILE, 'r', encoding='utf-8') as f:
        patterns_data = json.load(f)
    print(f"   Файл существует, паттернов: {len(patterns_data.get('patterns', []))}")
    for p in patterns_data.get('patterns', []):
        print(f"   - {p['id']}: {p['triggers']}")
else:
    print("   ❌ Файл не существует!")

# 2. Проверяем embeddings
print("\n2. Проверка embeddings...")
from core.embeddings_manager import VerbEmbeddings
embeddings = VerbEmbeddings(config.EMBEDDINGS_DIR)
print(f"   Словарь: {embeddings.get_vocab_size()} глаголов")
print("   Примеры глаголов:", list(embeddings.vocab.keys())[:5])

# 3. Тестируем поиск напрямую
print("\n3. Тестируем поиск похожих глаголов...")
test_queries = ["привет", "создай", "посчитай", "hello", "create"]

for query in test_queries:
    similar = embeddings.find_similar(query, top_k=3)
    print(f"   '{query}': {similar}")

# 4. Проверяем интерпретатор напрямую
print("\n4. Проверка интерпретатора...")
from core.interpreter import EmbeddingInterpreter
interpreter = EmbeddingInterpreter()

print(f"   Загружено паттернов: {len(interpreter.patterns)}")

# 5. Тестируем interpret метод
print("\n5. Тестируем метод interpret():")
for query in test_queries:
    result = interpreter.interpret(query)
    if result:
        template, vars, score = result
        print(f"   '{query}' -> Найдено ({score:.1%}): {template[:40]}...")
    else:
        print(f"   '{query}' -> Не найдено")

# 6. Проверяем SIMILARITY_THRESHOLD
print(f"\n6. SIMILARITY_THRESHOLD = {interpreter.similarity_threshold}")