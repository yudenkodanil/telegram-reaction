FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Каталоги для сессии и логов
RUN mkdir -p /app/session /app/logs

CMD ["python", "-m", "app.main"]
