# Simple makefile to easily work with a local deployment via Docker compose

.DEFAULT_TARGET := dev-run

GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
LOCAL_IP := $(firstword $(shell hostname -I))

dev-run: dev-build dev-start

dev-build:
	@echo "Building RDS NG (develop)..."
	cd ./deployment/containers && make dev-build

	@echo "Building RDS NG Integration App..."
	cd ../rds-ng-nextcloud && rm -rf build && make build

dev-start:
	RDS_NG_BRANCH_NAME=$(GIT_BRANCH) RDS_NG_LOCAL_IP=$(LOCAL_IP) \
 		docker compose -f ./deployment/local/dev.docker-compose.yml up --no-attach nextcloud --no-attach proxy

	RDS_NG_BRANCH_NAME=$(GIT_BRANCH) RDS_NG_LOCAL_IP=$(LOCAL_IP) \
		docker compose -f ./deployment/local/dev.docker-compose.yml down

.PHONY: dev-build dev-start dev-run
