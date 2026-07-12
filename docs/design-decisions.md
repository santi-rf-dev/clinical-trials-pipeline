# Design Decisions

This document summarizes the main architectural, modeling and implementation decisions made during the development of the Clinical Trial Data Pipeline.

---

# Dataset

The project uses the **ClinicalTrials.gov API v2** as the primary data source.

The API was intentionally selected instead of a static dataset because it better demonstrates several Data Engineering concepts, including:

- REST API integration
- Pagination handling
- Semi-structured JSON processing
- ETL design for live data sources

---

# Architecture

The project follows a classic ETL architecture with a clear separation of responsibilities.

```text
ClinicalTrials.gov API
            │
            ▼
        Extract Layer
            │
            ▼
      Transform Layer
            │
            ▼
      Validation Layer
            │
            ▼
 PostgreSQL (Normalized)
            │
            ▼
 Analytical SQL Queries
```

Each stage is implemented independently, making the pipeline easier to maintain, test and extend.

---

# Data Exploration

Before implementing the pipeline, an exploratory analysis of the API response was performed.

The objective was to understand the JSON structure, identify the available entities and design an appropriate relational model.

Only the original study data contained in the `protocolSection` was considered for the first version.

The `derivedSection` was intentionally excluded because it contains metadata enriched by ClinicalTrials.gov rather than original study data.

---

# ETL Strategy

The project follows a classic ETL architecture complemented by a dedicated validation layer.

## Extract

Responsible for retrieving studies from the ClinicalTrials.gov API, handling pagination and validating HTTP responses.

## Transform

Responsible for parsing the API response, normalizing the data, applying data quality rules and generating the relational entities.

## Load

Responsible for creating the PostgreSQL schema and loading the transformed data while preserving referential integrity.

The current implementation performs a **full refresh** on every execution by recreating the target schema before loading the latest extracted dataset.

---

# Data Model

A **normalized relational model** was selected.

The source data contains multiple one-to-many and many-to-many relationships between studies, conditions, interventions and locations.

Using a normalized schema minimizes data duplication and preserves data integrity.

```text
studies
    │
    ├────< study_conditions >──── conditions
    │
    ├────< study_interventions >── interventions
    │
    └────< locations
```

The following tables were implemented:

- studies
- conditions
- study_conditions
- interventions
- study_interventions
- locations

---

# Why not a Star Schema?

A dimensional model was intentionally not used.

The challenge explicitly requests a normalized database schema, and the source data is naturally relational.

A star schema would be more appropriate as a downstream analytical layer rather than as the operational storage model.

---

# Primary Keys

The ClinicalTrials.gov identifier (`nct_id`) is used as the primary key of the `studies` table.

Since it is globally unique and stable, no surrogate key was introduced.

The remaining entities use surrogate integer primary keys.

---

# Relationships

Many-to-many relationships are implemented through bridge tables.

- studies ↔ conditions
- studies ↔ interventions

Locations are modeled as a child entity of studies because each study may be conducted at multiple facilities.

---

# Data Standardization

Several transformations are applied during the ETL process to improve data consistency.

These include:

- trimming leading and trailing spaces
- normalizing condition and intervention names to uppercase
- removing duplicate relationships
- handling missing values
- converting partial dates into SQL-compatible dates

These transformations are intentionally performed in the ETL layer rather than in the database.

---

# Date Handling

ClinicalTrials.gov provides dates with different levels of precision.

Examples:

- YYYY
- YYYY-MM
- YYYY-MM-DD

For consistency, partial dates are converted to valid SQL dates by assuming the first available day.

| API value | Stored value |
|-----------|--------------|
| 2008 | 2008-01-01 |
| 2008-09 | 2008-09-01 |
| 2008-09-15 | 2008-09-15 |

This simplification is considered acceptable for the analytical goals of this prototype.

---

# Data Validation

Data validation is performed after the transformation stage and before loading the data into PostgreSQL.

The validation layer verifies that the transformed dataset satisfies a number of integrity rules before any data is written to the database.

Examples include:

- mandatory study identifier
- duplicate study detection
- non-negative enrollment values
- valid geographic coordinates
- referential integrity between tables

---

# Scope

Some API modules were intentionally excluded from the first version.

Excluded modules:

- descriptionModule
- oversightModule
- eligibilityModule

Potential future extensions:

- sponsorCollaboratorsModule
- outcomesModule

These modules were excluded because they are not required to answer the analytical questions proposed in the challenge.

---

# Database Constraints

The schema includes the following integrity constraints:

- Primary Keys
- Foreign Keys
- NOT NULL constraints
- UNIQUE constraints
- CHECK constraints

These constraints guarantee referential integrity while keeping the implementation simple.

---

# Loading Strategy

The prototype implements a **full refresh** loading strategy.

Each execution recreates the target schema only after the extracted data has been successfully transformed and validated.

This prevents the previous dataset from being removed if the ETL process fails before the loading stage.

This approach keeps the implementation deterministic and simple for the purposes of the technical challenge.

A production implementation would most likely replace this strategy with an incremental loading mechanism (UPSERT or CDC).

---

# Indexing Strategy

Indexes were added only on columns expected to be frequently used for filtering or aggregation.

Examples include:

- study status
- study type
- phase
- country
- intervention type

The objective is to balance query performance and insertion cost.

---

# Future Improvements

## Data Engineering

- Incremental loading
- Change Data Capture (CDC)
- Workflow orchestration (Airflow or Prefect)

## Data Quality

- MeSH terminology normalization
- Data quality reports
- Additional validation rules

## Data Model

- Sponsor information
- Outcome measures
- Eligibility criteria

## Operations

- Pipeline monitoring
- Enhanced logging
- Data lineage