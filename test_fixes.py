#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("🧪 ТЕСТ ИСПРАВЛЕНИЙ")

# Тест 1: Executor с переменными
print("\n1. Тест executor с переменными:")
from core.executor import CodeExecutor

executor = CodeExecutor()

# Тест подстановки переменных
test_code = "result = list(range({n}))"
success, output, result = executor.execute(test_code, {"n": 5})

if success and result == [0, 1, 2, 3, 4]:
    print("✅ Подстановка {n} → 5 работает")
else:
    print(f"❌ Ошибка: {output}")

# Тест с datetime
time_code = "import datetime; result = datetime.datetime.now().strftime('%H:%M')"
success, output, result = executor.execute(time_code, {})

if success and ":" in str(result):
    print("✅ Импорт datetime работает")
else:
    print(f"❌ Ошибка datetime: {output}")

# Тест 2: Interpreter с переменными
print("\n2. Тест interpreter с переменными:")
from core.interpreter import EmbeddingInterpreter
import config

interpreter = EmbeddingInterpreter()

test_cases = [
    ("создай список из 8 чисел", {"n": 8}),
    ("посчитай сумму 1 2 3", {"numbers": "1, 2, 3"}),
    ("переверни строку 'тест'", {"text": "тест"})
]

for i, (cmd, expected) in enumerate(test_cases, 1):
    result = interpreter.interpret(cmd)
    if result:
        template, vars, score = result
        if vars == expected:
            print(f"✅ Тест {i}: '{cmd}' → переменные: {vars}")
        else:
            print(f"❌ Тест {i}: ожидалось {expected}, получили {vars}")
    else:
        print(f"❌ Тест {i}: команда не найдена")

print("\n🎉 ТЕСТ ЗАВЕРШЕН")
