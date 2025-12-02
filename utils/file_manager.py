import json
import os
from pathlib import Path

def ensure_data_files():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    patterns_file = data_dir / "patterns.json"
    if not patterns_file.exists():
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump({"patterns": []}, f, indent=2)
        print("вњ… patterns.json СЃРѕР·РґР°РЅ")
    
    errors_file = data_dir / "error_db.json"
    if not errors_file.exists():
        with open(errors_file, 'w', encoding='utf-8') as f:
            json.dump({"errors": []}, f, indent=2)
        print("вњ… error_db.json СЃРѕР·РґР°РЅ")
    
    print("вњ… Р¤Р°Р№Р»С‹ РґР°РЅРЅС‹С… РіРѕС‚РѕРІС‹")
