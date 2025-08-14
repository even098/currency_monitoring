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
git clone https://github.com/username/currency_monitoring.git
cd currency_monitoring
```

### 2. Создать `.env` файл
```env
POSTGRES_DB=currency_db
POSTGRES_USER=currency_user
POSTGRES_PASSWORD=currency_pass
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*

TELEGRAM_BOT_TOKEN=your_tg_bot_token
CURRENCY_API_KEY=your_api_key
```

### 3. Запуск в Docker
```bash
docker-compose up --build
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
