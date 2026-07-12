import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import URL

logger = logging.getLogger(__name__)


def create_database_engine(
    host: str,
    port: int,
    database: str,
    username: str,
    password: str,
) -> Engine:
    """Create a SQLAlchemy engine for PostgreSQL."""
    connection_url = URL.create(
        drivername="postgresql+psycopg",
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )

    return create_engine(connection_url)


def initialize_database(
    engine: Engine,
    schema_path: str | Path = "sql/schema.sql",
) -> None:
    """Create the database schema from a SQL file."""
    sql = Path(schema_path).read_text(encoding="utf-8")

    with engine.begin() as connection:
        raw_connection = connection.connection
        with raw_connection.cursor() as cursor:
            cursor.execute(sql)

    logger.info("Database schema initialized.")


def load_base_tables(
    engine: Engine,
    tables: dict[str, pd.DataFrame],
) -> None:
    """Load main and dimension tables into PostgreSQL."""
    tables["studies"].to_sql(
        "studies",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    tables["conditions"].to_sql(
        "conditions",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    tables["interventions"].to_sql(
        "interventions",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    tables["locations"].to_sql(
        "locations",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    logger.info("Base tables loaded.")


def build_study_conditions(
    engine: Engine,
    study_conditions: pd.DataFrame,
) -> pd.DataFrame:
    """Replace condition names with their database identifiers."""
    conditions = pd.read_sql(
        """
        SELECT condition_id, condition_name
        FROM conditions
        """,
        engine,
    )

    return (
        study_conditions.merge(
            conditions,
            on="condition_name",
            how="inner",
            validate="many_to_one",
        )[["nct_id", "condition_id"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )


def build_study_interventions(
    engine: Engine,
    study_interventions: pd.DataFrame,
) -> pd.DataFrame:
    interventions = pd.read_sql(
        """
        SELECT
            intervention_id,
            intervention_name,
            intervention_type
        FROM interventions
        """,
        engine,
    )

    return (
        study_interventions.merge(
            interventions,
            on=["intervention_name", "intervention_type"],
            how="inner",
            validate="many_to_one",
        )[["nct_id", "intervention_id"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )


def load_tables(
    engine: Engine,
    tables: dict[str, pd.DataFrame],
) -> None:
    """Load transformed tables into PostgreSQL."""
    logger.info("Starting database load.")

    tables["studies"].to_sql(
        "studies",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    tables["conditions"].to_sql(
        "conditions",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    tables["interventions"].to_sql(
        "interventions",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    tables["locations"].to_sql(
        "locations",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    study_conditions = build_study_conditions(
        engine,
        tables["study_conditions"],
    )

    study_interventions = build_study_interventions(
        engine,
        tables["study_interventions"],
    )

    study_conditions.to_sql(
        "study_conditions",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    study_interventions.to_sql(
        "study_interventions",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    logger.info("Database load completed successfully.")
