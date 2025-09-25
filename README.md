### Запуск в докере

cp .env.example .env

```
docker-compose up -d --build
```

### Доступ к API
- **Swagger UI**: http://localhost:8000/docs
-  **ReDoc**: http://localhost:8000/redoc
-  **API**: http://localhost:8000

## Архитектура

- **Domain** - бизнес-логика и модели
- **Application** - схемы
- **Infrastructure** - реализация репозиториев и базы данных
- **API** - REST API эндпоинты

##  Технологии

- **Python 3.13** - основной язык
- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **Alembic** - миграции БД
- **PostgreSQL** - база данных
- **Docker** - контейнеризация

##  Разработка

### Локальный запуск
```bash
pip install -r requirements-dev.lock

alembic upgrade head

python src/main.py
```


