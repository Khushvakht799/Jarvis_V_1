import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("🧪 Тест улучшенных эмбеддингов")

from core.embeddings_manager import VerbEmbeddings

class Config:
    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(BASE_DIR, "data")
    EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")

config = Config()

print("1. Пересоздаем эмбеддинги с расширенным словарем...")
embeddings = VerbEmbeddings(config.EMBEDDINGS_DIR)

print(f"\n2. Размер словаря: {embeddings.get_vocab_size()}")

print("\n3. Тестируем поиск похожих:")
test_cases = [
    ("создать", "русский глагол"),
    ("create", "английский синоним"),
    ("создай", "частичное совпадение"),
    ("привет", "приветствие"),
    ("hello", "английское приветствие"),
    ("make", "другой синоним"),
    ("найти", "поиск"),
    ("find", "английский поиск")
]

for word, description in test_cases:
    similar = embeddings.find_similar(word, top_k=3)
    print(f"   '{word}' ({description}): {similar}")

print("\n4. Проверяем интерпретатор:")
from core.interpreter_fixed import EmbeddingInterpreter

interpreter = EmbeddingInterpreter()

test_commands = [
    "привет",
    "hello",
    "создай список",
    "create list",
    "создай список из 8 чисел",
    "покажи время"
]

print("\n5. Поиск команд:")
for cmd in test_commands:
    result = interpreter.interpret(cmd)
    if result:
        template, vars, score = result
        print(f"   ✅ '{cmd}' -> найдено")
        if vars:
            print(f"      Переменные: {vars}")
    else:
        print(f"   ❌ '{cmd}' -> не найдено")

print("\n✅ Тест завершен")
