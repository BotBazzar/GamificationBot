run:
	docker compose up --no-deps --build
start:
	docker compose up
build:
	docker compose up -d --no-deps --build
frontend:
	docker compose up -d --no-deps --build frontend
nginx:
	docker compose up -d --no-deps --build nginx
stop:
	docker compose stop
clean:
	docker compose down -v --rmi local --remove-orphans
