import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
PATTERNS_FILE = DATA_DIR / "patterns.json"
ERROR_DB_FILE = DATA_DIR / "error_db.json"
CONTEXT_FILE = DATA_DIR / "context.json"

EMBEDDING_DIM = 384
SIMILARITY_THRESHOLD = 0.7

SAFE_MODULES = ["math", "datetime", "json", "pathlib", "os", "sys", "re"]
BANNED_KEYWORDS = ["__import__", "eval", "exec", "compile"]

MAX_CODE_LENGTH = 1000
MAX_VARIABLES = 10
