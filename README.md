# Hotel Management System

## Quick Start

```bash
# Build and run all services
docker compose up --build -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## Services

| Service | URL | Description |
|---------|-----|-------------|
| Backend | http://localhost:8000 | Django + FastAPI |
| Frontend | http://localhost:5173 | React Vite |
| Database | localhost:5432 | PostgreSQL |
| Redis | localhost:6379 | Cache & Celery |

## Development

All services have live reloading enabled via volume mounts.
