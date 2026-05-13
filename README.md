# Organizational Structure API

REST API для управления иерархической структурой подразделений и сотрудниками. Позволяет создавать, редактировать, просматривать дерево подразделений и управлять сотрудниками внутри них.

## Технологии

- **Python 3.13+**
- **FastAPI** – современный веб-фреймворк
- **SQLAlchemy 2.0 (async)** – ORM для работы с PostgreSQL
- **PostgreSQL 16** – надёжная реляционная база данных
- **Alembic** – миграции схемы БД
- **Docker / Docker Compose** – контейнеризация и запуск
- **Pytest** – тестирование API

## Инструкция по запуску

Убедитесь, что у вас установлены **Docker** и **Docker Compose**.

Клонируйте репозиторий:
   ```bash
   git clone <repo-url>
   docker-compose up --build
   ```

Интерактивная документация (Swagger UI):
http://localhost:8000/docs
