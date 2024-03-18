.phony: run serve build logs stop restart migrations migrate repl

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

migrations:
	docker compose exec app sh -c 'poetry run python manage.py makemigrations'

migrate:
	docker compose exec app sh -c 'poetry run python manage.py migrate'

repl:
	docker compose exec -it app sh -c 'poetry run python manage.py shell'

ready:
	poetry run python manage.py check --deploy --settings="core.settings.prod"
