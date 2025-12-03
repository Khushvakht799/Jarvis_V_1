import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("🔍 Минимальная диагностика Jarvis")

# 1. Проверяем эмбеддинги
print("\n1. Проверка эмбеддингов:")
try:
    from core.embeddings_manager import VerbEmbeddings
    
    class Config:
        BASE_DIR = os.path.dirname(__file__)
        DATA_DIR = os.path.join(BASE_DIR, "data")
        EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")
    
    config = Config()
    embeddings = VerbEmbeddings(config.EMBEDDINGS_DIR)
    print(f"✅ Словарь: {embeddings.get_vocab_size()} глаголов")
    
    # Тест
    test = embeddings.find_similar("создать", top_k=2)
    print(f"   Поиск 'создать': {test}")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
print("\n2. Проверка patterns.json:")
import json
patterns_file = "data/patterns.json"
if os.path.exists(patterns_file):
    try:
        with open(patterns_file, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        patterns = data.get("patterns", [])
        print(f"✅ Файл есть, паттернов: {len(patterns)}")
        
        # Проверяем первый паттерн
        if patterns:
            print(f"   Первый паттерн: {patterns[0].get('id')}")
            print(f"   Триггеры: {patterns[0].get('triggers', [])[:2]}")
    except Exception as e:
        print(f"❌ Ошибка чтения: {e}")
else:
    print("❌ Файл не найден")
print("\n3. Простой поиск 'привет':")
if os.path.exists(patterns_file):
    with open(patterns_file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    patterns = data.get("patterns", [])
    found = False
    
    for pattern in patterns:
        for trigger in pattern.get("triggers", []):
            if "привет" in trigger.lower():
                print(f"✅ Найден триггер: {trigger}")
                print(f"   ID паттерна: {pattern.get('id')}")
                found = True
                break
        if found:
            break
    
    if not found:
        print("❌ Триггер 'привет' не найден")
