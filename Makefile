DOCKER_CMD=docker exec -it djangolifebartenders

# _config-env:
# 	[ -f .env ] || cp .env.sample .env

build: # _config-env
	docker-compose up -d

stop:
	docker-compose stop

upgrade-pip:
	${DOCKER_CMD} pip install --upgrade pip

setup:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

start:
	python manage.py runserver

