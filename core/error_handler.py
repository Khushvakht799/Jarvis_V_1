import json
import re
from pathlib import Path
from typing import Dict, List, Optional

class ErrorHandler:
    def __init__(self, error_db_file: Path):
        self.error_db_file = error_db_file
        self.error_db = self.load_error_db()
    
    def load_error_db(self) -> Dict:
        if self.error_db_file.exists():
            with open(self.error_db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"errors": []}
    
    def save_error_db(self):
        with open(self.error_db_file, 'w', encoding='utf-8') as f:
            json.dump(self.error_db, f, ensure_ascii=False, indent=2)
    
    def handle_error(self, error_msg: str) -> Optional[List[str]]:
        for error_entry in self.error_db["errors"]:
            if re.search(error_entry["pattern"], error_msg):
                return error_entry["solutions"]
        return None
    
    def add_error_solution(self, error_type: str, pattern: str, solutions: List[str]):
        new_entry = {
            "error_type": error_type,
            "pattern": pattern,
            "solutions": solutions,
            "prevention": ""
        }
        self.error_db["errors"].append(new_entry)
        self.save_error_db()