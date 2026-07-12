# Clinical Trial Data Pipeline

Technical challenge for the **MIGx Data Engineering** position.

This project implements an ETL pipeline that retrieves clinical trial data from the **ClinicalTrials.gov API v2**, transforms the raw JSON into a normalized relational model and stores it in a PostgreSQL database for analytical purposes.

---

# Features

- ClinicalTrials.gov API integration
- Normalized PostgreSQL schema
- Dockerized PostgreSQL
- Automated ETL pipeline
- SQL analytical queries
- Unit tests

---

# Configuration

Before running the application, create the `.env` configuration file following the instructions in:

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

# Data Model

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

# Testing

Run the complete test suite:

```bash
pytest -v
```

The tests cover:

- Data transformation
- Data validation
- Referential integrity
- Utility functions

---

# Project Structure

```text
clinical-trials-pipeline/
├── docs/
├── notebooks/
├── sql/
├── src/
├── tests/
├── .env
├── .gitignore
├── compose.yaml
├── main.py
├── README.md
└── requirements.txt
```

---

# Documentation

Additional project documentation:

- 📖 **[Configuration Guide](docs/configuration.md)** – Environment configuration
- 🏗️ **[Design Decisions](docs/design-decisions.md)** – Architecture and design rationale

---

# Author

Developed by **Santi Rodríguez**