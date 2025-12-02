# Проверьте какие файлы есть
Get-ChildItem -Recurse

# Если нет каких-то файлов, создайте их:

# 1. Проверьте config.py
if (-not (Test-Path "config.py")) {
    @'
BASE_DIR = "."
DATA_DIR = "./data"
EMBEDDINGS_DIR = "./data/embeddings"
PATTERNS_FILE = "./data/patterns.json"
ERROR_DB_FILE = "./data/error_db.json"
SIMILARITY_THRESHOLD = 0.7
'@ | Out-File -FilePath "config.py" -Encoding UTF8
}

# 2. Проверьте __init__.py файлы
$initFiles = @("__init__.py", "core\__init__.py", "utils\__init__.py")
foreach ($file in $initFiles) {
    if (-not (Test-Path $file)) {
        "" | Out-File -FilePath $file -Encoding UTF8
        Write-Host "Создан: $file" -ForegroundColor Green
    }
}