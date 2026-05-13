# API организационной структуры

REST API для управления иерархической структурой подразделений и сотрудниками. Позволяет создавать, редактировать, просматривать дерево подразделений и управлять сотрудниками внутри них.

## Технологии

- **Python 3.13+**
- **FastAPI** – современный веб-фреймворк
- **SQLAlchemy 2.0 (async)** – ORM для работы с PostgreSQL
- **PostgreSQL 16** – надёжная реляционная база данных
- **Alembic** – миграции схемы БД
- **Docker / Docker Compose** – контейнеризация и запуск
- **Pytest** – тестирование API

## Струтура проекта 

      org_structure/
      ├── app/                   # Исходный код приложения
      │   ├── api/               # Слой представления (API)
      │   │   ├── deps.py        # Зависимости FastAPI
      │   │   ├── errors.py      # Обработчики ошибок
      │   │   └── v1/            # Версия API
      │   │       ├── router.py  # Агрегация роутеров
      │   │       ├── departments.py  # Эндпоинты подразделений
      │   │       └── employees.py    # Эндпоинты сотрудников
      │   ├── core/              # Конфигурация и инфраструктура
      │   │   ├── config.py      # Настройки (БД, логгер)
      │   │   ├── database.py    # Асинхронное подключение к БД
      │   │   └── logging.py     # Инициализация логирования
      │   ├── models/            # SQLAlchemy ORM-модели
      │   │   └── org.py         # Department и Employee
      │   ├── repositories/      # Работа с базой данных
      │   │   ├── base.py        # Базовый репозиторий
      │   │   ├── department.py  # Репозиторий подразделений
      │   │   └── employee.py    # Репозиторий сотрудников
      │   ├── schemas/           # Pydantic-схемы (запросы/ответы)
      │   │   ├── department.py  # Схемы подразделений
      │   │   └── employee.py    # Схемы сотрудников
      │   └── main.py            # Точка входа FastAPI
      ├── migrations/            # Миграции Alembic
      │   ├── env.py             # Конфигурация Alembic
      │   └── versions/          # Файлы миграций
      ├── tests/                 # Автоматические тесты
      │   ├── conftest.py        # Фикстуры (БД, клиент)
      │   ├── test_departments.py # Тесты подразделений
      │   └── test_employees.py  # Тесты сотрудников
      ├── docker-compose.yml     # Описание сервисов
      ├── Dockerfile             # Инструкция сборки образа
      ├── pyproject.toml         # Зависимости и настройки
      ├── alembic.ini            # Базовые настройки Alembic
      └── README.md

## Инструкция по запуску

Убедитесь, что у вас установлены **Docker** и **Docker Compose**.

   ```bash
   git clone <repo-url>
   docker-compose up --build
   ```

Интерактивная документация (Swagger UI):
http://localhost:8000/docs
