# Currency Monitoring

Проект для отслеживания курса валют с автоматической рассылкой в Telegram.  
Бэкенд реализован на **Django Rest Framework**, фронтенд — Telegram-бот.  
Под капотом: **PostgreSQL**, **Docker**, **Celery**, **Celery Beat**, интеграция с внешними API для получения курсов валют.

---

## 🚀 Возможности
- Регистрация пользователей
- Получение списка валют и их актуальных курсов
- Подписка на интересующие валюты
- Изменение времени получения уведомлений
- Удаление подписок
- Автоматическое обновление курсов по расписанию

---

## 🛠 Технологии
- **Python 3.11**
- **Django Rest Framework**
- **PostgreSQL**
- **Docker** + **Docker Compose**
- **Celery** + **Celery Beat**
- **Redis** (брокер задач для Celery)
- **Aiogram** (Telegram-бот)
- **HTTPX / Requests** (для работы с внешними API)

---

## 📦 Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/even098/currency_monitoring.git
cd currency_monitoring
```

### 2. Создать `.env` файл
```env
SECRET_KEY=django_secret_key
API_URL='http://backend:8000/api'  # если работа через docker

BASE_URL=https://v6.exchangerate-api.com/v6
API_KEY=exchange_rates_api_key

BOT_TOKEN=telegram_bot_token

DB_NAME=currency_app_database
DB_USER=postgres
DB_PASSWORD=0910
DB_HOST=postgres
DB_PORT=5432

CELERY_BROKER_URL='redis://redis:6379/0'  # при работе через docker
CELERY_RESULT_BACKEND='redis://redis:6379/1'  # при работе через docker
```

### 3. Запуск в Docker
```bash
docker-compose up --build -d
```

---

## 🔌 API эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/register/` | Регистрация пользователя |
| `GET`  | `/currencies/` | Получение списка валют и их курсов |
| `POST` | `/subscribe/` | Подписка на валюту |
| `GET`  | `/subscriptions/` | Список подписок пользователя |
| `POST` | `/rates_update/` | Ручное обновление курсов валют |
| `POST` | `/change_notification_time/` | Изменение времени уведомлений |
| `POST` | `/delete_subscription/` | Удаление подписки |

---

## 🔄 Celery задачи
- **Обновление курсов валют** — выполняется по расписанию через **Celery Beat**
- **Отправка уведомлений в Telegram** в указанное пользователем время

---

## 🤖 Telegram-бот
Бот служит фронтендом проекта. Пользователь может:
- Зарегистрироваться
- Подписаться на валюты
- Изменить время уведомлений
- Отписаться от валют

---

## 🗂 Структура проекта
```
currency_monitoring/
├── backend/       # Django + DRF API
├── bot/           # Telegram бот (Aiogram)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```
