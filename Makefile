APP_DIR?=app
ROOT_TESTS_DIR?=tests
SCRIPTS_DIR?=scripts
ENV?="$$(dotenv get ENV)"
MAKE_ARGS?=--no-print-directory
API_PATH := ${APP_DIR}/
API_MODULE_MAIN := ${APP_DIR}.api_main
HOST?=0.0.0.0
PORT?=8000
INIT?=uvicorn ${API_MODULE_MAIN}:app --host $(HOST) --port $(PORT)
DOCKER_IMAGE_NAME=pc/identidade
DOCKERFILE_PATH=./devtools/docker/Dockerfile
CONTAINER_NAME?=pc-identidade

clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.log" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f .coverage.NB-SBDEV*
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log
	@rm -f .env.bkp*

build-venv:
	python3.12 -m venv venv
	source ./venv/bin/activate

requirements-dev:
	python3.12 -m pip install --upgrade pip
	python3.12 -m pip install --upgrade pip wheel setuptools
	@pip install -r requirements/develop.txt

docker-build:
	docker-compose up --build -d

auth-build-configuration:
	python devtools/keycloak-config/setup_sellers_attribute.py

lint:
	isort ${APP_DIR} ${ROOT_TESTS_DIR}
	bandit -c pyproject.toml -r -f custom ${APP_DIR} ${ROOT_TESTS_DIR}
	black ${APP_DIR} ${ROOT_TESTS_DIR}
	flake8 --max-line-length=120 ${APP_DIR} ${ROOT_TESTS_DIR}

check-lint:
	isort -c ${APP_DIR} ${ROOT_TESTS_DIR}
	bandit -c pyproject.toml -r -f custom ${APP_DIR} ${ROOT_TESTS_DIR}
	black --check ${APP_DIR} ${ROOT_TESTS_DIR}
	flake8 --max-line-length=120 ${APP_DIR} ${ROOT_TESTS_DIR}
	mypy ${APP_DIR} ${SCRIPTS_DIR} ${MIGRATIONS_DIR} ${ROOT_TESTS_DIR}

safety:
	@pip-audit -r requirements/base.txt

dead-fixtures:
ifeq ($(OS),Windows_NT)
	@cmd /C "set ENV=$(ENV)&& pytest --dead-fixtures"
else
	@ENV=$(ENV) pytest --dead-fixtures
endif

test:
ifeq ($(OS),Windows_NT)
	@cmd /C "set ENV=test&& pytest ${ROOT_TESTS_DIR}/"
else
	@ENV=test pytest ${ROOT_TESTS_DIR}/
endif

.PHONY: build test run
build: check-lint test


pop-env:
	@./devtools/scripts/pop-env

load-env:
	@./devtools/scripts/push-env "devtools/dotenv.$(env)"

load-dev-env:
ifeq ($(OS),Windows_NT)
	@cmd /C "set env=dev&& make $(MAKE_ARGS) load-env"
else
	@env=dev make $(MAKE_ARGS) load-env
endif

load-test-env:
ifeq ($(OS),Windows_NT)
	@cmd /C "set env=test&& make $(MAKE_ARGS) load-env"
else
	@env=test make $(MAKE_ARGS) load-env
endif

.PHONY: run
run:
	$(INIT)

run-dev:
ifeq ($(OS),Windows_NT)
	@cmd /C "set ENV=dev&& $(INIT) --reload"
else
	@ENV=dev $(INIT) --reload
endif


docker-run:
	docker run --rm --name $(CONTAINER_NAME) -e ENV=dev -p 8000:8000 $(DOCKER_IMAGE_NAME)

docker-shell:
	docker run --rm -it --name $(CONTAINER_NAME) -e ENV=dev $(DOCKER_IMAGE_NAME) /bin/bash

docker-compose-sonar-up:
	docker compose -f ./devtools/docker/docker-compose-sonar.yml up -d

docker-compose-sonar-down:
	docker compose -f ./devtools/docker/docker-compose-sonar.yml down

migration-create:
ifndef NOME
	$(error NOME é obrigatório. Use: make migration-create NOME="nome da migration")
endif
	@powershell -Command ".\venv\Scripts\mongodb-migrate-create.exe --description '$(NOME)'"

migration-run:
	@echo "Executando migrations..."
	@python3.12 run_migrations.py