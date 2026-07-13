# Clinical Trial Data Pipeline

An end-to-end ETL pipeline that retrieves clinical trial data from the ClinicalTrials.gov API v2, transforms it into a normalized relational model and loads it into PostgreSQL for analytical querying.

**Technology stack:** Python, pandas, PostgreSQL, SQLAlchemy, Docker and ClinicalTrials.gov API v2.

---

## Features

- ClinicalTrials.gov API integration
- Normalized relational database schema
- Dockerized PostgreSQL
- Automated ETL pipeline
- SQL analytical queries
- Unit tests

---

## Configuration

Before running the application, create the `.env` configuration file following the instructions in:

- **[Configuration Guide](docs/configuration.md)**

---

## Installation

It is recommended to use a dedicated Python virtual environment to isolate the project's dependencies.

### Windows

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Database

The project uses **PostgreSQL**, which is provided through Docker Compose.

Start the database:

```bash
docker compose up -d
```

Docker Compose starts a PostgreSQL instance using the configuration defined in the `.env` file.

The database schema is created automatically by the ETL application when `python main.py` is executed.

To stop the database:

```bash
docker compose down
```

To recreate the database from scratch:

```bash
docker compose down -v
docker compose up -d
```

---

## Architecture

```text
ClinicalTrials.gov API
          │
          ▼
       Extract
          │
          ▼
      Transform
          │
          ▼
       Validate
          │
          ▼
PostgreSQL Database
          │
          ▼
Analytical SQL Queries
```

The application follows a modular ETL architecture. Clinical trial data is retrieved from the API, transformed into normalized relational entities, validated before loading and stored in PostgreSQL for analytical querying.

---

## Execution

Once the database is running, execute the ETL pipeline from the project root:

```bash
python main.py
```

The ETL pipeline is executed in the following stages:

```text
Setup
    │
Extract
    │
Transform
    │
Validate
    │
Load
    │
Pipeline completed
```

---

## ETL Pipeline

The application follows a classic **Extract – Transform – Load (ETL)** architecture.

### Extract

- Retrieve clinical trial studies from the ClinicalTrials.gov API.
- Handle API pagination.
- Validate HTTP responses.
- Return the raw study data.

### Transform

- Parse the API response.
- Normalize the JSON structure.
- Standardize condition and intervention names.
- Convert partial dates into SQL-compatible dates.
- Build a normalized relational model.

### Load

- Perform a full-refresh load.
- Recreate the target schema.
- Populate all relational tables.
- Preserve referential integrity.

---

## Data Model

The normalized relational schema consists of the following tables:

- studies
- conditions
- study_conditions
- interventions
- study_interventions
- locations

The schema definition is available in:

```text
sql/schema.sql
```

---

## Analytical Queries

Example analytical SQL queries are available in:

```text
sql/analytics.sql
```

These queries demonstrate how the normalized schema can be used to answer common analytical questions about clinical trial data.

---

## Testing

Run the complete test suite:

```bash
pytest -v
```

The test suite covers:

- Data transformation
- Data validation
- Referential integrity
- Utility functions

---

## Code Quality

Code quality was verified using standard Python development tools:

- Black (code formatting)
- isort (import ordering)
- flake8 (static analysis)

---

## Documentation

Additional project documentation:

- 📖 **[Configuration Guide](docs/configuration.md)** – Environment configuration
- 🏗️ **[Design Decisions](docs/design-decisions.md)** – Architecture and design rationale
- 💡 **[Bonus Questions](docs/bonus-questions.md)** – Scalability, data quality, compliance, monitoring and security considerations

---

## Trade-offs and Limitations

This prototype intentionally prioritizes clarity and maintainability over production-level complexity.

Current limitations include:

- Full refresh loading instead of incremental loading.
- Single data source (ClinicalTrials.gov API v2).
- Sequential execution without workflow orchestration.
- Local PostgreSQL deployment intended for development purposes.
- Basic data quality validation focused on the challenge requirements.

---

## Time Allocation

Approximate effort invested:

| Task | Time |
|------|-----:|
| Environment setup |  1 h |
| Data exploration & schema design |  3 h |
| ETL implementation |  2 h |
| SQL analytics |  1 h |
| Testing |  1 h |
| Documentation & polishing |  3 h |

**Total effort:** ~11 hours

---

## AI Assistance

AI-assisted development tools (ChatGPT) were used during the development of this project to support:

- brainstorming and design discussions
- code review and refactoring suggestions
- documentation improvements
- test case design

All architectural decisions and implementation details were reviewed, understood and validated by the author.

---

## Author

**Santi Rodríguez**