# test_encoding.py
print("Проверка кодировки...")

# Тест русских символов
test_words = ["создать", "привет", "посчитать"]
for word in test_words:
    print(f"Слово '{word}':")
    print(f"  Длина: {len(word)}")
    print(f"  Байты: {word.encode('utf-8')}")
    print(f"  isalpha: {word.isalpha()}")

# Проверка файла
import os
if os.path.exists("core/embeddings_manager.py"):
    with open("core/embeddings_manager.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "создать" in content:
            print("✅ Русские слова в файле корректны")
        else:
            print("❌ Русских слов не найдено")