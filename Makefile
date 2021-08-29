build:
	docker-compose build app

test:
	docker-compose run --rm --no-deps app pytest

run:
	docker-compose run --rm app
