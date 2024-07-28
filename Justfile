default: fmt lint

# Code Formatting & Linting
fmt:
	ruff format

lint:
	ruff check

fix:
	ruff check --fix

# Start Bot & Containers
start:
	python -m bot.main

up:
	docker compose -f docker-compose-local.yml up -d

# Migrations Management
revise msg:
    alembic revision --autogenerate -m "{{msg}}"

migrate target="head":
    alembic upgrade {{target}}

revert target="-1":
    alembic downgrade {{target}}
