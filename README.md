 Bookshelf API
 
REST API for managing authors and books, built with Flask, SQLAlchemy 2.0 and PostgreSQL using a layered, object-oriented architecture.
 
## Stack
 
| Layer | Choice |
| --- | --- |
| Language | Python 3.12+ |
| Web framework | Flask 3 |
| ORM | SQLAlchemy 2.0 via Flask-SQLAlchemy |
| Database | PostgreSQL 16 (Docker) |
| DB driver | psycopg 3 |
| Migrations | Flask-Migrate (Alembic) |
| Validation | Pydantic 2 |
| Tests | pytest |
 
## Architecture
 
Requests flow down through four layers; imports only flow in the same direction.
 
```text
api (blueprints) → services → repositories → models → extensions
```
 
| Layer | Responsibility |
| --- | --- |
| `api/` | Parse HTTP, validate input with Pydantic, call one service method, serialize output |
| `services/` | Business rules, orchestration, transaction boundary (`commit`) |
| `repositories/` | Queries only, no business rules, no commits |
| `models/` | ORM entities and single-entity invariants |
| `schemas/` | Pydantic request/response DTOs |
| `errors.py` | Domain exception hierarchy and JSON error handlers |
 
## Project structure
 
```text
.
├── bookshelf/
│   ├── __init__.py          # create_app() factory
│   ├── config.py            # config classes per environment
│   ├── extensions.py        # db, migrate
│   ├── errors.py
│   ├── api/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   └── services/
├── migrations/
├── tests/
├── docker-compose.yml
├── requirements.txt
└── .env.example
```
 
## Getting started
 
### Prerequisites
 
- Python 3.12+
- Docker and Docker Compose
### 1. Clone and create a virtual environment
 
```bash
git clone <repo-url> bookshelf
cd bookshelf
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```
 
### 2. Configure environment
 
```bash
cp .env.example .env
```
 
| Variable | Example | Purpose |
| --- | --- | --- |
| `FLASK_APP` | `bookshelf:create_app` | App factory used by the Flask CLI |
| `FLASK_RUN_PORT` | `5001` | Port for `flask run` (5000 is taken by AirPlay on macOS) |
| `APP_ENV` | `development` | `development`, `testing` or `production` |
| `DATABASE_URL` | `postgresql+psycopg://bookshelf:bookshelf@localhost:5432/bookshelf` | Main database |
| `TEST_DATABASE_URL` | `postgresql+psycopg://bookshelf:bookshelf@localhost:5433/bookshelf_test` | Test database |
| `SECRET_KEY` | `change-me` | Flask secret key |
 
### 3. Start PostgreSQL
 
```bash
docker compose up -d
```
 
This starts two containers: `db` on port 5432 and `db_test` on port 5433.
 
### 4. Apply migrations
 
```bash
flask db upgrade
```
 
### 5. Run the API
 
```bash
flask run --debug
curl http://127.0.0.1:5001/health
# {"status": "ok"}
```
 
All commands (`flask`, `pytest`, `docker compose`) run from the repository root.
 
## API
 
| Method | Path | Body | Success |
| --- | --- | --- | --- |
| GET | `/health` | none | 200 |
| GET | `/api/books?page=1&per_page=20` | none | 200, paged list |
| GET | `/api/books/<id>` | none | 200 |
| POST | `/api/books` | `BookCreate` | 201 + `Location` header |
| PATCH | `/api/books/<id>` | `BookUpdate` (partial) | 200 |
| DELETE | `/api/books/<id>` | none | 204 |
| POST | `/api/books/<id>/discount` | `{"percent": 10}` | 200 |
| GET | `/api/authors/<id>` | none | 200, includes books |
| POST | `/api/authors` | `AuthorCreate` | 201 |
| DELETE | `/api/authors/<id>` | none | 204, cascades to books |
 
### Example
 
```bash
curl -X POST http://127.0.0.1:5001/api/authors \
  -H "Content-Type: application/json" \
  -d '{"name": "Clarice Lispector", "email": "clarice@example.com"}'
 
curl -X POST http://127.0.0.1:5001/api/books \
  -H "Content-Type: application/json" \
  -d '{"title": "A Hora da Estrela", "isbn": "978-85-325-0812-3", "price": "39.90", "author_id": 1}'
```
 
Monetary values are returned as strings (`"39.90"`) to avoid float rounding.
 
### Error format
 
Every error uses the same shape:
 
```json
{
  "error": {
    "code": "validation_error",
    "message": "Request body is invalid",
    "details": [{"field": "price", "message": "Input should be greater than or equal to 0"}]
  }
}
```
 
| Status | `code` | When |
| --- | --- | --- |
| 400 | `validation_error` | Request body fails schema validation |
| 404 | `not_found` | Resource does not exist |
| 409 | `conflict` | Duplicate ISBN or email |
| 422 | `business_rule_violation` | Domain rule rejected the operation |
| 500 | `internal_error` | Unexpected error (details hidden) |
 
## Database migrations
 
```bash
flask db migrate -m "describe the change"   # generate a revision from model changes
flask db upgrade                            # apply pending revisions
flask db downgrade                          # revert the last revision
flask db current                            # show current revision
```
 
Always review generated revisions before applying them. Never edit a revision that has already run in a shared environment.
 
## Tests
 
```bash
docker compose up -d db_test
pytest -q
pytest --cov=bookshelf --cov-report=term-missing   # requires pytest-cov
```
 
- **Unit tests** use fake repositories injected into services; no database needed for the logic itself.
- **API tests** run against the `bookshelf_test` database; tables are truncated after each test.
## Troubleshooting
 
| Symptom | Cause | Fix |
| --- | --- | --- |
| `TypeError: unsupported operand type(s) for \|` | Python older than 3.10 | Recreate `.venv` with Python 3.12 |
| `externally-managed-environment` on `pip install` | venv not active, system pip used | `source .venv/bin/activate`, then `python -m pip install ...` |
| `Could not import 'bookshelf.bookshelf'` | `__init__.py` in the repository root | Delete it; only the inner `bookshelf/` package has one |
| 403 on port 5000 (macOS) | AirPlay Receiver owns port 5000 | Use `FLASK_RUN_PORT=5001` |
| `No changes in schema detected` | Tables already exist or models not imported | Check `\dt` in psql and `db.metadata.tables` in `flask shell` |
 
## References
 
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy 2.0 ORM](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [pytest](https://docs.pytest.org/en/stable/)