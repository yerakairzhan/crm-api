# CRM API (FastAPI)

Production-style REST API for task and comment management with JWT auth, role-based access control, PostgreSQL, automated tests, and CI.

## Project links
- Repository: [https://github.com/yerakairzhan/crm-api](https://github.com/yerakairzhan/crm-api)
- FastAPI branch: `fastapi`
- NestJS implementation: [https://github.com/yerakairzhan/crm-api/tree/main](https://github.com/yerakairzhan/crm-api/tree/main)

## Stack
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT (access + refresh)
- Pytest
- GitHub Actions
- Docker / Docker Compose

## Roles and permissions
- `user` can create tasks.
- `author` can create comments.
- Only resource owner can update/delete tasks and comments.

## Data model
- `User`: `id`, `email`, `password`, `role`, `task_id`, `created_at`, `updated_at`
- `Task`: `id`, `user_id`, `description`, `comment`, `created_at`, `updated_at`
- `Comment`: `id`, `task_id`, `user_id`, `text`, `created_at`, `updated_at`

## API overview
### Auth
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`

### Users
- `POST /users/`
- `GET /users/`
- `GET /users/{id}`
- `PATCH /users/{id}`
- `DELETE /users/{id}`

### Tasks
- `POST /tasks/`
- `GET /tasks/`
- `GET /tasks/{id}`
- `PATCH /tasks/{id}`
- `DELETE /tasks/{id}`

### Comments
- `POST /comments/`
- `GET /comments/`
- `GET /comments/?task_id=...`
- `GET /comments/{id}`
- `PATCH /comments/{id}`
- `DELETE /comments/{id}`

## Run with Docker
```bash
docker compose up --build
```

- API: `http://localhost:8001`
- PostgreSQL: `postgresql://postgres:postgres@localhost:5434/task_manager`

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
export DATABASE_URL="postgresql://postgres:postgres@localhost:5434/task_manager"
export SECRET_KEY="change-me"
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Tests
```bash
pytest -q
```

Current suite covers auth, users, tasks, comments, role restrictions, ownership checks, and validation scenarios.

## Environment variables
- `DATABASE_URL`
- `SECRET_KEY`
