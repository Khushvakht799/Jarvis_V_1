import ast
import sys
import io
import importlib
from contextlib import redirect_stdout, redirect_stderr
from typing import Tuple, Any, Optional

class CodeExecutor:
    def __init__(self, safe_mode: bool = True):
        self.safe_mode = safe_mode
        self.local_vars = {}
    
    def execute(self, code: str, variables: Optional[dict] = None) -> Tuple[bool, str, Any]:
        """Безопасное выполнение кода Python с подстановкой переменных"""
        try:
            # 1. Подставляем переменные
            if variables:
                for key, value in variables.items():
                    placeholder = f"{{{key}}}"
                    code = code.replace(placeholder, str(value))
            
            # 2. Проверка безопасности
            if self.safe_mode:
                self._validate_code(code)
            
            # 3. Создаем безопасное окружение
            safe_globals = self._create_safe_globals()
            
            # 4. Выполняем код
            output = io.StringIO()
            with redirect_stdout(output), redirect_stderr(output):
                exec(code, safe_globals, self.local_vars)
            
            # 5. Получаем результат
            result = self.local_vars.get('result', None)
            return True, output.getvalue(), result
            
        except Exception as e:
            return False, str(e), None
    
    def _create_safe_globals(self):
        """Создает безопасное глобальное окружение"""
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
                'round': round,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
                'bool': bool,
                'type': type,
                'isinstance': isinstance
            }
        }
        
        # Добавляем разрешенные модули
        allowed_modules = ['math', 'datetime', 'random']
        for module_name in allowed_modules:
            try:
                safe_globals[module_name] = importlib.import_module(module_name)
            except ImportError:
                pass
        
        return safe_globals
    
    def _validate_code(self, code: str):
        """Проверка кода на безопасность"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            raise ValueError("Некорректный синтаксис Python")
        
        # Запрещенные конструкции
        banned = ['eval', 'exec', 'compile', '__import__', 'open']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in banned:
                        raise SecurityError(f"Использование {node.func.id} запрещено")

class SecurityError(Exception):
    pass
