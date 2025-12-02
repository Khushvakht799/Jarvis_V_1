import ast
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

class CodeExecutor:
    def __init__(self, safe_mode: bool = True):
        self.safe_mode = safe_mode
        self.local_vars = {}
    
    def execute(self, code: str):
        try:
            if self.safe_mode:
                self._validate_code(code)
            
            safe_globals = {
                \"__builtins__\": {
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
                    'set': set
                }
            }
            
            output = io.StringIO()
            with redirect_stdout(output), redirect_stderr(output):
                exec(code, safe_globals, self.local_vars)
            
            result = self.local_vars.get('result', None)
            return True, output.getvalue(), result
            
        except Exception as e:
            return False, str(e), None
    
    def _validate_code(self, code: str):
        try:
            tree = ast.parse(code)
        except SyntaxError:
            raise ValueError(\"Некорректный синтаксис Python\")
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                raise SecurityError(\"Импорт модулей запрещен\")
            
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec', 'compile', '__import__']:
                        raise SecurityError(f\"Использование {node.func.id} запрещено\")

class SecurityError(Exception):
    pass