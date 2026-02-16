# Docker Deployment Guide

Complete guide for deploying the Secure Task Manager using Docker and Docker Compose.

---

## 📦 What's Included

- **Dockerfile** - Multi-stage Python application container
- **docker-compose.yml** - Full stack orchestration (Django + PostgreSQL + Nginx)
- **nginx.conf** - Production-ready Nginx configuration
- **.dockerignore** - Optimized build context
- **.env.docker** - Environment template

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+

### Deploy with One Command

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/secure-task-manager.git
cd secure-task-manager

# 2. Setup environment
cp .env.docker .env
# Edit .env and change SECRET_KEY and passwords

# 3. Start everything
docker-compose up -d

# 4. Create superuser
docker-compose exec web python manage.py createsuperuser

# 5. Access application
# Open http://localhost
```

**That's it!** Your app is running with PostgreSQL and Nginx! 🎉

---

## 🏗️ Architecture

### Container Structure

```
┌─────────────────────────────────────────┐
│  Nginx (Port 80)                        │
│  - Reverse proxy                        │
│  - Static file serving                  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Django + Gunicorn (Port 8000)          │
│  - Application server                   │
│  - Business logic                       │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  PostgreSQL (Port 5432)                 │
│  - Database                             │
│  - Persistent storage                   │
└─────────────────────────────────────────┘
```

### Volumes
- `postgres_data` - Database persistence
- `static_volume` - Shared static files between Django and Nginx

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Generate secure SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Required variables
SECRET_KEY=<generated-key>
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DATABASE_URL=postgresql://django:secure_password@db:5432/taskmanager
```

### Database Configuration

Default PostgreSQL settings in `docker-compose.yml`:
```yaml
POSTGRES_DB=taskmanager
POSTGRES_USER=django
POSTGRES_PASSWORD=secure_password_change_this  # CHANGE THIS!
```

**⚠️ Security:** Always change default passwords in production!

---

## 📋 Docker Commands Reference

### Basic Operations

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web

# Restart a service
docker-compose restart web
```

### Django Management

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Django shell
docker-compose exec web python manage.py shell

# Database shell
docker-compose exec db psql -U django -d taskmanager
```

### Maintenance

```bash
# View running containers
docker-compose ps

# Check resource usage
docker stats

# Remove stopped containers
docker-compose rm

# Rebuild after code changes
docker-compose up -d --build

# View container details
docker-compose exec web env
```

---

## 🔄 Deployment Workflow

### Development

```bash
# Start with live code reloading
docker-compose -f docker-compose.dev.yml up

# Run tests
docker-compose exec web python manage.py test

# Check code
docker-compose exec web python manage.py check
```

### Production Deployment

```bash
# 1. Pull latest code
git pull origin main

# 2. Rebuild containers
docker-compose build

# 3. Run migrations
docker-compose run --rm web python manage.py migrate

# 4. Restart services
docker-compose up -d

# 5. Verify
docker-compose ps
curl http://localhost
```

---

## 🗄️ Database Management

### Backup Database

```bash
# Create backup
docker-compose exec db pg_dump -U django taskmanager > backup_$(date +%Y%m%d).sql

# With compression
docker-compose exec db pg_dump -U django taskmanager | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Restore Database

```bash
# From backup file
cat backup.sql | docker-compose exec -T db psql -U django taskmanager

# From compressed backup
gunzip -c backup.sql.gz | docker-compose exec -T db psql -U django taskmanager
```

### Reset Database

```bash
# WARNING: This deletes all data!
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 🐛 Troubleshooting

### Database Connection Issues

**Problem:** `django.db.utils.OperationalError: could not connect to server`

**Solution:**
```bash
# Check database is running
docker-compose ps db

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db

# Wait for database to be ready
docker-compose exec web python manage.py check --database default
```

### Static Files Not Loading

**Problem:** CSS/JS not loading

**Solution:**
```bash
# Recollect static files
docker-compose exec web python manage.py collectstatic --noinput

# Restart nginx
docker-compose restart nginx

# Check nginx logs
docker-compose logs nginx
```

### Permission Errors

**Problem:** `PermissionError: [Errno 13] Permission denied`

**Solution:**
```bash
# Fix ownership
docker-compose exec web chown -R django:django /app

# Rebuild with correct user
docker-compose build --no-cache
```

### Port Already in Use

**Problem:** `Error starting userland proxy: listen tcp 0.0.0.0:80: bind: address already in use`

**Solution:**
```bash
# Find what's using the port
sudo lsof -i :80

# Stop conflicting service
sudo systemctl stop nginx  # or apache2

# Or change port in docker-compose.yml
ports:
  - "8080:80"  # Use port 8080 instead
```

---

## 🔒 Production Security

### SSL/TLS Configuration

**Option 1: Let's Encrypt with Certbot**

```yaml
# docker-compose.yml - add certbot service
certbot:
  image: certbot/certbot
  volumes:
    - ./certbot/conf:/etc/letsencrypt
    - ./certbot/www:/var/www/certbot
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

Update `nginx.conf` for HTTPS (see nginx-ssl.conf example)

**Option 2: Reverse Proxy (Traefik/Caddy)**

Use Traefik or Caddy for automatic SSL management.

### Security Checklist

- [ ] Change all default passwords
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Enable SSL/TLS
- [ ] Set `ALLOWED_HOSTS` correctly
- [ ] Use environment variables for secrets
- [ ] Enable firewall rules
- [ ] Regular security updates
- [ ] Database backups automated
- [ ] Monitor logs regularly

---

## 📊 Monitoring & Logging

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service with timestamps
docker-compose logs -f --timestamps web

# Last 100 lines
docker-compose logs --tail=100 web
```

### Log to File

```bash
# Export logs
docker-compose logs > logs_$(date +%Y%m%d).txt

# Continuous logging to file
docker-compose logs -f >> production.log &
```

### Health Checks

```bash
# Check container health
docker-compose ps

# Inspect health status
docker inspect --format='{{.State.Health.Status}}' secure-task-manager_web_1

# Test endpoints
curl http://localhost/
curl -I http://localhost/admin/
```

---

## 🚀 Scaling

### Horizontal Scaling

```bash
# Scale web service to 3 instances
docker-compose up -d --scale web=3

# Load balancer will be needed (Nginx, HAProxy, Traefik)
```

### Resource Limits

Add to `docker-compose.yml`:

```yaml
web:
  deploy:
    resources:
      limits:
        cpus: '1'
        memory: 512M
      reservations:
        cpus: '0.5'
        memory: 256M
```

---

## 📈 Performance Optimization

### Docker Image Size

```bash
# Check image size
docker images secure-task-manager_web

# Optimize by:
# - Using alpine base images
# - Multi-stage builds
# - Removing unnecessary dependencies
# - Combining RUN commands
```

### Build Cache

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker-compose build

# Clear build cache
docker builder prune
```

---

## 🌐 Cloud Deployment

### AWS ECS

```bash
# 1. Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker tag secure-task-manager:latest <account>.dkr.ecr.<region>.amazonaws.com/secure-task-manager:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/secure-task-manager:latest

# 2. Create ECS task definition
# 3. Deploy to ECS service
```

### DigitalOcean App Platform

```bash
# Use docker-compose.yml directly
# App Platform supports Docker Compose
```

### Railway / Render

```bash
# Both support Dockerfile deployment
# Connect GitHub repository
# Auto-deploy on push
```

---

## 🧪 Testing in Docker

### Run Tests

```bash
# Unit tests
docker-compose exec web python manage.py test

# With coverage
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report

# Specific test
docker-compose exec web python manage.py test tasks.tests.TestTaskModel
```

### Integration Testing

```bash
# Create test database
docker-compose exec web python manage.py test --keepdb

# Load fixtures
docker-compose exec web python manage.py loaddata fixtures/test_data.json
```

---

## 📦 CI/CD Integration

### GitHub Actions Example

```yaml
name: Docker Build & Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker-compose build
      - name: Run tests
        run: docker-compose run web python manage.py test
      - name: Tear down
        run: docker-compose down
```

---

## 🔄 Migration from Traditional Deployment

### Export SQLite Data

```bash
# On old server
python manage.py dumpdata > datadump.json

# Transfer to Docker
docker cp datadump.json secure-task-manager_web_1:/app/

# Load in Docker
docker-compose exec web python manage.py loaddata datadump.json
```

### Migrate to PostgreSQL

```bash
# 1. Dump from SQLite
python manage.py dumpdata --natural-foreign --natural-primary > data.json

# 2. Switch to PostgreSQL in settings
# 3. Run migrations
docker-compose exec web python manage.py migrate

# 4. Load data
docker-compose exec web python manage.py loaddata data.json
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [PostgreSQL in Docker](https://hub.docker.com/_/postgres)
- [Nginx in Docker](https://hub.docker.com/_/nginx)

---

## ✅ Benefits of Docker Deployment

### For Development
- ✅ Consistent environment across team
- ✅ No "works on my machine" issues
- ✅ Easy to onboard new developers
- ✅ Isolated dependencies

### For Production
- ✅ Easy deployment
- ✅ Scalability
- ✅ Rollback capability
- ✅ Resource efficiency
- ✅ Platform independent

### For Operations
- ✅ Simplified updates
- ✅ Health monitoring
- ✅ Easy backups
- ✅ Predictable behavior

---

**🎉 Your Django app is now production-ready with Docker!**
