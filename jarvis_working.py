#!/usr/bin/env python3
"""
Jarvis - работающая версия
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("🤖 Jarvis - работающая версия")

try:
    from core.interpreter_fixed import EmbeddingInterpreter
    from core.executor import CodeExecutor
    
    print("✅ Модули загружены")
    
    interpreter = EmbeddingInterpreter()
    executor = CodeExecutor(safe_mode=True)
    
    print(f"📚 Словарь: {interpreter.get_vocab_size()} глаголов")
    print(f"📝 Паттернов: {len(interpreter.patterns)}")
    
    print("\n" + "="*50)
    print("🚀 Готов к работе!")
    print("Команды: привет, создай список, покажи время, exit")
    print("="*50)
    
    while True:
        cmd = input("\nJarvis> ").strip()
        if cmd.lower() == "exit":
            print("Завершение...")
            break
        
        result = interpreter.interpret(cmd)
        
        if result:
            template, variables, score = result
            print(f"✅ Найдено ({score:.0%})")
            print(f"Шаблон: {template}")
            
            # Подставляем переменные
            code = template
            for key, value in variables.items():
                code = code.replace(f"{{{key}}}", str(value))
            
            # Выполняем
            success, output, res = executor.execute(code)
            if success:
                if res is not None:
                    print(f"Результат: {res}")
                else:
                    print("✅ Выполнено")
            else:
                print(f"❌ Ошибка: {output}")
        else:
            print("❌ Команда не распознана")
            print("   Доступные команды:")
            for pattern in interpreter.patterns[:3]:  # Показываем первые 3
                triggers = pattern.get("triggers", [])
                if triggers:
                    print(f"   • {triggers[0]}")
            
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Создайте файлы:")
    print("  core/interpreter_fixed.py")
    print("  core/embeddings_manager_fixed.py")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
