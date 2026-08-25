# Simple makefile to easily work with a local deployment via Docker compose

.DEFAULT_TARGET := run

GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

run: build start

build:
	@echo "Building RDS NG..."
	cd ./deployment/containers && make dev-build

	@echo "Building RDS NG Integration App..."
	cd ../rds-ng-nextcloud && make build

start:
	RDS_NG_BRANCH_NAME=$(GIT_BRANCH) docker compose -f ./local/docker-compose.yml up --no-attach nextcloud --no-attach proxy
	RDS_NG_BRANCH_NAME=$(GIT_BRANCH) docker compose -f ./local/docker-compose.yml down

.PHONY: build start run
