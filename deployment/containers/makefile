# Simple makefile to easily work with a local deployment via Docker compose

# Regular targets
# --
build:
	docker compose -p rds build

build-no-cache:
	docker compose -p rds build --no-cache

run:
	docker compose -p rds build
	docker compose -p rds up
	docker compose -p rds down

# Development targets
# --
dev-build:
	docker compose -p rds -f dev.docker-compose.yaml build

dev-build-no-cache:
	docker compose -p rds -f dev.docker-compose.yaml build --no-cache

dev-run:
	docker compose -p rds -f dev.docker-compose.yaml build
	docker compose -p rds -f dev.docker-compose.yaml up
	docker compose -p rds -f dev.docker-compose.yaml down

# Helper targets
# --
logs:
	docker compose -p rds logs
