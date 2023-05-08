# Simple makefile to easily work with a local deployment via Docker compose

# Regular targets
# --
build:
	docker compose build

build-no-cache:
	docker compose build --no-cache

run:
	docker compose build
	docker compose up
	docker compose down

# Development targets
# --
dev-build:
	docker compose -f dev.docker-compose.yaml build

dev-build-no-cache:
	docker compose -f dev.docker-compose.yaml build --no-cache

dev-run:
	docker compose -f dev.docker-compose.yaml build
	docker compose -f dev.docker-compose.yaml up
	docker compose -f dev.docker-compose.yaml down

# Helper targets
# --
logs:
	docker compose logs
