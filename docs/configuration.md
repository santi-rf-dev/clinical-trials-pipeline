# Configuration

Create a file named `.env` in the project root with the following content:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=clinical_trials
DB_USER=clinical_user
DB_PASSWORD=clinical_password

MAX_STUDIES=1000
PAGE_SIZE=100
```

The default values are intended for the PostgreSQL instance started with Docker Compose.