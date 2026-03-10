FROM python:3.11-slim

WORKDIR /app

# Запрещаем Python писать файлы .pyc и включаем немедленный вывод логов
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости Python
# Используем --no-cache-dir для уменьшения размера образа
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]