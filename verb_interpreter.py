# verb_interpreter.py (обновлённая версия)
import json
import os
import re
from datetime import datetime
from typing import Dict, Any, List
from python_knowledge_base import PYTHON_KNOWLEDGE  # <-- ИМПОРТ ЗНАНИЙ

class VerbInterpreter:
    def __init__(self, dict_path="data/action_dictionary.json"):
        self.dict_path = dict_path
        self.actions = {}
        self.knowledge = PYTHON_KNOWLEDGE  # <-- ЗАГРУЖАЕМ ЗНАНИЯ
        
        # Загружаем пользовательские команды
        self.load_dictionary()
        
        print(f"🤖 Jarvis инициализирован")
        print(f"📚 Знаний: {len(self.knowledge['builtins'])} builtins, "
              f"{len(self.knowledge['modules'])} модулей")
    
    def load_dictionary(self):
        """Загружает пользовательские команды"""
        if not os.path.exists(self.dict_path):
            print("📝 Создаю базовый словарь...")
            self.create_default_dictionary()
            return
        
        try:
            with open(self.dict_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.actions = {a["verb"]: a for a in data.get("actions", [])}
            print(f"✅ Загружено {len(self.actions)} пользовательских команд")
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            self.create_default_dictionary()
    
    def search_knowledge(self, query: str) -> List[Dict]:
        """Ищет в базе знаний Python по запросу"""
        results = []
        query_lower = query.lower()
        
        # Ищем в builtins
        for func_name, info in self.knowledge["builtins"].items():
            if (query_lower in func_name.lower() or 
                query_lower in info["description"].lower()):
                results.append({
                    "type": "builtin",
                    "name": func_name,
                    "description": info["description"],
                    "usage": info["usage"],
                    "examples": info["examples"]
                })
        
        # Ищем в модулях
        for module_name, info in self.knowledge["modules"].items():
            if query_lower in module_name.lower() or query_lower in info["description"].lower():
                results.append({
                    "type": "module",
                    "name": module_name,
                    "description": info["description"],
                    "import": info["import"],
                    "functions": info["functions"]
                })
        
        # Ищем в шаблонах
        for pattern_name, code in self.knowledge["common_patterns"].items():
            if query_lower in pattern_name.lower():
                results.append({
                    "type": "pattern",
                    "name": pattern_name,
                    "code": code
                })
        
        return results
    
    def suggest_python_code(self, user_request: str) -> str:
        """Предлагает код Python на основе запроса пользователя"""
        # Анализируем запрос
        if any(word in user_request.lower() for word in ["выведи", "напечатай", "покажи"]):
            return "print('ваш_текст')"
        
        elif any(word in user_request.lower() for word in ["посчитай", "вычисли", "реши"]):
            return "result = eval('2+2')  # Замените выражение"
        
        elif any(word in user_request.lower() for word in ["прочитай", "открой файл"]):
            return "with open('файл.txt', 'r', encoding='utf-8') as f:\n    content = f.read()"
        
        elif any(word in user_request.lower() for word in ["создай", "сделай", "напиши файл"]):
            return "with open('новый_файл.txt', 'w', encoding='utf-8') as f:\n    f.write('текст')"
        
        elif any(word in user_request.lower() for word in ["список", "массив"]):
            return "my_list = [1, 2, 3, 4, 5]"
        
        elif any(word in user_request.lower() for word in ["словарь", "ключ-значение"]):
            return "my_dict = {'ключ1': 'значение1', 'ключ2': 'значение2'}"
        
        # Если не нашли паттерн - ищем в базе знаний
        search_results = self.search_knowledge(user_request)
        if search_results:
            result = search_results[0]
            if result["type"] == "builtin":
                return f"# {result['description']}\n{result['usage']}\n# Пример: {result['examples'][0]}"
            elif result["type"] == "module":
                return f"# {result['description']}\n{result['import']}\n# Функции: {', '.join(result['functions'][:3])}"
        
        return "# Не могу предложить код. Попробуйте точнее описать задачу."
    
    def process(self, user_input: str) -> Dict[str, Any]:
        """Обрабатывает ввод пользователя"""
        text = user_input.strip()
        
        if not text:
            return {"success": False, "message": "Введите команду"}
        
        # Специальные команды
        if text.lower() in ["что ты умеешь", "возможности", "help python"]:
            return self.show_capabilities()
        
        elif text.lower().startswith("найди в python"):
            query = text[14:].strip()
            return self.search_in_python(query)
        
        elif text.lower().startswith("как сделать"):
            task = text[11:].strip()
            return self.how_to_do(task)
        
        # Проверяем пользовательские команды
        text_lower = text.lower()
        for verb, action in self.actions.items():
            if text_lower.startswith(verb):
                param = text[len(verb):].strip()
                return self.execute_user_command(verb, param)
        
        # Если команда не найдена - предлагаем Python код
        suggestion = self.suggest_python_code(text)
        return {
            "success": False,
            "message": f"❓ Команда не найдена\n💡 Попробуйте в Python:\n```python\n{suggestion}\n```",
            "suggestion": suggestion,
            "type": "python_suggestion"
        }
    
    def show_capabilities(self) -> Dict[str, Any]:
        """Показывает возможности Python"""
        builtins_count = len(self.knowledge["builtins"])
        modules_count = len(self.knowledge["modules"])
        
        message = f"""🤖 **Jarvis знает о Python:**
        
📊 **Built-in функции:** {builtins_count} 
  • print() - вывод текста
  • len() - длина объекта
  • input() - ввод пользователя
  • str(), int(), float() - преобразования
  • list(), dict(), range() - структуры данных

📦 **Модули:** {modules_count}
  • os - работа с файловой системой
  • math - математические функции
  • datetime - дата и время
  • json - работа с JSON
  • re - регулярные выражения

💡 **Используйте:**
  • 'найди в python [запрос]' - поиск функций
  • 'как сделать [задача]' - получить пример кода
  • Или просто введите команду"""
        
        return {
            "success": True,
            "message": message,
            "type": "capabilities"
        }
    
    def search_in_python(self, query: str) -> Dict[str, Any]:
        """Ищет в базе знаний Python"""
        results = self.search_knowledge(query)
        
        if not results:
            return {
                "success": False,
                "message": f"🔍 По запросу '{query}' ничего не найдено"
            }
        
        message = f"🔍 **Найдено в Python по запросу '{query}':**\n\n"
        
        for i, result in enumerate(results[:5], 1):  # Показываем первые 5
            if result["type"] == "builtin":
                message += f"{i}. **{result['name']}()** - {result['description']}\n"
                message += f"   Использование: `{result['usage']}`\n"
            elif result["type"] == "module":
                message += f"{i}. **Модуль {result['name']}** - {result['description']}\n"
                message += f"   Импорт: `{result['import']}`\n"
        
        if len(results) > 5:
            message += f"\n📄 ... и ещё {len(results) - 5} результатов"
        
        return {
            "success": True,
            "message": message,
            "results": results[:5],
            "type": "search_results"
        }
    
    def how_to_do(self, task: str) -> Dict[str, Any]:
        """Показывает как сделать что-то в Python"""
        suggestion = self.suggest_python_code(task)
        
        return {
            "success": True,
            "message": f"💡 **Как сделать '{task}' в Python:**\n```python\n{suggestion}\n```",
            "code": suggestion,
            "type": "how_to"
        }
    
    def execute_user_command(self, verb: str, param: str) -> Dict[str, Any]:
        """Выполняет пользовательскую команду"""
        # Базовая реализация
        if verb == "напиши":
            try:
                with open("output.txt", "a", encoding="utf-8") as f:
                    f.write(f"{param}\n")
                return {
                    "success": True,
                    "message": f"✅ Записал: '{param}' в output.txt",
                    "type": "write"
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"❌ Ошибка записи: {e}"
                }
        
        elif verb == "посчитай":
            try:
                result = eval(param)
                return {
                    "success": True,
                    "message": f"🧮 {param} = {result}",
                    "result": result,
                    "type": "calculate"
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"❌ Ошибка вычисления: {e}"
                }
        
        return {
            "success": False,
            "message": f"⚠️ Команда '{verb}' не реализована"
        }

# Тестирование
if __name__ == "__main__":
    vi = VerbInterpreter()
    
    test_queries = [
        "что ты умеешь",
        "найди в python вывод текста",
        "как сделать список",
        "напиши привет мир",
        "посчитай 10+5*2",
        "неизвестная команда"
    ]
    
    print("🧪 Тестирование Jarvis с базой знаний Python")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n▶ Ввод: {query}")
        result = vi.process(query)
        
        if result["success"]:
            print(f"✅ {result['message'][:100]}...")
        else:
            print(f"❓ {result['message'][:100]}...")