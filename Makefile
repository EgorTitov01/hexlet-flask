PORT ?= 8000

dev:
	poetry run flask --app users_example.app --debug run --port $(PORT)
build:
	./build.sh
prod:
	poetry run gunicorn --workers=4 --bind=0.0.0.0:$(PORT) users_example.app:app
render:
	poetry install
	poetry build