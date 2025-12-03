import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("Диагностика...")

# Проверка файлов
files = [
    "config.py",
    "core/__init__.py", 
    "core/interpreter.py",
    "core/executor.py",
    "core/embeddings_manager.py",
    "core/error_handler.py",
    "utils/__init__.py",
    "utils/file_manager.py"
]

for f in files:
    full_path = os.path.join(os.path.dirname(__file__), f)
    if os.path.exists(full_path):
        print(f"✅ {f}")
        # Пробуем прочитать первые 3 строки
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()[:3]
                print(f"   Содержит: {''.join(lines).strip()[:50]}...")
        except:
            print(f"   (бинарный или ошибка чтения)")
    else:
        print(f"❌ {f}")

print("\nПопытка импорта...")
try:
    from core.interpreter import EmbeddingInterpreter
    print("✅ interpreter - OK")
except ImportError as e:
    print(f"❌ interpreter: {e}")

try:
    from core.executor import CodeExecutor
    print("✅ executor - OK")
except ImportError as e:
    print(f"❌ executor: {e}")

try:
    from utils.file_manager import ensure_data_files
    print("✅ file_manager - OK")
except ImportError as e:
    print(f"❌ file_manager: {e}")
