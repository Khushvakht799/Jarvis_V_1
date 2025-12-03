import ast
import sys
import io
from contextlib import redirect_stdout

class CodeExecutor:
    def __init__(self, safe_mode=True):
        self.safe_mode = safe_mode
        self.vars = {}
    
    def execute(self, code):
        try:
            if self.safe_mode:
                tree = ast.parse(code)
            
            safe_globals = {
                "__builtins__": {
                    'print': print,
                    'len': len,
                    'range': range,
                    'list': list,
                    'sum': sum,
                    'int': int,
                    'str': str,
                    'float': float
                }
            }
            
            output = io.StringIO()
            with redirect_stdout(output):
                exec(code, safe_globals, self.vars)
            
            result = self.vars.get('result', None)
            return True, output.getvalue(), result
            
        except Exception as e:
            return False, str(e), None
