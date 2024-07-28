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
