.PHONY: build up down shell test lint

build:
	docker compose build

up:
	docker compose up --build

down:
	docker compose down

shell:
	docker compose exec api /bin/bash

test:
	# placeholder for test runner
	echo "Run tests in backend and frontend"

lint:
	# placeholder for linters
	echo "Run linting"
