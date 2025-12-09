# Dev shortcuts (build, run, lint, migrate, etc.)
.PHONY: help build run lint migrate test seed reset

help:
	@echo "Available commands:"
	@echo "  make build   - Build Docker containers"
	@echo "  make run     - Start all services"
	@echo "  make lint    - Run code linting"
	@echo "  make migrate - Run database migrations"
	@echo "  make test    - Run tests"
	@echo "  make seed    - Seed database with dev data"
	@echo "  make reset   - Reset database"

build:
	docker-compose build

run:
	docker-compose up

lint:
	python -m flake8 app/
	python -m black --check app/

migrate:
	python scripts/run_migrations.py

test:
	pytest app/tests/

seed:
	python scripts/seed_dev_data.py

reset:
	python scripts/reset_db.py
