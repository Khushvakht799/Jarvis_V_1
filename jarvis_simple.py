# jarvis_simple.py - минимальная работающая версия
import json
import os
import numpy as np

# 1. Создаем embedding-овый словарь
print("🔄 Создание embedding-ового словаря...")

verbs = ['создать', 'выполнить', 'посчитать', 'привет', 'hello']
embeddings = {}

for verb in verbs:
    # Простой эмбеддинг на основе хеша
    import hashlib
    h = hashlib.md5(verb.encode()).digest()
    emb = np.frombuffer(h[:16], dtype=np.float32)
    emb = np.pad(emb, (0, 384 - len(emb)), 'constant')
    emb = emb / (np.linalg.norm(emb) + 1e-10)
    embeddings[verb] = emb

print(f"✅ Создано {len(verbs)} эмбеддингов")

# 2. Паттерны
patterns = [
    {
        "triggers": ["привет", "hello"],
        "template": "result = 'Привет от Jarvis!'"
    },
    {
        "triggers": ["создай список"],
        "template": "result = list(range(5))"
    }
]

# 3. Поиск
def find_command(user_input):
    user_input = user_input.lower()
    
    # Простой поиск по ключевым словам
    for pattern in patterns:
        for trigger in pattern["triggers"]:
            if trigger in user_input:
                return pattern["template"], {}
    
    return None, {}

# 4. Запуск
print("\n🤖 Jarvis готов! Введите команду...")

while True:
    cmd = input("\nJarvis> ").strip()
    if cmd.lower() == 'exit':
        break
    
    template, vars = find_command(cmd)
    if template:
        print(f"✅ Найдено: {template}")
        
        # Выполняем
        try:
            exec(template, {'__builtins__': {}}, {})
            print(f"Результат: {locals().get('result', 'выполнено')}")
        except Exception as e:
            print(f"Ошибка: {e}")
    else:
        print("❌ Не распознано")