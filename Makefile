.PHONY: build up down logs migrate seed user shell

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose run --rm backend-django python manage.py makemigrations
	docker compose run --rm backend-django python manage.py migrate

seed:
	docker compose run --rm backend-django python manage.py seed_data

user:
	docker compose run --rm backend-django python manage.py createsuperuser

shell:
	docker compose run --rm backend-django python manage.py shell

test:
	docker compose run --rm backend-django pytest
	docker compose run --rm backend-fastapi pytest
