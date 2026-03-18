# ---- Config ----
VENV        := .venv
PYTHON      := $(VENV)/bin/python
PIP         := $(VENV)/bin/pip
FLASK       := $(VENV)/bin/flask
PYTEST      := $(VENV)/bin/pytest
version	 	:= latest
POSTGRES_PASSWORD := abc123

help:
	@echo "Available targets:"
	@echo "  all         - Default target (alias for 'setup')"
	@echo "  setup       - Set up the virtual environment and install dependencies"
	@echo "  db_create   - Create or upgrade the database schema"
	@echo "  db_reset    - Drop and recreate the database (use with caution)"
	@echo "  run         - Run the Flask application"
	@echo "  dev         - Run the Flask application in development mode with debug enabled"
	@echo "  test        - Run tests using pytest"
	@echo "  lint        - Run code linting using ruff (optional)"
	@echo "  clean       - Remove virtual environment and instance folder"
	@echo "  distclean   - Remove virtual environment, instance folder, and migrations"
	@echo "  build       - Build the Docker image for the application"

# ---- Default ----
.PHONY: all
all: setup

# ---- Setup / env ----
$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@touch $@

.PHONY: setup
setup: $(VENV)/bin/activate

# ---- DB ----
.PHONY: db_create
db_create: setup
	$(FLASK) db upgrade

.PHONY: db_reset
db_reset: setup
	@echo "Dropping and recreating database (use with caution)"
	rm -rf instance/
	$(FLASK) db upgrade

# ---- Tests ----
.PHONY: test
test: setup
	$(PYTEST)

# ---- Lint (optional) ----
.PHONY: lint
lint: setup
	$(VENV)/bin/ruff check .

# ---- Clean ----
.PHONY: clean
clean:
	rm -rf $(VENV)/
	rm -rf instance/

.PHONY: distclean
distclean: clean
	rm -rf migrations/


#----Docker----
.PHONY: build
build:
	docker build -t student-app:${version} .

.PHONY: push
push: build
	docker tag student-app:${version} acidcow/student-app:${version}
	docker push acidcow/student-app:${version}

.PHONY: run
run:
	docker compose -f compose.yaml up -d --build

.PHONY: stop
stop:
	docker compose -f compose.yaml down