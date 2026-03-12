# Secure Task Manager

Secure Task Manager is a server-rendered Django application for authenticated users to manage personal tasks with priority and due-date tracking. The codebase is intentionally small, but it now includes the baseline controls expected in a production-minded Django service: object-level authorization, safer state-changing routes, containerized deployment, and CI validation.

## What changed

- Hardened authentication and authorization flow.
- Restricted task mutation to the owning user.
- Moved destructive and state-changing actions to `POST`.
- Added registration with unique email capture.
- Improved security-related settings for reverse-proxy deployments.
- Fixed PostgreSQL container support by adding a database driver.
- Added Docker entrypoint orchestration and GitHub Actions CI.
- Rewrote the project documentation to reflect how the app actually runs.

## Stack

- Python 3.12
- Django 6.0
- Gunicorn
- PostgreSQL or SQLite
- WhiteNoise for static assets
- Docker and Docker Compose
- GitHub Actions

## Application capabilities

- User registration, login, and logout
- Per-user task isolation
- Task creation, editing, deletion, and completion toggle
- Priority-aware task ordering
- Optional due dates
- Django admin for operational access

## Security posture

The application uses Django’s built-in authentication system and standard middleware protections, with a few important improvements:

- Every task lookup used for edit, delete, or completion toggle is scoped to `request.user`.
- Logout, delete, toggle, and create submission paths use `POST`, which removes unsafe state changes over `GET`.
- CSRF middleware is active across forms.
- Secure cookie and transport settings are configurable from environment variables.
- Proxy-aware SSL handling is enabled for deployments behind Nginx or another load balancer.
- Password validation uses Django’s built-in validators.

This is still a session-based web app, not a multi-tenant platform. If you plan to expose it publicly, review `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, TLS termination, and secret management before deployment.

## Project layout

```text
.
├── accounts/                  # Registration and auth-related views/templates
├── tasks/                     # Task domain logic, forms, templates, tests
├── config/                    # Django settings and root URL configuration
├── .github/workflows/ci.yml   # CI checks and Docker build validation
├── Dockerfile                 # Production image
├── docker-compose.yml         # App + PostgreSQL + Nginx local/prod-style stack
├── entrypoint.sh              # Migrations and collectstatic before app start
├── nginx.conf                 # Reverse proxy and static file config
└── requirements.txt
```

## Local development

### Prerequisites

- Python 3.12
- `pip`
- virtual environment tooling

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The default database is SQLite unless `DATABASE_URL` is set.

## Environment configuration

The project reads configuration from environment variables through `python-decouple`.

Core variables:

```bash
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://localhost
DATABASE_URL=sqlite:///db.sqlite3
```

Production-oriented variables:

```bash
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

If TLS is terminated upstream, keep `SECURE_PROXY_SSL_HEADER` aligned with your proxy configuration.

## Running with Docker

The containerized stack includes:

- `db`: PostgreSQL 16
- `web`: Django + Gunicorn
- `nginx`: reverse proxy in front of the app

### Start the stack

```bash
cp .env.example .env
docker compose up --build
```

### Create an admin user

```bash
docker compose exec web python manage.py createsuperuser
```

### Stop the stack

```bash
docker compose down
```

The image entrypoint runs `migrate` and `collectstatic` before starting Gunicorn. That keeps startup deterministic in local and simple server deployments.

## Quality gates

### Run checks locally

```bash
python manage.py check
python manage.py test
```

### GitHub Actions

`.github/workflows/ci.yml` runs:

- dependency installation
- `python manage.py check`
- `python manage.py test`
- Docker image build validation

That gives you a minimum safety net for framework-level regressions and packaging failures.

## Auth and authorization notes

The highest-risk issue in the original codebase was authorization, not authentication. Login was present, but task mutation views fetched tasks by primary key only. In Django, that means any authenticated user who can guess another task ID could edit, delete, or toggle it unless the queryset is scoped properly.

The refactor addresses that by resolving tasks through the authenticated user:

```python
get_object_or_404(Task, pk=pk, user=request.user)
```

That pattern should remain the default for any future task-specific action.

## Testing focus

The current test suite covers:

- registration and login session behavior
- duplicate email rejection on sign-up
- logout method restrictions
- per-user task visibility
- owner-only edit, delete, and toggle behavior
- task creation ownership assignment

If the project grows, the next logical step is splitting unit tests from request/flow tests and adding coverage for forms plus admin behavior.

## Suggested next improvements

- Replace the built-in `User` model with a custom user model before the project grows further.
- Introduce service or selector layers if task workflows become more complex.
- Add structured logging and Sentry or OpenTelemetry instrumentation.
- Add pagination and filtering once task counts increase.
- Consider Django REST Framework only if an API is actually needed.

## Operations

Useful commands:

```bash
python manage.py showmigrations
python manage.py check --deploy
docker compose logs -f web
docker compose exec db pg_dump -U django taskmanager > backup.sql
```

## License

Add the project license explicitly if you intend to distribute or open-source this repository.
