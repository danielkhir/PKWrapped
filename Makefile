up:
	docker compose up -d
upb:
	docker compose up -d --build
down:
	docker compose down
build:
	docker compose build
build-scratch:
	docker compose build --no-cache
