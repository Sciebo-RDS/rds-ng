# Simple makefile to easily work with a local deployment via Docker compose

# Regular targets
# --
build:
	docker compose down
	docker compose build

fresh-build:
	docker compose down
	docker compose build --no-cache

run:
	docker compose up -d

stop:
	docker compose down

go:
	docker compose down
	docker compose build
	docker compose up

# Development targets
# --
dev-build:
	docker compose -f dev.docker-compose.yaml down
	docker compose -f dev.docker-compose.yaml build

dev-fresh-build:
	docker compose -f dev.docker-compose.yaml down
	docker compose -f dev.docker-compose.yaml build --no-cache

dev-run:
	docker compose -f dev.docker-compose.yaml up -d

dev-stop:
	docker compose -f dev.docker-compose.yaml down

dev-go:
	docker compose -f dev.docker-compose.yaml down
	docker compose -f dev.docker-compose.yaml build
	docker compose -f dev.docker-compose.yaml up

# Helper targets
# --
logs:
	docker compose logs
