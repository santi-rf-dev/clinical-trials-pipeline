import logging

from sqlalchemy.exc import OperationalError

from src.config import Config
from src.extract import fetch_studies
from src.load import create_database_engine, initialize_database, load_tables
from src.transform import transform_studies
from src.validation import validate_tables

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the Clinical Trial ETL pipeline."""

    # Configure application logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    # Initialize application configuration
    conf = Config()

    # Create the database connection
    try:
        engine = create_database_engine(
            host=conf.db_host,
            port=conf.db_port,
            database=conf.db_name,
            username=conf.db_user,
            password=conf.db_password,
        )

        # Initialize the database schema
        initialize_database(engine)

    except OperationalError as exc:
        logger.error(
            "Unable to connect to PostgreSQL. "
            "Ensure the database is running (docker compose up -d)."
        )
        raise SystemExit(1) from exc

    # Extract raw studies from the ClinicalTrials.gov API
    raw_studies = fetch_studies(
        base_url=conf.base_url,
        request_timeout_seconds=conf.request_timeout_seconds,
        max_studies=conf.max_studies,
        page_size=conf.page_size,
    )

    # Transform the raw JSON into relational tables
    tables = transform_studies(raw_studies)

    # Validate the transformed data before loading
    validate_tables(tables)

    # Load the transformed data into PostgreSQL
    load_tables(engine, tables)

    logger.info("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
