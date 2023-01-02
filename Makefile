build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

up-prod: down
	docker-compose up backend -d
