# 🛒 Django Shop - Інтернет-магазин

Повнофункціональний веб-додаток для управління каталогом товарів та кошиком покупок, розроблений на Django з підтримкою REST API.

## ✨ Основний функціонал

### 📦 Каталог товарів
- Перегляд товарів з пагінацією (6 товарів на сторінку)
- Фільтрація за категоріями
- Детальна інформація про кожен товар
- Зображення товарів
- Швидке додавання до кошика

### 🛍️ Кошик покупок
- Додавання товарів
- Зміна кількості
- Видалення позицій
- Автоматичний підрахунок суми
- Збереження через сесії (без реєстрації)

### 🔌 REST API
| Метод | Endpoint | Опис |
|-------|----------|------|
| GET | `/api/products/` | Список товарів (з фільтрацією) |
| GET | `/api/products/{id}/` | Деталі товару |
| GET | `/api/cart/` | Вміст кошика |
| POST | `/api/cart/` | Додати/оновити товар |
| DELETE | `/api/cart/` | Видалити товар |

## 🛠️ Технології

- **Backend:** Django 5.2.7, Django REST Framework 3.16.1
- **Database:** PostgreSQL 15
- **Frontend:** Bootstrap 5.3.0
- **Deployment:** Docker, Docker Compose
- **Tools:** Adminer (управління БД)

## 🚀 Швидкий старт з Docker

### Передумови
- Docker
- Docker Compose

### Запуск проєкту

1. **Клонування репозиторію**
```bash
git clone <repository-url>
cd DjangoProject
```

2. **Створення файлу .env**
```env
DEBUG=1
SECRET_KEY=supersecretkey123
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

POSTGRES_DB=shop_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

3. **Запуск контейнерів**
```bash
docker-compose build
```
- І запуск докера
```bash
docker-compose up
```

4. **Доступ до додатку**
- 🌐 Веб-додаток: http://localhost:8000
- 👨‍💼 Адмін-панель: http://localhost:8000/admin
- 🗄️ Adminer: http://localhost:8080

### Створення суперкористувача

```bash
docker-compose exec web python manage.py createsuperuser
```

### Зупинка контейнерів

```bash
docker-compose down
```

## 💻 Локальна установка (без Docker)

### 1. Підготовка середовища

```bash
# Клонування репозиторію
git clone <repository-url>
cd DjangoProject

# Створення віртуального середовища
python -m venv venv

# Активація (Linux/Mac)
source venv/bin/activate

# Активація (Windows)
venv\Scripts\activate

# Встановлення залежностей
pip install -r requirements.txt
```

### 2. Налаштування PostgreSQL

```sql
CREATE DATABASE shop_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE shop_db TO postgres;
```

### 3. Створення .env файлу

```env
DEBUG=1
SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

POSTGRES_DB=shop_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 4. Міграції та запуск

```bash
# Застосування міграцій
python manage.py migrate

# Завантаження тестових даних
python manage.py loaddata shop/fixtures/initial_data.json

# Створення суперкористувача
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver
```

## 📁 Структура проєкту

```
DjangoProject/
├── DjangoProject/              # Конфігурація проєкту
│   ├── settings.py             # Налаштування Django
│   ├── urls.py                 # Головні URL-маршрути
│   └── wsgi.py                 # WSGI конфігурація
│
├── shop/                       # Основний додаток
│   ├── models.py               # Моделі (Category, Product, Cart)
│   ├── views.py                # HTML-представлення
│   ├── api_views.py            # REST API представлення
│   ├── serializers.py          # DRF серіалізатори
│   ├── urls.py                 # URL-маршрути додатку
│   ├── admin.py                # Конфігурація адмін-панелі
│   └── fixtures/               # Тестові дані
│       └── initial_data.json
│
├── templates/                  # HTML-шаблони
│   └── shop/
│       ├── base.html           # Базовий шаблон
│       ├── product_list.html   # Каталог товарів
│       ├── product_detail.html # Деталі товару
│       └── cart.html           # Кошик
│
├── media/                      # Завантажені файли
├── staticfiles/                # Зібрана статика
├── docker-compose.yml          # Docker Compose конфігурація
├── Dockerfile                  # Docker образ
├── entrypoint.sh               # Скрипт запуску
├── requirements.txt            # Python залежності
└── .env                        # Змінні середовища
```

## 📡 Приклади використання API

### Отримання товарів

```bash
# Всі товари
curl http://localhost:8000/api/products/

# Фільтрація за категорією
curl http://localhost:8000/api/products/?category=1

# Конкретний товар
curl http://localhost:8000/api/products/1/
```

### Робота з кошиком

```bash
# Переглянути кошик (зберігайте cookies!)
curl -c cookies.txt http://localhost:8000/api/cart/

# Додати товар
curl -X POST http://localhost:8000/api/cart/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}' \
  -b cookies.txt -c cookies.txt

# Оновити кількість
curl -X POST http://localhost:8000/api/cart/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 5}' \
  -b cookies.txt -c cookies.txt

# Видалити товар
curl -X DELETE http://localhost:8000/api/cart/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}' \
  -b cookies.txt
```

### Відповіді API

**Список товарів:**
```json
{
  "count": 12,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Smartphone",
      "description": "Powerful Android phone",
      "price": "799.99",
      "image": "/media/products/phone.jpg",
      "category": {
        "id": 1,
        "name": "Electronics"
      }
    }
  ]
}
```

**Кошик:**
```json
{
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Smartphone",
        "price": "799.99",
        "category": {"id": 1, "name": "Electronics"}
      },
      "quantity": 2,
      "total_price": "1599.98"
    }
  ],
  "total": "1599.98"
}
```

## 🗂️ Тестові дані

Проєкт містить 12 товарів у 4 категоріях:

- **Electronics:** Smartphone, Laptop, Headphones, Smartwatch
- **Books:** Python for Beginners, Django Mastery
- **Clothing:** T-Shirt, Jeans, Jacket
- **Home & Kitchen:** Coffee Maker, Blender, Toaster

Дані автоматично завантажуються при запуску через Docker або вручну командою:
```bash
python manage.py loaddata shop/fixtures/initial_data.json
```

## 🔧 Корисні команди

### Docker

```bash
# Перезібрати контейнери
docker-compose up --build

# Запуск у фоновому режимі
docker-compose up -d

# Перегляд логів
docker-compose logs -f web

# Виконання команд в контейнері
docker-compose exec web python manage.py shell

# Очистити все (контейнери + volumes)
docker-compose down -v
```

### Django

```bash
# Створити міграції
python manage.py makemigrations

# Застосувати міграції
python manage.py migrate

# Створити суперкористувача
python manage.py createsuperuser

# Зібрати статичні файли
python manage.py collectstatic

# Відкрити Django shell
python manage.py shell
```

## 🔐 Безпека для production

⚠️ **Важливо!** Перед деплоєм змініть:

1. **SECRET_KEY** - згенеруйте новий унікальний ключ
2. **DEBUG** - встановіть `DEBUG=0`
3. **ALLOWED_HOSTS** - вкажіть свій домен
4. **POSTGRES_PASSWORD** - сильний пароль
5. Видаліть `.env` з репозиторію (додайте до `.gitignore`)

### .gitignore

```gitignore
*.pyc
__pycache__/
*.sqlite3
.env
venv/
env/
media/
staticfiles/
.DS_Store
.idea/
.vscode/
*.log
```

## 📝 Ліцензія

Цей проєкт створено для навчальних цілей.

## 🤝 Внесок

Будь-які пропозції та pull requests вітаються!

## 📧 Контакти

Якщо у вас виникли питання, створіть Issue в репозиторії.

---

**Приємної розробки! 🚀**