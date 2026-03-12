# Secure Task Manager

Secure Task Manager is a Django web application for managing personal tasks with session-based authentication, per-user authorization, and a Docker-first deployment workflow. The backend is intentionally simple: Django handles routing, forms, sessions, CSRF protection, and ORM access; the `tasks` app owns the task domain; the `accounts` app owns registration and authentication views.

## Tech stack

- Python 3.12
- Django 6
- Gunicorn
- PostgreSQL for containerized deployment
- SQLite for lightweight local development
- WhiteNoise for static files
- Docker and Docker Compose
- GitHub Actions

## Quick start with Docker

Docker is the primary installation path for this project.

### 1. Prepare environment variables

```bash
cp .env.example .env
```

Set at least:

```bash
SECRET_KEY=replace-this
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
DATABASE_URL=postgresql://django:secure_password_change_this@db:5432/taskmanager
```

### 2. Build and start the stack

```bash
docker compose up --build
```

### 3. Create an admin user

```bash
docker compose exec web python manage.py createsuperuser
```

### 4. Open the application

- App: `http://localhost`
- Admin: `http://localhost/admin/`

## Local development without Docker

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

If `DATABASE_URL` is not set, Django falls back to SQLite.

## Backend overview

This backend is split into two Django apps and a project configuration package.

### `accounts`

The `accounts` app handles user registration and logout behavior. Registration uses a custom form built on top of Django’s `UserCreationForm`, adds email capture, and rejects duplicate email addresses. Authentication itself is still powered by Django’s built-in auth system and session middleware.

### `tasks`

The `tasks` app owns the `Task` model, forms, list view, create/edit flows, and task state transitions. Every task belongs to a Django `User` through a foreign key. The important authorization rule is that task mutations are resolved through the authenticated user, not by primary key alone.

### `config`

The `config` package contains Django settings, URL routing, and WSGI/ASGI entrypoints. Settings are environment-driven, with secure defaults for production-oriented deployments behind a reverse proxy.

## Data model

The core model is `Task`:

- `user`: owner of the task
- `title`: short required title
- `description`: optional text
- `priority`: `low`, `medium`, or `high`
- `completed`: boolean completion flag
- `created_at`: creation timestamp
- `due_date`: optional due date

The task list view sorts incomplete items before completed ones, then prioritizes higher-priority tasks, then earlier due dates.

## Authentication and authorization

Authentication is session-based and uses Django’s built-in auth framework.

### Authentication flow

1. A user registers through `/accounts/register/`.
2. Django hashes the password using its configured password hasher.
3. The user logs in through `/accounts/login/`.
4. Django creates a session and stores the authenticated user ID in the session backend.
5. On later requests, `AuthenticationMiddleware` attaches `request.user`.

### Authorization flow

Authorization is enforced at the view layer.

- Views that require a user are protected with `@login_required`.
- State-changing routes use `POST`.
- Task ownership is checked with a user-scoped lookup:

```python
get_object_or_404(Task, pk=pk, user=request.user)
```

That prevents one authenticated user from editing, deleting, or toggling another user’s tasks even if they know the object ID.

## HTTP routes

This project is a server-rendered Django app, not a JSON API. The backend still exposes a clear set of HTTP endpoints.

### Authentication routes

- `GET /accounts/register/`: registration form
- `POST /accounts/register/`: create account
- `GET /accounts/login/`: login form
- `POST /accounts/login/`: authenticate user
- `POST /accounts/logout/`: terminate current session

### Task routes

- `GET /`: list current user’s tasks
- `GET /create/`: render create-task form
- `POST /create/submit/`: create a task for the authenticated user
- `GET /edit/<id>/`: render edit form for the owner’s task
- `POST /edit/<id>/`: update the owner’s task
- `POST /delete/<id>/`: delete the owner’s task
- `POST /toggle/<id>/`: toggle completion status for the owner’s task

### Admin route

- `GET /admin/`: Django admin

## Security notes

The backend currently relies on Django’s built-in protections plus deployment settings from the environment.

- CSRF protection is enabled through Django middleware and template tokens.
- Password validation uses Django’s default validators.
- Secure cookie flags can be enabled from environment variables.
- `SECURE_PROXY_SSL_HEADER` is configured for reverse-proxy deployments.
- WhiteNoise serves static assets from the Django container.

For public deployment, review these variables carefully:

```bash
DEBUG=False
ALLOWED_HOSTS=your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Docker architecture

The default Compose stack runs three services:

- `db`: PostgreSQL 16
- `web`: Django application served by Gunicorn
- `nginx`: reverse proxy in front of the Django container

At container startup, `entrypoint.sh` runs:

1. `python manage.py migrate --noinput`
2. `python manage.py collectstatic --noinput`
3. Gunicorn

That gives a predictable startup path for local deployment and simple VPS hosting.

## CI

GitHub Actions is configured in `.github/workflows/ci.yml`.

The workflow runs:

- dependency installation
- `python manage.py check`
- `python manage.py test`
- Docker image build validation

## Useful commands

```bash
python3 manage.py check
python3 manage.py check --deploy
python3 manage.py test
python3 manage.py showmigrations
docker compose logs -f web
docker compose exec db pg_dump -U django taskmanager > backup.sql
```

## License

This project is licensed under the MIT License. See `LICENSE`.
