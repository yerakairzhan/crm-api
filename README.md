# CRM Backend API — Комментарии к задачам (NestJS + TypeORM)

REST API модуль для CRM‑системы «Комментарии к задачам».  
Проект выполнен на **NestJS**, **TypeORM** и **PostgreSQL** с JWT‑аутентификацией (access + refresh).

**Репозиторий:** [https://github.com/yerakairzhan/crm-api](https://github.com/yerakairzhan/crm-api)  
**Основная ветка (NestJS):** `main`  
**Дополнительная реализация на Python/FastAPI:** [https://github.com/yerakairzhan/crm-api/tree/fastapi](https://github.com/yerakairzhan/crm-api/tree/fastapi)

---

## Зачем так сделано (аргументация решений)

1. **NestJS + TypeORM** — это прямое соблюдение требований и стабильная структура: модули, DI, сервисы и контроллеры упрощают тестирование и сопровождение.
2. **PostgreSQL** — промышленная СУБД, оптимальна для задач с отношениями (users → tasks → comments).
3. **JWT access + refresh** — минимально достаточная, но полноценная схема авторизации. Access — короткоживущий, refresh — продлевает сессию без повторного логина.
4. **RBAC (roles `user` / `author`)** — ключевые бизнес‑ограничения внедрены в сервисном слое, где проще всего контролировать доступ.
5. **DTO + class‑validator** — обеспечивает предсказуемые контракты и проверку входных данных по требованиям (1–1000 символов).
6. **Unit‑тесты + CI** — подтверждают корректность логики и дают автоматическую проверку проекта при каждом push/PR.

Цель — не просто “чтобы работало”, а чтобы было **воспроизводимо, проверяемо и безопасно**.

---

## Соответствие требованиям задания

### Технологии
- ✅ NestJS  
- ✅ TypeORM  
- ✅ PostgreSQL  
- ✅ TypeScript  

### Задача 1: Users
**Сущность User**: `id`, `password`, `role`, `task_id`, `created_at`, `updated_at`

**Эндпоинты:**
- `POST /users` — создать пользователя
- `GET /users/:id` — получить пользователя по ID
- `GET /users` — получить список всех пользователей
- `PATCH /users/:id` — редактировать пользователя
- `DELETE /users/:id` — удалить пользователя

### Задача 2: Tasks
**Сущность Task**: `id`, `user_id`, `description`, `comment`, `created_at`, `updated_at`

**Эндпоинты:**
- `POST /tasks` — создать задачу
- `GET /tasks/:id` — получить задачу по ID
- `GET /tasks` — получить список всех задач
- `PATCH /tasks/:id` — редактировать задачу
- `DELETE /tasks/:id` — удалить задачу

### Задача 3: Comments
**Сущность Comment**: `id`, `task_id`, `user_id`, `text`, `created_at`, `updated_at`

**Эндпоинты:**
- `POST /comments` — создать комментарий
- `GET /comments?task_id=xxx` — комментарии по задаче
- `GET /comments/:id` — получить комментарий по ID
- `PATCH /comments/:id` — редактировать комментарий
- `DELETE /comments/:id` — удалить комментарий

### Бизнес‑правила
- ✅ Создавать задачу может только роль `user`
- ✅ Создавать комментарий может только роль `author`
- ✅ Редактировать/удалять может только автор ресурса
- ✅ Сортировка задач/комментариев по дате (новые первыми)
- ✅ Связь: одна задача → много комментариев

---

## Архитектура и структура проекта

```
src/
├── auth/                    # JWT аутентификация (access + refresh)
├── users/                   # Users CRUD
├── tasks/                   # Tasks CRUD
├── comments/                # Comments CRUD
├── common/                  # Гварды/декораторы/базовые сущности
├── app.module.ts
└── main.ts
```

---

## Авторизация

**Основной флоу:**
1. `POST /users` — регистрация
2. `POST /auth/login` — получение `access_token` и `refresh_token`
3. `POST /auth/refresh` — обновление access‑токена
4. В защищенные эндпоинты передаем:
```
Authorization: Bearer <access_token>
```

---

## Запуск проекта

### Вариант 1: Docker (рекомендуется)

```bash
docker compose up --build
```

Сервис доступен:
```
http://localhost:3000
```

PostgreSQL доступен по порту **5434**:
```
postgresql://postgres:postgres@localhost:5434/crm_db
```

### Вариант 2: Локально

1. Установить зависимости:
```bash
npm install
```

2. Создать `.env` на основе `.env.example`
```bash
cp .env.example .env
```

3. Запуск:
```bash
npm run start:dev
```

---

## Переменные окружения

См. `.env.example`:

```
NODE_ENV=development
PORT=3000
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_NAME=crm_db
JWT_SECRET=your-secret-key-change-this-in-production
```

Для docker‑compose:
```
DB_PORT=5434
```

---

## Swagger / OpenAPI

Swagger подключен и доступен в проекте.

- UI документации: `http://localhost:3000/docs`
- OpenAPI JSON: `http://localhost:3000/docs-json`

Что документировано:
- все endpoint'ы `auth`, `users`, `tasks`, `comments`
- request/response схемы DTO
- коды ответов и основные ошибки (`400`, `401`, `403`, `404`, `409`)
- Bearer JWT авторизация в UI (`Authorize`)

Как использовать:
1. Выполнить `POST /auth/login` и получить `access_token`.
2. Нажать `Authorize` в Swagger UI.
3. Вставить токен в формате `Bearer <access_token>`.
4. Вызывать защищенные endpoint'ы прямо из Swagger.

---

## Тестирование

Unit‑тесты реализованы в модулях:
- `src/auth/auth.service.spec.ts`
- `src/users/users.service.spec.ts`
- `src/tasks/tasks.service.spec.ts`
- `src/comments/comments.service.spec.ts`

Запуск:
```bash
npm test
```

Покрытие:
```bash
npm run test:cov
```

---

## CI (GitHub Actions)

Workflow: `.github/workflows/ci.yml`  
Включает:
- ESLint
- Unit‑тесты и coverage
- Сборка Docker образа
- Security checks (`npm audit`, Snyk)

---

## Дополнительная ветка на Python/FastAPI

Ветка `fastapi` содержит альтернативную реализацию того же задания на **FastAPI + SQLAlchemy**:  
[https://github.com/yerakairzhan/crm-api/tree/fastapi](https://github.com/yerakairzhan/crm-api/tree/fastapi)

Это демонстрирует гибкость и способность работать с разными стек‑технологиями при сохранении требований.

---

## Почему меня стоит рассмотреть

- Я не просто «закрываю задачу», а делаю **поддерживаемый и проверяемый API**.
- Соблюдены все бизнес‑правила и архитектурные требования.
- Сделаны тесты и CI, чтобы гарантировать стабильность.
- Есть альтернативная реализация на Python, что показывает **широкий стек и способность быстро адаптироваться**.
