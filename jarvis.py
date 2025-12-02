#!/usr/bin/env python3
"""
Jarvis - AI Interface
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("рџ¤– Р—Р°РїСѓСЃРє Jarvis...")

# РџС‹С‚Р°РµРјСЃСЏ РёРјРїРѕСЂС‚РёСЂРѕРІР°С‚СЊ РјРѕРґСѓР»Рё
try:
    from core.interpreter import EmbeddingInterpreter
    from core.executor import CodeExecutor
    from utils.file_manager import ensure_data_files
    import config
    
    print("вњ… РњРѕРґСѓР»Рё Р·Р°РіСЂСѓР¶РµРЅС‹")
    
    # РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ
    ensure_data_files()
    interpreter = EmbeddingInterpreter()
    executor = CodeExecutor(safe_mode=True)
    
    print(f"вњ… РЎР»РѕРІР°СЂСЊ: {interpreter.get_vocab_size()} РіР»Р°РіРѕР»РѕРІ")
    
    # РРЅС‚РµСЂР°РєС‚РёРІРЅС‹Р№ СЂРµР¶РёРј
    while True:
        cmd = input("\nJarvis> ").strip()
        if cmd.lower() == 'exit':
            break
        
        result = interpreter.interpret(cmd)
        if result:
            template, vars, score = result
            print(f"вњ… ({score:.1%}): {template}")
            
            # РџРѕРґСЃС‚Р°РІР»СЏРµРј РїРµСЂРµРјРµРЅРЅС‹Рµ
            code = template
            for k, v in vars.items():
                code = code.replace(f"{{{k}}}", str(v))
            
            # Р’С‹РїРѕР»РЅСЏРµРј
            success, output, res = executor.execute(code)
            if success:
                print(f"Р РµР·СѓР»СЊС‚Р°С‚: {res}")
            else:
                print(f"РћС€РёР±РєР°: {output}")
        else:
            print("вќЊ РќРµ СЂР°СЃРїРѕР·РЅР°РЅРѕ")
            
except ImportError as e:
    print(f"вќЊ РћС€РёР±РєР° РёРјРїРѕСЂС‚Р°: {e}")
    print("РЎРѕР·РґР°Р№С‚Рµ РЅРµРґРѕСЃС‚Р°СЋС‰РёРµ РјРѕРґСѓР»Рё")
