#!/usr/bin/env python3
# run.py - Исправленный запуск Jarvis

import sys
import os
from pathlib import Path

# Добавляем текущую папку в путь Python
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Создаем минимальный config если нет
if not (current_dir / "config.py").exists():
    config_content = '''
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
PATTERNS_FILE = DATA_DIR / "patterns.json"
ERROR_DB_FILE = DATA_DIR / "error_db.json"
SIMILARITY_THRESHOLD = 0.7
'''
    with open(current_dir / "config.py", 'w') as f:
        f.write(config_content)

# Теперь импортируем
from jarvis.core.interpreter import EmbeddingInterpreter
from jarvis.core.executor import CodeExecutor
from jarvis.core.error_handler import ErrorHandler
from jarvis.utils.file_manager import ensure_data_files

import config

# Запускаем основную функцию из jarvis.py
# Копируем основной код из jarvis.py или импортируем класс

class SimpleJarvis:
    def __init__(self):
        print("🤖 Инициализация Jarvis...")
        ensure_data_files()
        self.interpreter = EmbeddingInterpreter()
        self.executor = CodeExecutor(safe_mode=True)
        self.error_handler = ErrorHandler(config.ERROR_DB_FILE)
        print("✅ Jarvis готов!")
    
    def run(self):
        print("\n" + "="*50)
        print("       JARVIS с Embedding-овым словарем")
        print("="*50)
        print("Команды: 'exit' - выход, 'stats' - статистика")
        print("="*50)
        
        while True:
            try:
                cmd = input("\nJarvis> ").strip()
                if cmd.lower() == 'exit':
                    break
                elif cmd.lower() == 'stats':
                    print(f"Глаголов в словаре: {self.interpreter.get_vocab_size()}")
                else:
                    # Обработка команды
                    result = self.interpreter.interpret(cmd)
                    if result:
                        template, vars, score = result
                        print(f"✅ Распознано ({score:.1%}): {template}")
                    else:
                        print("❌ Команда не распознана")
            except KeyboardInterrupt:
                print("\nЗавершение...")
                break

if __name__ == "__main__":
    jarvis = SimpleJarvis()
    jarvis.run()