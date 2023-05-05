# Simple makefile to easily work with a local deployment via Docker compose
# Note that due to Docker's nature, you need to run all make commands as a superuser

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

# Helper targets
# --
logs:
	docker compose logs
