default: fmt lint

# Code Formatting & Linting
fmt:
	ruff format

lint:
	ruff check

fix:
	ruff check --fix

# Start Bot
start:
	python -m bot.main
