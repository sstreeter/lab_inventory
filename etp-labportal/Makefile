# Makefile

ENV_FILE ?= .env.dev

run:
	@echo "Using $(ENV_FILE)"
	cp $(ENV_FILE) .env
	docker-compose up -d --build

prod:
	$(MAKE) run ENV_FILE=.env.prod

dev:
	$(MAKE) run ENV_FILE=.env.dev

down:
	docker-compose down
