#!/bin/bash
set -e

# 1. Міграції
echo "Applying database migrations..."
python manage.py migrate

# 2. Завантаження тестових даних (fixtures)
echo "Loading initial data..."
python manage.py loaddata shop/fixtures/initial_data.json || true

# 3. Запуск сервера
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
