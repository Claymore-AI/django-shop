# 1. Базовий образ
FROM python:3.11-slim

# 2. Встановлюємо робочу директорію
WORKDIR /app

# 3. Копіюємо залежності
COPY requirements.txt .

# 4. Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копіюємо весь проєкт
COPY . .

# 6. Додаємо entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 7. Відкриваємо порт
EXPOSE 8000

# 8. Запускаємо через entrypoint
ENTRYPOINT ["/entrypoint.sh"]
