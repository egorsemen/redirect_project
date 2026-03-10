# URL Shortener API

Микросервис для сокращения длинных ссылок на FastAPI с подсчетом переходов.

## Технологический стек
* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Validation:** Pydantic
* **Containerization:** Docker / Docker-compose
* **Testing:** Pytest / TestClient

## Функциональные возможности
1. `POST /shorten` — Создание короткого ID для длинной ссылки. Валидация URL через Pydantic.
2. `GET /{short_id}` — Редирект (307 Temporary Redirect) на оригинальный URL с обновлением счетчика кликов.
3. `GET /stats/{short_id}` — Получение статистики переходов по ссылке.

## Как запустить

### 1. Окружение
Создайте файл `.env` в корневой папке (на основе `.env.example`):
```text
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/shortener_db
```

### 2. Сборка и запуск контейнеров
Убедитесь, что у вас установлен Docker, и выполните команду:

```bash
docker-compose up --build 
```

API будет доступно по адресу: `http://localhost:8000`

Интерактивная документация (Swagger): `http://localhost:8000/docs`

### 3. Запуск тестов
Для проверки работоспособности выполните:

```bash
pytest
```

