import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Пути к данным
DATA_DIR = BASE_DIR / "data"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
PATTERNS_FILE = DATA_DIR / "patterns.json"
ERROR_DB_FILE = DATA_DIR / "error_db.json"
CONTEXT_FILE = DATA_DIR / "context.json"

# Embeddings files
VERB_EMBEDDINGS_FILE = EMBEDDINGS_DIR / "verb_embeddings.npy"
VERB_VOCAB_FILE = EMBEDDINGS_DIR / "verb_vocab.pkl"

# Настройки эмбеддингов
EMBEDDING_DIM = 384
SIMILARITY_THRESHOLD = 0.7
MAX_VECTORS = 10000

# Настройки безопасности
SAFE_MODULES = ["math", "datetime", "json", "pathlib", "os", "sys", "re"]
BANNED_KEYWORDS = ["__import__", "eval", "exec", "compile", "open", "delete"]

# Лимиты
MAX_CODE_LENGTH = 1000
MAX_VARIABLES = 10

# Настройки интерфейса
GUI_TITLE = "Jarvis - Python AI Interface"
GUI_SIZE = "900x700"