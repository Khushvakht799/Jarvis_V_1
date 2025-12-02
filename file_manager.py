import json
import pickle
import numpy as np
from pathlib import Path
import config

def ensure_data_files():
    config.DATA_DIR.mkdir(exist_ok=True)
    config.EMBEDDINGS_DIR.mkdir(exist_ok=True)
    
    if not config.PATTERNS_FILE.exists():
        with open(config.PATTERNS_FILE, 'w', encoding='utf-8') as f:
            initial_patterns = {
                \"patterns\": [
                    {
                        \"id\": \"hello_world\",
                        \"triggers\": [\"привет\", \"hello\", \"старт\"],
                        \"template\": \"result = 'Привет! Я Jarvis с embedding-овым словарем.'\",
                        \"variables\": {},
                        \"category\": \"system\"
                    },
                    {
                        \"id\": \"create_list\",
                        \"triggers\": [\"создай список из чисел\", \"create list of numbers\"],
                        \"template\": \"result = list(range({n}))\",
                        \"variables\": {\"n\": {\"type\": \"int\", \"default\": 5}},
                        \"category\": \"data_structures\"
                    }
                ],
                \"statistics\": {\"total_uses\": 0, \"last_updated\": \"\"}
            }
            json.dump(initial_patterns, f, ensure_ascii=False, indent=2)
        print(\"✅ Создан файл patterns.json\")
    
    if not config.ERROR_DB_FILE.exists():
        with open(config.ERROR_DB_FILE, 'w', encoding='utf-8') as f:
            initial_errors = {
                \"errors\": [
                    {
                        \"error_type\": \"NameError\",
                        \"pattern\": \"name .* is not defined\",
                        \"solutions\": [\"Переменная не определена\", \"Проверьте правильность написания\"],
                        \"prevention\": \"Инициализируйте переменные\"
                    }
                ]
            }
            json.dump(initial_errors, f, ensure_ascii=False, indent=2)
        print(\"✅ Создан файл error_db.json\")
    
    if not config.CONTEXT_FILE.exists():
        with open(config.CONTEXT_FILE, 'w', encoding='utf-8') as f:
            json.dump({\"variables\": {}, \"history\": []}, f, ensure_ascii=False, indent=2)
    
    print(\"✅ Все файлы данных готовы\")