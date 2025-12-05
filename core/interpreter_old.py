# verb_interpreter.py - Windows compatible
# -*- coding: utf-8 -*-
import json
import os
import sys

class VerbInterpreter:
    def __init__(self, dict_path="data/action_dictionary.json"):
        self.dict_path = dict_path
        self.actions = {}
        self.load_dictionary()
    
    def load_dictionary(self):
        if not os.path.exists(self.dict_path):
            print(f"[WARN] Dictionary not found: {self.dict_path}")
            self.create_default_dict()
            return
        
        try:
            with open(self.dict_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for action in data.get("actions", []):
                self.actions[action["verb"]] = action
            
            print(f"[OK] Loaded {len(self.actions)} actions")
            
        except Exception as e:
            print(f"[ERROR] Loading dictionary: {e}")
            self.create_default_dict()
    
    def create_default_dict(self):
        self.actions = {
            "напиши": {
                "verb": "напиши",
                "intent": "write",
                "params": ["текст"],
                "type": "text_output",
                "code": "print('Написано: {текст}')",
                "examples": ["напиши привет", "напиши текст"]
            },
            "прочитай": {
                "verb": "прочитай",
                "intent": "read",
                "params": ["файл"],
                "type": "text_input",
                "code": "self.read_file('{файл}')",
                "examples": ["прочитай файл.txt"]
            },
            "создай": {
                "verb": "создай",
                "intent": "create",
                "params": ["файл"],
                "type": "file_op",
                "code": "self.create_file('{файл}')",
                "examples": ["создай новый.txt"]
            },
            "удали": {
                "verb": "удали",
                "intent": "delete",
                "params": ["файл"],
                "type": "file_op",
                "code": "self.delete_file('{файл}')",
                "examples": ["удали старый.txt"]
            },
            "посчитай": {
                "verb": "посчитай",
                "intent": "calculate",
                "params": ["выражение"],
                "type": "math",
                "code": "self.calculate('{выражение}')",
                "examples": ["посчитай 2+2"]
            }
        }
        self.save_dictionary()
    
    def save_dictionary(self):
        data = {"version": "1.0", "actions": list(self.actions.values())}
        os.makedirs(os.path.dirname(self.dict_path), exist_ok=True)
        with open(self.dict_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[OK] Dictionary saved: {self.dict_path}")
    
    def find_action(self, text):
        text = text.strip().lower()
        words = text.split()
        
        if not words:
            return None, 0.0
        
        first_word = words[0]
        
        # Direct match
        if first_word in self.actions:
            return self.actions[first_word], 0.95
        
        # Search in verbs
        for verb, action in self.actions.items():
            if verb in text:
                return action, 0.8
        
        return None, 0.0
    
    def execute(self, action, params):
        verb = action["verb"]
        
        if verb == "напиши":
            text = params.get("текст", "")
            return f"Написано: {text}"
        
        elif verb == "прочитай":
            filename = params.get("файл", "")
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read(200)
                    return f"Файл {filename}:\n{content}"
                except:
                    return f"Ошибка чтения: {filename}"
            else:
                return f"Файл не найден: {filename}"
        
        elif verb == "создай":
            filename = params.get("файл", "")
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Создано Jarvis\n")
                return f"Файл создан: {filename}"
            except Exception as e:
                return f"Ошибка создания: {e}"
        
        elif verb == "удали":
            filename = params.get("файл", "")
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    return f"Удалено: {filename}"
                except:
                    return f"Ошибка удаления: {filename}"
            else:
                return f"Файл не найден: {filename}"
        
        elif verb == "посчитай":
            expr = params.get("выражение", "")
            try:
                result = eval(expr)
                return f"{expr} = {result}"
            except:
                return f"Ошибка вычисления: {expr}"
        
        return f"Действие не реализовано: {verb}"
    
    def process(self, user_input):
        action, confidence = self.find_action(user_input)
        
        if not action:
            verbs = ", ".join(list(self.actions.keys())[:5])
            return {
                "success": False,
                "message": f"Не распознано. Используйте: {verbs}..."
            }
        
        # Simple parameter extraction
        verb = action["verb"]
        params_text = user_input[len(verb):].strip() if user_input.startswith(verb) else user_input
        params = {}
        
        if action["params"]:
            param_name = action["params"][0]
            params[param_name] = params_text
        
        result = self.execute(action, params)
        
        return {
            "success": True,
            "verb": verb,
            "confidence": confidence,
            "result": result
        }

# Windows PowerShell запуск
if __name__ == "__main__":
    print("Verb Interpreter Test (Windows)")
    print("=" * 40)
    
    interpreter = VerbInterpreter()
    
    test_commands = [
        "напиши привет мир",
        "прочитай test.txt",
        "создай новый.txt",
        "посчитай 10+5*2"
    ]
    
    for cmd in test_commands:
        print(f"\nВвод: {cmd}")
        response = interpreter.process(cmd)
        
        if response["success"]:
            print(f"OK: {response['result']}")
        else:
            print(f"ERROR: {response['message']}")