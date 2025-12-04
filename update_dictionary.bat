@echo off
chcp 65001 >nul
echo Обновление словаря глаголов Jarvis...
python extend_actions.py
pause
EOF