SHELL := /bin/bash

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f | cat

ps:
	docker compose ps

restart: down up


