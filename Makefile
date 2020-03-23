DOCKER_CMD=docker exec -it djangolifebartenders


setup:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

start:
	python manage.py runserver

