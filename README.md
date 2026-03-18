# One2N SRE Bootcamp - Student App

This repository is a simple Flask + SQLAlchemy student management API used for the [One2N SRE Bootcamp](https://one2n.io/sre-bootcamp/sre-bootcamp-exercises).

It provides:

- A REST API to create/read/update/delete students
- SQLAlchemy models and Flask-Migrate/Alembic migrations
- Logging of requests/responses/exceptions to `logs/app.log`
- A healthcheck endpoint for service monitoring

---

## 📦 Prerequisites

### Recommended
- macOS / Linux
- Python 3.12 (system or via `pyenv` / `asdf`)
- GNU Make
- Docker


---

## 🧰 Local Development (Makefile)

This repo ships a `Makefile` that manages the virtual environment, dependencies, migrations, running the app, and tests.

### Setup (one-time)

```bash
make setup
```

This will:
- Create a Python virtual environment in `.venv`
- Install dependencies from `requirements.txt`

### Run the app

Start the app (ensures migrations are applied first):

```bash
make run
```

Run in development mode (hot reload + debug logging):

```bash
make dev
```

Then open: `http://localhost:8080`

### Database (migrations)

Apply migrations (create/update the database schema):

```bash
make db_create
```

Reset the database (DANGEROUS: drops `instance/`):

```bash
make db_reset
```

### Tests

Run unit tests with pytest:

```bash
make test
```

### Lint

Run Ruff linter:

```bash
make lint
```

### Cleaning up

Remove the virtual environment and database files:

```bash
make clean
```

Remove migrations as well:

```bash
make distclean
```

---

## 🧠 How Configuration Works

The app loads config from .env files using the `settings.py`. It supports using `SQLALCHEMY_DATABASE_URI` to point at the database.

Example (for local SQLite):

```env
SQLALCHEMY_DATABASE_URI=sqlite:///instance/student.db
```

> ✅ In Docker / Docker Compose, we use PostgreSQL and set `SQLALCHEMY_DATABASE_URI` via environment variables.

---

## 🚀 Docker

### Build the image

From the repo root:

```bash
docker build -t student-app:1.0 .
```

### Run the container

```bash
docker run -p 8080:8080 student-app:1.0
```

Then open: `http://localhost:8080/api/v1/healthcheck`

---

## 🧩 Docker Compose (Postgres + App)

A `compose.yaml` is included to run the app with PostgreSQL.

Start the stack:

```bash
make run
```

Or directly:

```bash
docker compose up --build
```

The app will be available at `http://localhost:8080`.

Stop the stack:

```bash
make stop
```

Or directly:

```bash
docker compose down
```

---

## 🧪 API Endpoints

| Method | Path | Description |
|------|------|-------------|
| GET | `/api/v1/healthcheck` | Health check (DB connectivity) |
| GET | `/api/v1/students` | List all students |
| POST | `/api/v1/students` | Create a new student |
| GET | `/api/v1/students/<id>` | Get a student by ID |
| PUT | `/api/v1/students/<id>` | Update a student |
| DELETE | `/api/v1/students/<id>` | Delete a student |

Example request (create a student):

```bash
curl -X POST http://localhost:8080/api/v1/students \
  -H 'Content-Type: application/json' \
  -d '{"first_name": "Jane", "last_name": "Doe", "age": 15, "grade": "10"}'
```

---

## 🧾 Logs

Logs are written to `logs/app.log` by default.

If you run via Docker and want to persist logs outside the container, mount the `logs/` directory as a volume:

```bash
docker run -v $(pwd)/logs:/app/student-app/logs -p 8080:8080 student-app:1.0
```

---

## 🧩 Notes

- The repository uses SQLite by default (in `instance/`) but can be configured to use PostgreSQL.
- Migrations are managed by Flask-Migrate (Alembic) and are stored under `migrations/`.

---

Happy hacking! 🎉
