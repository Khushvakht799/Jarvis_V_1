Write-Host "Запуск Jarvis с Embedding-овым словарем..." -ForegroundColor Cyan
Write-Host ""

if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    python jarvis.py
} else {
    python jarvis.py
}

Read-Host "
Нажмите Enter для выхода"
