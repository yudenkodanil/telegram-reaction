FROM python:3.13-slim

WORKDIR /app

# Устанавливаем зависимости для сборки пакетов (gcc, make, libffi и т.д.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем проект
COPY . .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
