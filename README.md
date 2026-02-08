# CRM API (FastAPI) — Комментарии к задачам

REST API модуль для CRM‑системы: пользователи, задачи и комментарии с JWT‑аутентификацией и ролевой моделью.

## Стек
- Python, FastAPI
- SQLAlchemy
- PostgreSQL
- JWT (access + refresh)

## Роли
- `user` — может создавать задачи
- `author` — может создавать комментарии

Пользователь может редактировать/удалять только свои задачи и комментарии.

## Запуск через Docker

1. Собрать и запустить сервисы:
```bash
docker compose up --build
```

2. API будет доступен:
- `http://localhost:8001`

PostgreSQL проброшен на порт `5434`:
- `postgresql://postgres:postgres@localhost:5434/task_manager`

## Локальный запуск без Docker

1. Установить зависимости:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
```

2. Экспортировать переменные окружения (пример):
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5434/task_manager"
export SECRET_KEY="change-me"
```

3. Запустить приложение:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Тесты

```bash
pytest -q
```

Тесты используют SQLite in‑memory, чтобы не зависеть от PostgreSQL.

## Основные эндпоинты

### Пользователи
- `POST /users/` — регистрация
- `POST /users/login` — логин (access/refresh токены)
- `POST /users/refresh` — обновление access токена
- `GET /users/` — список пользователей
- `GET /users/{id}` — пользователь по ID
- `PATCH /users/{id}` — обновление пользователя
- `DELETE /users/{id}` — удаление пользователя

### Задачи
- `POST /tasks/` — создать задачу (только роль `user`)
- `GET /tasks/` — список задач (новые первыми)
- `GET /tasks/{id}` — задача по ID
- `PATCH /tasks/{id}` — обновить задачу (только владелец)
- `DELETE /tasks/{id}` — удалить задачу (только владелец)

### Комментарии
- `POST /comments/` — создать комментарий (только роль `author`)
- `GET /comments/?task_id=...` — комментарии по задаче (новые первыми)
- `GET /comments/{id}` — комментарий по ID
- `PATCH /comments/{id}` — обновить комментарий (только владелец)
- `DELETE /comments/{id}` — удалить комментарий (только владелец)

## Бизнес‑правила
- Создавать задачи может только пользователь с ролью `user`
- Создавать комментарии может только пользователь с ролью `author`
- Редактировать и удалять задачи/комментарии может только их автор
- Список задач и комментариев отсортирован по дате (новые первыми)
- У задачи может быть несколько комментариев, комментарий принадлежит одной задаче

## Переменные окружения
- `DATABASE_URL` — строка подключения к БД
- `SECRET_KEY` — ключ для подписи JWT
