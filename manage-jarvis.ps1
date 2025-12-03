# Скрипт управления Jarvis (PowerShell)
param (
    [string]$Command = "help"
)

switch ($Command.ToLower()) {
    "start" {
        docker compose up -d
        Write-Host "Jarvis запущен"
    }
    "stop" {
        docker compose down
        Write-Host "Jarvis остановлен"
    }
    "restart" {
        docker compose restart
        Write-Host "Jarvis перезапущен"
    }
    "logs" {
        docker compose logs -f
    }
    "status" {
        docker compose ps
    }
    "update" {
        docker compose pull
        docker compose build --no-cache
        docker compose up -d
        Write-Host "Jarvis обновлён"
    }
    default {
        Write-Host "Использование: .\manage-jarvis.ps1 <команда>"
        Write-Host "Команды: start, stop, restart, logs, status, update"
    }
}
