#!/bin/bash
set -e

CONTAINER_NAME="telegram-reaction"
IMAGE_NAME="telegram-reaction-telegram-reaction"

echo "⛔ Останавливаю и удаляю контейнер $CONTAINER_NAME (если есть)..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

echo "🗑 Удаляю старый образ $IMAGE_NAME (если есть)..."
docker rmi $IMAGE_NAME 2>/dev/null || true

echo "🔨 Пересобираю образ без кэша..."
docker compose build --no-cache

echo "🚀 Запускаю контейнер с интерактивным вводом..."
docker compose run --rm telegram-reaction
