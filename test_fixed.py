import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("🧪 Тест исправленных эмбеддингов")

try:
    from core.embeddings_manager_fixed import VerbEmbeddings
    
    class Config:
        BASE_DIR = os.path.dirname(__file__)
        DATA_DIR = os.path.join(BASE_DIR, "data")
        EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")
    
    config = Config()
    
    print("1. Создаем эмбеддинги...")
    embeddings = VerbEmbeddings(config.EMBEDDINGS_DIR)
    
    print(f"\n2. Размер словаря: {embeddings.get_vocab_size()}")
    print(f"   Глаголы: {list(embeddings.vocab.keys())}")
    
    print("\n3. Тестируем поиск похожих:")
    
    test_words = ["создать", "create", "привет", "hello", "создай"]
    
    for word in test_words:
        similar = embeddings.find_similar(word, top_k=3)
        print(f"   '{word}': {similar}")
    
    print("\n4. Проверяем нормализацию:")
    import numpy as np
    
    norms = np.linalg.norm(embeddings.embeddings, axis=1)
    print(f"   Нормы векторов: min={norms.min():.3f}, max={norms.max():.3f}")
    
    print("\n✅ Тест завершен успешно!")
    
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
