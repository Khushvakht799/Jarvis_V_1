# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём папку data если её нет (для сохранения файлов)
RUN mkdir -p data/embeddings

# Указываем точку входа (можно менять на jarvis.py или run.py)
CMD ["python", "jarvis.py"]
