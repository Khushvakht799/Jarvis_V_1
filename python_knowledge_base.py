# python_knowledge_base.py
"""
База знаний о возможностях Python для Jarvis
"""

PYTHON_KNOWLEDGE = {
    "builtins": {
        "print": {
            "description": "Выводит текст в консоль",
            "usage": "print('текст')",
            "examples": ["print('Привет мир')", "print(2+2)"],
            "category": "output"
        },
        "len": {
            "description": "Возвращает длину объекта",
            "usage": "len(объект)",
            "examples": ["len('строка')", "len([1,2,3])"],
            "category": "data"
        },
        "input": {
            "description": "Читает ввод пользователя",
            "usage": "input('подсказка')",
            "examples": ["name = input('Введите имя:')"],
            "category": "input"
        },
        "str": {
            "description": "Преобразует в строку",
            "usage": "str(объект)",
            "examples": ["str(123)", "str([1,2,3])"],
            "category": "conversion"
        },
        "int": {
            "description": "Преобразует в целое число",
            "usage": "int('строка')",
            "examples": ["int('42')", "int(3.14)"],
            "category": "conversion"
        },
        "float": {
            "description": "Преобразует в число с плавающей точкой",
            "usage": "float('строка')",
            "examples": ["float('3.14')"],
            "category": "conversion"
        },
        "list": {
            "description": "Создаёт список",
            "usage": "list(последовательность)",
            "examples": ["list('abc')", "list(range(5))"],
            "category": "data"
        },
        "dict": {
            "description": "Создаёт словарь",
            "usage": "dict(ключ=значение)",
            "examples": ["dict(name='John', age=30)"],
            "category": "data"
        },
        "range": {
            "description": "Создаёт последовательность чисел",
            "usage": "range(начало, конец, шаг)",
            "examples": ["range(5)", "range(1, 10, 2)"],
            "category": "data"
        },
        "type": {
            "description": "Возвращает тип объекта",
            "usage": "type(объект)",
            "examples": ["type('текст')", "type(42)"],
            "category": "debug"
        }
    },
    
    "modules": {
        "os": {
            "description": "Работа с операционной системой",
            "functions": ["os.listdir()", "os.getcwd()", "os.path.exists()"],
            "import": "import os",
            "category": "system"
        },
        "sys": {
            "description": "Доступ к системным параметрам",
            "functions": ["sys.argv", "sys.path", "sys.exit()"],
            "import": "import sys",
            "category": "system"
        },
        "math": {
            "description": "Математические функции",
            "functions": ["math.sqrt()", "math.sin()", "math.pi"],
            "import": "import math",
            "category": "math"
        },
        "datetime": {
            "description": "Работа с датой и временем",
            "functions": ["datetime.now()", "datetime.date()", "datetime.timedelta()"],
            "import": "from datetime import datetime",
            "category": "time"
        },
        "json": {
            "description": "Работа с JSON данными",
            "functions": ["json.load()", "json.dump()", "json.loads()"],
            "import": "import json",
            "category": "data"
        },
        "re": {
            "description": "Регулярные выражения",
            "functions": ["re.search()", "re.findall()", "re.sub()"],
            "import": "import re",
            "category": "text"
        },
        "random": {
            "description": "Генерация случайных чисел",
            "functions": ["random.randint()", "random.choice()", "random.random()"],
            "import": "import random",
            "category": "random"
        }
    },
    
    "common_patterns": {
        "вывести текст": "print('текст')",
        "посчитать выражение": "eval('выражение')",
        "прочитать файл": "with open('файл.txt', 'r') as f: content = f.read()",
        "записать в файл": "with open('файл.txt', 'w') as f: f.write('текст')",
        "создать список": "list = [1, 2, 3]",
        "создать словарь": "dict = {'ключ': 'значение'}",
        "проверить условие": "if условие: ... else: ...",
        "цикл по списку": "for item in список: print(item)",
        "обработать ошибку": "try: ... except Exception as e: ..."
    }
}