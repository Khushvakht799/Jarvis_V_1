#!/usr/bin/env python3
"""
Jarvis - AI Interface
"""


import sys
import os
import traceback  # ← ДОБАВЬТЕ ЭТО

# Добавляем текущую папку в путь
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)

print("🤖 Запуск Jarvis...")

# Проверяем наличие файлов
print("🔍 Проверка файлов...")
required = [
    ("config.py", os.path.join(current_dir, "config.py")),
    ("core/interpreter.py", os.path.join(current_dir, "core", "interpreter.py")),
    ("core/executor.py", os.path.join(current_dir, "core", "executor.py")),
    ("utils/file_manager.py", os.path.join(current_dir, "utils", "file_manager.py"))
]

for name, path in required:
    if os.path.exists(path):
        print(f"✅ {name}")
    else:
        print(f"❌ {name} - отсутствует")

# Пытаемся импортировать модули
try:
    from core.interpreter import EmbeddingInterpreter
    from core.executor import CodeExecutor
    from utils.file_manager import ensure_data_files
    import config
    
    print("✅ Модули загружены")
    
    # РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ
    ensure_data_files()
    interpreter = EmbeddingInterpreter()
    executor = CodeExecutor(safe_mode=True)
    
    print(f"вњ… РЎР»РѕРІР°СЂСЊ: {interpreter.get_vocab_size()} РіР»Р°РіРѕР»РѕРІ")
    
    # РРЅС‚РµСЂР°РєС‚РёРІРЅС‹Р№ СЂРµР¶РёРј
    while True:
        cmd = input("\nJarvis> ").strip()
        if cmd.lower() == 'exit':
            break
        
        result = interpreter.interpret(cmd)
        if result:
            template, vars, score = result
            print(f"вњ… ({score:.1%}): {template}")
            
            # РџРѕРґСЃС‚Р°РІР»СЏРµРј РїРµСЂРµРјРµРЅРЅС‹Рµ
            code = template
            for k, v in vars.items():
                code = code.replace(f"{{{k}}}", str(v))
            
            # Р’С‹РїРѕР»РЅСЏРµРј
            success, output, res = executor.execute(code)
            if success:
                print(f"Р РµР·СѓР»СЊС‚Р°С‚: {res}")
            else:
                print(f"РћС€РёР±РєР°: {output}")
        else:
            print("вќЊ РќРµ СЂР°СЃРїРѕР·РЅР°РЅРѕ")
            
except ImportError as e:
    print(f"вќЊ РћС€РёР±РєР° РёРјРїРѕСЂС‚Р°: {e}")
    print("РЎРѕР·РґР°Р№С‚Рµ РЅРµРґРѕСЃС‚Р°СЋС‰РёРµ РјРѕРґСѓР»Рё")
