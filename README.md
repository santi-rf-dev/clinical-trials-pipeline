# Clinical Trial Data Pipeline

Technical challenge for the **MIGx Data Engineering** position.

This project implements an ETL pipeline that retrieves clinical trial data from the **ClinicalTrials.gov API v2**, transforms the raw JSON into a normalized relational model and stores it in a PostgreSQL database for analytical purposes.

---

# Configuration

Before running the application, create the configuration file described in:

- **Configuration Guide** (`docs/configuration.md`)

---

# Installation

It is recommended to use a dedicated Python virtual environment to isolate the project's dependencies.

## Windows

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

# Database

The project uses **PostgreSQL**, which is provided through Docker Compose.

Start the database:

```bash
docker compose up -d
```

Docker Compose starts a PostgreSQL instance and creates the `clinical_trials` database.

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

# Execution

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

# ETL Pipeline

The application follows a classic **Extract – Transform – Load (ETL)** architecture.

## Extract

- Retrieve clinical trial studies from the ClinicalTrials.gov API.
- Handle API pagination.
- Validate HTTP responses.
- Return the raw study data.

## Transform

- Parse the API response.
- Normalize the JSON structure.
- Standardize condition names.
- Convert partial dates into SQL-compatible dates.
- Build a normalized relational model.

## Load

- Perform a full-refresh load.
- Populate all relational tables.
- Preserve referential integrity.

---

# Database Schema

The normalized schema contains the following tables:

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

# Analytical Queries

Example analytical SQL queries are available in:

```text
sql/analytics.sql
```

These queries demonstrate how the normalized schema can be used to answer the business questions proposed in the technical challenge.

---

# Project Structure

```text
clinical-trials-pipeline/
├── docs/
│   ├── configuration.md
│   └── design-decisions.md
├── notebooks/
│   └── api_exploration.ipynb
├── sql/
│   ├── schema.sql
│   └── analytics.sql
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── ...
├── tests/
├── main.py
├── requirements.txt
├── compose.yaml
└── README.md
```

---

# Documentation

Additional documentation is available in:

- **Configuration Guide** (`docs/configuration.md`)
- **Design Decisions** (`docs/design-decisions.md`)
---

## Author

**Santi Rodríguez**