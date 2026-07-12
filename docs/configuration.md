# Configuration

The application is configured through environment variables loaded from a `.env` file located in the project root.

All configuration variables are **required**. The application will fail to start if any variable is missing.

---

## Example

```text
# ClinicalTrials.gov API
BASE_URL=https://clinicaltrials.gov/api/v2/studies
REQUEST_TIMEOUT_SECONDS=30
MAX_STUDIES=1000
PAGE_SIZE=100

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=clinical
DB_SCHEMA=clinical_trials
DB_USER=clinical_user
DB_PASSWORD=clinical_password
```

---

## Configuration Variables

### ClinicalTrials.gov API

| Variable | Description |
|----------|-------------|
| `BASE_URL` | ClinicalTrials.gov API v2 endpoint. |
| `REQUEST_TIMEOUT_SECONDS` | HTTP request timeout in seconds. |
| `MAX_STUDIES` | Maximum number of studies to retrieve. |
| `PAGE_SIZE` | Number of studies requested per API call. |

### PostgreSQL

| Variable | Description |
|----------|-------------|
| `DB_HOST` | PostgreSQL server hostname. |
| `DB_PORT` | PostgreSQL server port. |
| `DB_NAME` | PostgreSQL database name. |
| `DB_SCHEMA` | Database schema where the application tables are created. |
| `DB_USER` | Database username. |
| `DB_PASSWORD` | Database password. |

---

## Notes

- The PostgreSQL values shown above match the local Docker Compose configuration included in this project.
- `MAX_STUDIES` controls how many studies are retrieved from the ClinicalTrials.gov API.
- `PAGE_SIZE` defines the number of studies requested per API call.
- The ETL pipeline automatically creates the configured database schema if it does not already exist.
- The `.env` file should not be committed to version control.