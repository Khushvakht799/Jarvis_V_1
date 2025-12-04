### Сценарий для расширения словаря глаголов из action_add.txt

import json
import os
import sys
from typing import Dict, List, Any

# Пути к файлам
DICT_FILE = "action_dictionary.json"  # основной словарь
ADD_FILE = "action_add.txt"           # файл с новыми глаголами
BACKUP_FILE = "action_dictionary_backup.json"

class ActionDictionaryExpander:
    def __init__(self, dict_file: str, add_file: str):
        self.dict_file = dict_file
        self.add_file = add_file
        self.dictionary = self.load_dictionary()
        
    def load_dictionary(self) -> Dict:
        """Загружает существующий словарь или создаёт базовый"""
        if os.path.exists(self.dict_file):
            try:
                with open(self.dict_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Ошибка загрузки словаря: {e}")
                return self.create_base_dictionary()
        else:
            print(f"📝 Файл {self.dict_file} не найден, создаю базовый словарь")
            return self.create_base_dictionary()
    
    def create_base_dictionary(self) -> Dict:
        """Создаёт базовую структуру словаря"""
        return {
            "version": "1.0",
            "last_updated": "",
            "actions": [
                {
                    "verb": "напиши",
                    "intent": "write",
                    "parameters": ["text"],
                    "action_type": "text_output",
                    "machine_code": "ACTION.WRITE(text)",
                    "examples": ["напиши Hello", "напиши привет мир"]
                },
                {
                    "verb": "прочитай",
                    "intent": "read",
                    "parameters": ["file"],
                    "action_type": "text_input",
                    "machine_code": "ACTION.READ(file)",
                    "examples": ["прочитай файл.txt", "прочитай документ"]
                },
                {
                    "verb": "удали",
                    "intent": "delete",
                    "parameters": ["file"],
                    "action_type": "file_op",
                    "machine_code": "ACTION.DELETE(file)",
                    "examples": ["удали test.txt", "удали старый файл"]
                },
                {
                    "verb": "создай",
                    "intent": "create",
                    "parameters": ["file"],
                    "action_type": "file_op",
                    "machine_code": "ACTION.CREATE(file)",
                    "examples": ["создай report.txt", "создай новый файл"]
                }
            ]
        }
    
    def parse_addition_file(self) -> List[Dict]:
        """Парсит файл action_add.txt с новыми глаголами"""
        if not os.path.exists(self.add_file):
            print(f"⚠️ Файл {self.add_file} не найден")
            return []
        
        new_actions = []
        with open(self.add_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        for line in lines:
            if line.startswith('#') or not line:
                continue  # пропускаем комментарии и пустые строки
            
            try:
                # Формат: глагол|интент|параметры|тип|машинный код|пример1,пример2
                parts = line.split('|')
                if len(parts) >= 5:
                    action = {
                        "verb": parts[0].strip(),
                        "intent": parts[1].strip(),
                        "parameters": [p.strip() for p in parts[2].split(',')],
                        "action_type": parts[3].strip(),
                        "machine_code": parts[4].strip(),
                        "examples": [e.strip() for e in parts[5].split(',')] if len(parts) > 5 else []
                    }
                    new_actions.append(action)
            except Exception as e:
                print(f"⚠️ Ошибка парсинга строки '{line}': {e}")
        
        return new_actions
    
    def merge_actions(self, new_actions: List[Dict]) -> int:
        """Добавляет новые действия в словарь, избегая дубликатов"""
        existing_verbs = {action["verb"] for action in self.dictionary.get("actions", [])}
        added_count = 0
        
        for new_action in new_actions:
            if new_action["verb"] in existing_verbs:
                print(f"⚠️ Глагол '{new_action['verb']}' уже существует, пропускаю")
                continue
            
            self.dictionary["actions"].append(new_action)
            existing_verbs.add(new_action["verb"])
            added_count += 1
            print(f"✅ Добавлен: {new_action['verb']} -> {new_action['intent']}")
        
        return added_count
    
    def save_backup(self):
        """Сохраняет резервную копию словаря"""
        if os.path.exists(self.dict_file):
            import shutil
            shutil.copy2(self.dict_file, BACKUP_FILE)
            print(f"📦 Создана резервная копия: {BACKUP_FILE}")
    
    def save_dictionary(self):
        """Сохраняет обновлённый словарь"""
        import datetime
        self.dictionary["last_updated"] = datetime.datetime.now().isoformat()
        
        with open(self.dict_file, 'w', encoding='utf-8') as f:
            json.dump(self.dictionary, f, ensure_ascii=False, indent=2, sort_keys=True)
        
        print(f"💾 Словарь сохранён в {self.dict_file}")
        print(f"📊 Всего действий: {len(self.dictionary['actions'])}")
    
    def print_summary(self):
        """Выводит статистику словаря"""
        print("\n" + "="*50)
        print("📋 СТАТИСТИКА СЛОВАРЯ:")
        print(f"📁 Файл словаря: {self.dict_file}")
        print(f"📁 Файл дополнений: {self.add_file}")
        print(f"🔢 Всего глаголов: {len(self.dictionary['actions'])}")
        print("\n📝 Последние 5 глаголов:")
        for action in self.dictionary['actions'][-5:]:
            print(f"  • {action['verb']} → {action['intent']} ({action['action_type']})")
        print("="*50)
    
    def run(self):
        """Основной метод расширения словаря"""
        print("🚀 Расширение словаря глаголов Jarvis")
        
        # Загружаем новые действия
        new_actions = self.parse_addition_file()
        if not new_actions:
            print(f"📭 В файле {self.add_file} нет новых действий для добавления")
            print("📝 Формат строки: глагол|интент|параметры|тип|машинный код|примеры")
            print("📝 Пример: посчитай|calculate|expression|math|ACTION.CALCULATE(expression)|посчитай 2+2")
            return
        
        print(f"📖 Найдено новых действий: {len(new_actions)}")
        
        # Создаём резервную копию
        self.save_backup()
        
        # Добавляем новые действия
        added = self.merge_actions(new_actions)
        
        if added > 0:
            # Сохраняем обновлённый словарь
            self.save_dictionary()
            
            # Выводим статистику
            self.print_summary()
            
            # Создаём файл с примерами использования
            self.create_examples_file(new_actions)
        else:
            print("📭 Нет новых действий для добавления")
    
    def create_examples_file(self, new_actions: List[Dict]):
        """Создаёт файл с примерами использования новых глаголов"""
        examples_file = "new_actions_examples.txt"
        with open(examples_file, 'w', encoding='utf-8') as f:
            f.write("# Примеры использования новых глаголов\n\n")
            for action in new_actions:
                f.write(f"## {action['verb']} ({action['intent']})\n")
                f.write(f"- Тип: {action['action_type']}\n")
                f.write(f"- Машинный код: {action['machine_code']}\n")
                f.write(f"- Параметры: {', '.join(action['parameters'])}\n")
                if action['examples']:
                    f.write(f"- Примеры:\n")
                    for example in action['examples']:
                        f.write(f"  • {example}\n")
                else:
                    f.write(f"- Пример: {action['verb']} [параметр]\n")
                f.write("\n")
        
        print(f"📝 Создан файл с примерами: {examples_file}")

def main():
    """Точка входа в программу"""
    expander = ActionDictionaryExpander(DICT_FILE, ADD_FILE)
    expander.run()

if __name__ == "__main__":
    main()
EOF