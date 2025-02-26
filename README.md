# Django Stripe Checkout Integration

Этот проект демонстрирует интеграцию Stripe Checkout в Django для обработки платежей. Пользователи могут покупать товары или заказы, а Stripe обрабатывает платежи через безопасную платежную страницу.

## Основные функции

- Покупка отдельных товаров через Stripe Checkout.
- Покупка заказов (групп товаров) с поддержкой скидок и налогов.
- Интеграция с Stripe API для создания платежных сессий.
- Простая настройка через `.env` файл.

---

## Технологии

- **Python** (3.11+)
- **Django** (4.2+)
- **Stripe** (для обработки платежей)
- **PostgreSQL** (база данных)
- **Docker** (опционально, для контейнеризации)

---

## Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/ваш-username/ваш-репозиторий.git
cd ваш-репозиторий
```

### 2. Настройте переменные окружения

Создайте файл `.env` в корне проекта и добавьте следующие переменные:

```plaintext
# Django
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
URL=http://127.0.0.1:8000

# Stripe (тестовые ключи)
STRIPE_API_KEY_USD=sk_test_ваш-ключ
STRIPE_PUBLIC_KEY_USD=pk_test_ваш-ключ
STRIPE_API_KEY_RUB=sk_test_ваш-ключ
STRIPE_PUBLIC_KEY_RUB=pk_test_ваш-ключ

# База данных
POSTGRES_DB=db
POSTGRES_USER=user
POSTGRES_PASSWORD=pas
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Примените миграции

```bash
python manage.py migrate
```

### 5. Запустите сервер

```bash
python manage.py runserver
```

---

## Использование

### 1. Покупка товара

1. Перейдите на страницу товара: `http://127.0.0.1:8000/item/1/`.
2. Нажмите кнопку **Buy Now**.
3. Вы будете перенаправлены на страницу Stripe Checkout для завершения платежа.

### 2. Покупка заказа

1. Перейдите на страницу заказа: `http://127.0.0.1:8000/order/1/`.
2. Нажмите кнопку **Buy Now**.
3. Вы будете перенаправлены на страницу Stripe Checkout для завершения платежа.

---

## Структура проекта

```
DjangoStripeAPI/
├── pay/
│   ├── migrations/          # Миграции базы данных
│   ├── templates/           # HTML-шаблоны
│   ├── __init__.py
│   ├── admin.py             # Админка Django
│   ├── apps.py
│   ├── models.py            # Модели (Item, Order, Discount, Tax)
│   ├── tests.py
│   ├── urls.py              # Маршруты приложения
│   └── views.py             # Логика представлений
├── DjangoStripeAPI/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Настройки Django
│   ├── urls.py              # Главные маршруты
│   └── wsgi.py
├── .env                     # Переменные окружения
├── .gitignore
├── Dockerfile               # Конфигурация Docker
├── docker-compose.yml       # Docker Compose
├── manage.py
├── README.md                # Этот файл
└── requirements.txt         # Зависимости
```

---

## Docker

Проект можно запустить с помощью Docker:

### 1. Соберите и запустите контейнеры:

```bash
docker-compose up --build
```

### 2. Примените миграции:

```bash
docker-compose exec web python manage.py migrate
```

### 3. Перейдите на `http://localhost:8000/`.

