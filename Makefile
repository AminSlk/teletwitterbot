.PHONY: venv pre-commit fmt lint run clean docke-build
DOCKER_IMAGE ?= teletwitterbot 

venv:
	pipenv install

pre-commit:
	pre-commit install

fmt:
	yapf --in-place **/*.py
	isort .
	autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .

lint:
	pylint ./teletwitterbot --disable=C0114,C0115,C0116

run:
	python -m teletwitterbot

clean:
	rm -f database.db

docker-build: clean 
	docker build -t ${DOCKER_IMAGE} . 
