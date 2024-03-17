.phony: run serve build logs stop restart migration migrate

run:
	docker compose up

serve:
	docker compose up -d

build:
	docker compose build

logs:
	docker compose logs -f

stop:
	docker compose stop

restart:
	docker compose restart

migration:
	docker compose run app sh -c 'poetry run python manage.py makemigration'

migrate:
	docker compose run app sh -c 'poetry run python manage.py migrate'
