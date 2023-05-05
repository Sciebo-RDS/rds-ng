# Simple makefile to easily work with a local deployment via Docker compose
# Note that due to Docker's nature, you need to run all make commands as a superuser
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
