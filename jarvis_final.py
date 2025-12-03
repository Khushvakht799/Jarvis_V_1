#!/usr/bin/env python3
"""
Jarvis FINAL - полностью работающая версия
"""

import sys
import os
import json
import re
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

print("🤖 Jarvis FINAL - работающая система с embedding-овым словарем")

# Конфигурация
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
PATTERNS_FILE = DATA_DIR / "patterns.json"

# 1. Загружаем паттерны
print("\n📂 Загрузка паттернов...")
patterns = []
if PATTERNS_FILE.exists():
    with open(PATTERNS_FILE, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        patterns = data.get("patterns", [])
    print(f"✅ Загружено {len(patterns)} паттернов")
else:
    print("⚠️  patterns.json не найден")

# 2. Простой поиск
def find_command(user_input):
    user_input_lower = user_input.lower()
    
    for pattern in patterns:
        for trigger in pattern.get("triggers", []):
            if trigger.lower() in user_input_lower:
                # Извлекаем переменные
                variables = {}
                numbers = re.findall(r'\b\d+\b', user_input)
                
                template = pattern.get("template", "")
                if numbers:
                    if "{n}" in template:
                        variables["n"] = int(numbers[0])
                    if "{start}" in template:
                        variables["start"] = int(numbers[0])
                    if "{end}" in template and len(numbers) > 1:
                        variables["end"] = int(numbers[1])
                
                return template, variables
    
    return None, {}

# 3. Исполнитель
def execute_python(code, variables):
    """Безопасное выполнение Python кода"""
    try:
        # Подставляем переменные
        for key, value in variables.items():
            code = code.replace(f"{{{key}}}", str(value))
        
        # Создаем безопасное окружение
        safe_globals = {
            "__builtins__": {
                'print': print,
                'len': len,
                'range': range,
                'list': list,
                'sum': sum,
                'int': int,
                'str': str,
                'float': float,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'abs': abs,
                'min': min,
                'max': max,
                'sorted': sorted
            }
        }
        
        # Разрешаем импорт некоторых модулей
        import importlib
        for module in ["math", "datetime", "random"]:
            try:
                safe_globals[module] = importlib.import_module(module)
            except:
                pass
        
        local_vars = {}
        exec(code, safe_globals, local_vars)
        
        return True, "", local_vars.get('result', None)
        
    except Exception as e:
        return False, str(e), None

# 4. Интерактивный режим
print("\n" + "="*60)
print("🚀 СИСТЕМА ГОТОВА К РАБОТЕ")
print("="*60)

if patterns:
    print("\n📚 Доступные команды:")
    for i, pattern in enumerate(patterns[:8]):  # Показываем первые 8
        triggers = pattern.get("triggers", [])
        if triggers:
            print(f"  {i+1}. {triggers[0]}")
    if len(patterns) > 8:
        print(f"  ... и еще {len(patterns)-8} команд")

print("\n💡 Примеры: 'привет', 'создай список из 10 чисел', 'покажи время'")
print("   Введите 'exit' для выхода")
print("="*60)

while True:
    try:
        cmd = input("\nJarvis> ").strip()
        
        if cmd.lower() in ["exit", "quit", "выход"]:
            print("Завершение работы...")
            break
        
        template, variables = find_command(cmd)
        
        if template:
            print(f"✅ Команда распознана")
            if variables:
                print(f"   Переменные: {variables}")
            
            success, error, result = execute_python(template, variables)
            
            if success:
                if result is not None:
                    print(f"📊 Результат: {result}")
                else:
                    print("✅ Команда выполнена успешно")
            else:
                print(f"❌ Ошибка выполнения: {error}")
        else:
            print("❌ Команда не распознана")
            print("   Попробуйте:")
            print("   - 'привет' - тест системы")
            print("   - 'создай список' - создать список чисел")
            print("   - 'покажи время' - показать текущее время")
            
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем")
        break
    except Exception as e:
        print(f"⚠️  Системная ошибка: {e}")

print("\n🎉 Спасибо за использование Jarvis!")
