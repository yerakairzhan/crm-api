# CRM Backend API (NestJS)

Production-style backend for task and comment management with role-based access, JWT auth, PostgreSQL, Swagger docs, tests, and CI.

## Project links
- Repository: [https://github.com/yerakairzhan/crm-api](https://github.com/yerakairzhan/crm-api)
- Main branch (NestJS): `main`
- Alternative implementation (FastAPI): [https://github.com/yerakairzhan/crm-api/tree/fastapi](https://github.com/yerakairzhan/crm-api/tree/fastapi)

## Stack
- NestJS
- TypeScript
- TypeORM
- PostgreSQL
- JWT (access + refresh)
- Swagger/OpenAPI
- Jest
- GitHub Actions
- Docker / Docker Compose

## Domain model
- `User`: `id`, `email`, `password`, `role`, `task_id`, `created_at`, `updated_at`
- `Task`: `id`, `user_id`, `description`, `comment`, `created_at`, `updated_at`
- `Comment`: `id`, `task_id`, `user_id`, `text`, `created_at`, `updated_at`

## Access rules
- Only role `user` can create tasks.
- Only role `author` can create comments.
- Update/delete operations are owner-only for tasks and comments.
- Tasks and comments are returned newest first.
- One task has many comments; one comment belongs to one task.

## API overview
### Auth
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`

### Users
- `POST /users`
- `GET /users`
- `GET /users/:id`
- `PATCH /users/:id`
- `DELETE /users/:id`

### Tasks
- `POST /tasks`
- `GET /tasks`
- `GET /tasks/:id`
- `PATCH /tasks/:id`
- `DELETE /tasks/:id`

### Comments
- `POST /comments`
- `GET /comments`
- `GET /comments?task_id=...`
- `GET /comments/:id`
- `PATCH /comments/:id`
- `DELETE /comments/:id`

## Run with Docker
```bash
docker compose up --build
```

- API: `http://localhost:3000`
- PostgreSQL: `postgresql://postgres:postgres@localhost:5434/crm_db`

## Run locally
```bash
npm install
cp .env.example .env
npm run start:dev
```

## Environment
From `.env.example`:
- `NODE_ENV`
- `PORT`
- `DB_HOST`
- `DB_PORT`
- `DB_USERNAME`
- `DB_PASSWORD`
- `DB_NAME`
- `JWT_SECRET`

## Swagger
- UI: `http://localhost:3000/docs`
- OpenAPI JSON: `http://localhost:3000/docs-json`

## Tests
```bash
npm test
npm run test:cov
```

## CI
Workflow: `.github/workflows/ci.yml`
- lint
- tests + coverage
- docker build
- security checks (`npm audit`, Snyk)
