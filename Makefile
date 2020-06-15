DOCKER_CMD=docker exec -it lifebartenders

_upgrade-pip:
	${DOCKER_CMD} pip install --upgrade pip

build:
	docker-compose up -d

setup: _upgrade-pip
	${DOCKER_CMD} pip install -r requirements.txt

migrate:
	${DOCKER_CMD} python manage.py migrate

start:
	${DOCKER_CMD} gunicorn lifebartenders.wsgi:application --bind 0.0.0.0:8000 --workers 3
# 	${DOCKER_CMD} python manage.py runserver
# 	docker run -it lifebartenders

