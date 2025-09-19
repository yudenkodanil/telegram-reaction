ARG PYTHON_VERSION=3.11-slim
FROM python:${PYTHON_VERSION} AS base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Устанавливаем зависимости для сборки, потом удалим их
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем только requirements для кэширования слоя
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Копируем проект
COPY . .

# Создаём непривилегированного пользователя и даём права на /app
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser \
    && chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

# необязательно: healthcheck (предпочтительнее реализовать /health в приложении)
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
#   CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "main.py"]
