.PHONY: help clean

# Help system from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean: ## Removes all the compiled python files
	find . -name '*.py[co]' -delete

check-%:  ## Checks for a defined env variable
	@: $(if $(value $*),,$(error $* is undefined))

# Virtual environment 
.PHONY: virtualenv virtualenv-check

virtualenv-check:| check-VIRTUAL_ENV ## Check if the virtual env has been initialized else exit with error
	echo "VIRTUAL_ENV is $$VIRTUAL_ENV"

virtualenv: ## Set up a local 'venv' virtual env	
	python3.7 -m venv venv
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install -e .

virtualenv-upgrade:| virtualenv-check ## Upgrade dependencies to the latest compatible specified.
	pip install -U --upgrade-strategy eager -r requirements.txt

# DB
.PHONY: db-migrations db-autogenerate db-redo db-refresh-data

db-migrations:| virtualenv-check ## Apply the latest migrations to the DB.
	alembic upgrade heads
	python ./scripts/loads_data.py

db-autogenerate:| virtualenv-check ## Autogenerates the alembic migration based on the current state of the DB and the migrations.
	alembic revision --autogenerate -m "Add tables"

db-redo:| virtualenv-check ## Fast redo of the model to iterate fast
	alembic downgrade -1
	rm -r alembic/versions/*
	alembic revision --autogenerate -m "Add tables"
	alembic upgrade heads
	python ./scripts/loads_data.py

db-refresh-data:| virtualenv-check ## Refresh the data on the DB
	python ./scripts/cleans_data.py
	python ./scripts/loads_data.py

# Development
.PHONY: back-start front-start db-start

back-start:| virtualenv-check ## Start the flask web service
	python ./back/app.py

db-start: ## Start docker composer
	docker-compose up

front-start:  ## Start the development web server
	bash -c "pushd front; yarn; yarn serve; popd"
