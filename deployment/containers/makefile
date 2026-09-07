# Simple makefile to build Docker images for local deployments

.DEFAULT_GOAL := run

# Regular targets
# --
build:
	docker compose -p rds build

build-no-cache:
	docker compose -p rds build --no-cache

# Development targets
# --
dev-build:
	docker compose -p rds -f dev.docker-compose.yaml build

dev-build-no-cache:
	docker compose -p rds -f dev.docker-compose.yaml build --no-cache
