# jarvis.py (обновлённая версия)
from verb_interpreter import VerbInterpreter

def main():
    print("=" * 60)
    print("🤖 JARVIS - Python Knowledge Assistant")
    print("💡 Знает о builtins, модулях и паттернах Python")
    print("=" * 60)
    
    interpreter = VerbInterpreter("data/action_dictionary.json")
    
    print("\n✨ **Доступные команды:**")
    print("  1. Пользовательские команды:")
    print("     • напиши [текст] - записать в файл")
    print("     • посчитай [выражение] - вычислить")
    print("")
    print("  2. Поиск в Python:")
    print("     • 'что ты умеешь' - возможности Python")
    print("     • 'найди в python [запрос]' - поиск функций")
    print("     • 'как сделать [задача]' - получить код")
    print("")
    print("  3. Управление словарём:")
    print("     • 'где словарь' - путь к файлу команд")
    print("     • 'обновить словарь' - добавить новые команды")
    print("")
    print("💬 Попробуйте: 'найди в python работа с файлами'")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n👤 Вы: ").strip()
            
            if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
                print("\n👋 До свидания!")
                break
            
            if not user_input:
                continue
            
            result = interpreter.process(user_input)
            
            if result["success"]:
                print(f"\n🤖 Jarvis: {result['message']}")
            else:
                print(f"\n🤖 Jarvis: {result['message']}")
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Прервано")
            break
        except Exception as e:
            print(f"\n🔥 Ошибка: {e}")

if __name__ == "__main__":
    main()