# Local Smart Hotel Management

A production-quality, dockerized Hotel Management system implementing a hybrid **Django + FastAPI** architecture with **React** frontend.

## Architecture

- **Django (Core)**: Handles business logic, Admin UI, Database Migrations, and Celery Tasks.
  - *Tech*: Django 5.2.x, Python 3.12-alpine.
- **FastAPI (API)**: High-performance public API reading from the same DB. integrates with Django Sessions.
  - *Tech*: FastAPI, SQLAlchemy, Python 3.12-alpine.
- **PostgreSQL**: Single Service of Truth for data.
- **Redis**: Broker for Celery and result backend.
- **React (Frontend)**: Vite + Tailwind CSS SPA.
- **Nginx**: Reverse proxy to serve Frontend and route `/api/` and `/admin/` requests.

## Setup Instructions

### Prerequisites
- Docker & Docker Compose
- Make (optional, for convenience scripts)

### Quick Start

1. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

2. **Build & Run**
   ```bash
   make build
   make up
   ```

3. **Initialize Database**
   ```bash
   make migrate
   ```

4. **Seed Data** (Optional)
   Creates 10 rooms, 5 guests, amenities, and sample bookings.
   ```bash
   make seed
   ```
   *Admin User*: `admin` / `adminpass`

### Access Points

- **Frontend**: [http://localhost](http://localhost)
- **FastAPI Docs**: [http://localhost/api/docs](http://localhost/api/docs)
- **Django Admin**: [http://localhost/admin/](http://localhost/admin/) (Login: admin/adminpass)

## Features

- **Role-Based Auth**: Superadmin, Manager, Receptionist, Guest.
- **Shared Session**: Log in via Django or Frontend; session is valid across both.
- **Room Management**: Admin can manage rooms/types/amenities.
- **Bookings**: Public API for creating bookings with overlap protection.
- **Billing**: Automatic Invoice generation.
- **PDF Generation**: Celery task generates PDFs using ReportLab.

## Technical Notes

- **Django Version**: Pinned to `Django==5.2.*` as requested.
- **Docker Images**: All Python services use `python:3.12-alpine` for minimal footprint.
- **Auth Strategy**: Shared Session via Cookie. FastAPI validates `sessionid` against `django_session` table in Postgres.

## Testing

Run tests via:
```bash
make test
```
