dev:
	poetry run flask --app users_example.app --debug run --port 8000
build:
	./build.sh
prod:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:8000 users_example.app:app
render:
	poetry install
	poetry build