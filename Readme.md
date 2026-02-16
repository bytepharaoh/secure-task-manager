# Secure Task Manager

A production-ready Django task management application demonstrating modern web development practices, user authentication, and comprehensive security features. Built with Django 6.0.2 and Python 3.12.

## 🌐 Live Demo

**Production URL:** http://securetaskmanager.duckdns.org/

**Demo Credentials:**
- Username: `demo`
- Password: `demo2026`

*Feel free to explore all features. Demo account resets daily.*

---

## ✨ Features

### Core Functionality
- ✅ User authentication (registration, login, logout)
- ✅ Task CRUD operations (Create, Read, Update, Delete)
- ✅ Task priorities (Low, Medium, High)
- ✅ Due date tracking with calendar picker
- ✅ Task completion toggle
- ✅ Automatic sorting by priority and due date
- ✅ User isolation - each user sees only their tasks

### Security
- 🔒 Secure password hashing (Django PBKDF2)
- 🛡️ CSRF protection on all forms
- 🔐 Login-required view protection
- 🚫 SQL injection prevention (Django ORM)
- 🔑 Environment-based configuration
- ⚠️ Production-ready security headers

---

## 🏗️ Technical Stack

### Backend
- **Django 6.0.2** - Web framework
- **Python 3.12** - Programming language
- **Gunicorn** - WSGI HTTP server
- **PostgreSQL/SQLite** - Database
- **Whitenoise** - Static file serving

### Security & Configuration
- **python-decouple** - Environment variable management
- **dj-database-url** - Database configuration
- **Django Auth** - Built-in authentication system

### Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy & static files
- **Systemd** - Process management (alternative)

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

**Prerequisites:** Docker & Docker Compose installed

```bash
# 1. Clone repository
git clone https://github.com/bytepharaoh/secure-task-manager.git
cd secure-task-manager

# 2. Setup environment
cp .env.example .env
# Edit .env and set SECRET_KEY

# 3. Start containers
docker-compose up -d

# 4. Run migrations
docker-compose exec web python manage.py migrate

# 5. Create admin user
docker-compose exec web python manage.py createsuperuser

# 6. Access application
open http://localhost
```

**Full Docker documentation:** [DOCKER.md](DOCKER.md)

---

### Option 2: Local Development

**Prerequisites:** Python 3.12+, pip, virtualenv

```bash
# 1. Clone and setup environment
git clone https://github.com/bytepharaoh/secure-task-manager.git
cd secure-task-manager
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env
# Edit .env with your configuration

# 4. Setup database
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

# 5. Run development server
python manage.py runserver

# 6. Access at http://127.0.0.1:8000
```

---

## 📁 Project Structure

```
secure-task-manager/
├── accounts/              # Authentication app
│   ├── templates/         # Login & registration
│   ├── views.py
│   └── urls.py
├── tasks/                 # Task management app
│   ├── static/            # CSS, JavaScript
│   ├── templates/         # Task views
│   ├── models.py          # Data models
│   ├── forms.py           # Task forms
│   ├── views.py           # Business logic
│   └── urls.py
├── config/                # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Multi-container setup
├── nginx.conf             # Nginx configuration
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
└── manage.py
```

---

## 🔒 Security Features

### Authentication & Authorization
- Session-based authentication with secure cookies
- Password strength validation (min 8 chars, not all numeric)
- CSRF token protection on all state-changing operations
- Login-required decorators for protected views
- User-specific data isolation

### Configuration Security
- Environment variables for sensitive data (`.env` file)
- SECRET_KEY separation from codebase
- Debug mode disabled in production
- ALLOWED_HOSTS whitelist
- Security middleware enabled

### Production Headers
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
X_FRAME_OPTIONS = 'DENY'
```

### Database Security
- Django ORM prevents SQL injection
- Parameterized queries
- No raw SQL execution
- Password hashing with PBKDF2

---

## 🐳 Docker Deployment

### Architecture

```
┌─────────────────────────────┐
│  Nginx (Reverse Proxy)      │  Port 80
│  - Static file serving      │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  Django + Gunicorn           │  Port 8000
│  - Application server       │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  PostgreSQL Database         │  Port 5432
│  - Persistent storage       │
└─────────────────────────────┘
```

### Services
- **web** - Django application with Gunicorn
- **db** - PostgreSQL 16 database
- **nginx** - Reverse proxy and static file server

### Volumes
- `postgres_data` - Database persistence
- `static_volume` - Shared static files

### Environment Variables

Create `.env` file with:

```bash
SECRET_KEY=<generate-secure-key>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost
DATABASE_URL=postgresql://user:password@db:5432/dbname
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🔧 Development

### Running Tests

```bash
# Local
python manage.py test

# Docker
docker-compose exec web python manage.py test
```

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Code Quality

```bash
# Check for issues
python manage.py check

# Django deployment checklist
python manage.py check --deploy
```

---

## 📊 API Endpoints

### Authentication
- `GET /accounts/login/` - Login page
- `POST /accounts/login/` - Login submission
- `GET /accounts/register/` - Registration page
- `POST /accounts/register/` - Registration submission
- `POST /accounts/logout/` - Logout

### Tasks
- `GET /` - Task list (requires authentication)
- `GET /create/` - Create task form
- `POST /create/` - Create task submission
- `GET /edit/<id>/` - Edit task form
- `POST /edit/<id>/` - Edit task submission
- `GET /delete/<id>/` - Delete task (with confirmation)
- `GET /toggle/<id>/` - Toggle task completion

---

## 🔄 Update & Maintenance

### Update Application

```bash
# Docker deployment
docker-compose down
git pull origin main
docker-compose up -d --build
docker-compose exec web python manage.py migrate

# Traditional deployment
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Restart application server
```

### Backup Database

```bash
# Docker (PostgreSQL)
docker-compose exec db pg_dump -U django taskmanager > backup_$(date +%Y%m%d).sql

# Local (SQLite)
cp db.sqlite3 backups/db_$(date +%Y%m%d).sqlite3
```

---

## 📈 Performance & Scalability

### Current Capabilities
- Handles moderate traffic loads
- Efficient query optimization with Django ORM
- Static file caching with Whitenoise
- Database connection pooling

### Scaling Options
- Horizontal scaling with load balancer
- Database read replicas
- Redis for session storage and caching
- CDN for static assets
- Async task queue (Celery) for background jobs

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Follow PEP 8 style guide
4. Write tests for new features
5. Commit with clear messages (`git commit -m 'Add feature: ...'`)
6. Push to your branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Development Guidelines
- Use Django's built-in features when possible
- Follow the DRY principle
- Write docstrings for functions and classes
- Keep views focused and models comprehensive
- Use Django ORM instead of raw SQL queries

---

## 🐛 Troubleshooting

### Common Issues

**Static files not loading:**
```bash
python manage.py collectstatic --noinput
```

**Database migrations failing:**
```bash
python manage.py migrate --fake-initial
```

**Docker containers not starting:**
```bash
docker-compose logs
docker-compose down -v  # Remove volumes
docker-compose up -d --build
```

**Permission errors:**
```bash
# Check file permissions
ls -la db.sqlite3
# Ensure proper ownership
```

---

## 📚 Documentation

- [DOCKER.md](DOCKER.md) - Complete Docker deployment guide
- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 🗺️ Roadmap

### Planned Features
- [ ] REST API with Django REST Framework
- [ ] Task categories and tags
- [ ] Email notifications for due tasks
- [ ] Task sharing between users
- [ ] File attachments
- [ ] Advanced search and filtering
- [ ] Calendar view
- [ ] Mobile application
- [ ] Two-factor authentication
- [ ] Activity logs and audit trails

### Performance Improvements
- [ ] Redis caching layer
- [ ] PostgreSQL full-text search
- [ ] WebSocket support for real-time updates
- [ ] API rate limiting
- [ ] Database query optimization

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Ziad (BytePharaoh)**

- GitHub: [@bytepharaoh](https://github.com/bytepharaoh)
- Project: [Secure Task Manager](https://github.com/bytepharaoh/secure-task-manager)

---

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Containerized with [Docker](https://www.docker.com/)
- Inspired by modern task management applications
- Thanks to the Django and open-source communities

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/bytepharaoh/secure-task-manager/issues)
- **Discussions:** [GitHub Discussions](https://github.com/bytepharaoh/secure-task-manager/discussions)
- **Security:** Report security vulnerabilities privately via GitHub Security Advisories

---

**⭐ If you find this project helpful, please give it a star on GitHub! ⭐**

---

**Built with ❤️ using Django 6.0.2 and Python 3.12**
