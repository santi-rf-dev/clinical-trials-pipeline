import logging
import os
import re
from pathlib import Path

import pandas as pd
from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import URL

logger = logging.getLogger(__name__)


def validate_schema_name(schema: str) -> None:
    """Validate the PostgreSQL schema identifier."""
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", schema):
        raise ValueError(f"Invalid database schema name: {schema}")


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
    schema: str,
) -> None:
    """Recreate the PostgreSQL schema from the project SQL file."""
    validate_schema_name(schema)

    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "sql",
        "schema.sql",
    )
    sql = Path(schema_path).read_text(encoding="utf-8")
    sql = sql.replace("{{schema}}", schema)

    with engine.begin() as connection:
        raw_connection = connection.connection

        with raw_connection.cursor() as cursor:
            cursor.execute(sql)

    logger.info("Database schema '%s' initialized.", schema)


def build_study_conditions(
    engine: Engine,
    study_conditions: pd.DataFrame,
    schema: str,
) -> pd.DataFrame:
    """Replace condition names with their database identifiers."""
    validate_schema_name(schema)

    conditions = pd.read_sql(
        f"""
        SELECT condition_id, condition_name
          FROM {schema}.conditions
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
    schema: str,
) -> pd.DataFrame:
    """Replace intervention attributes with their database identifiers."""
    validate_schema_name(schema)

    interventions = pd.read_sql(
        f"""
        SELECT intervention_id, intervention_name, intervention_type
          FROM {schema}.interventions
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
    schema: str,
    tables: dict[str, pd.DataFrame],
) -> None:
    """Load transformed tables into PostgreSQL."""
    validate_schema_name(schema)

    logger.info("Starting database load.")

    # Load main and lookup tables
    tables["studies"].to_sql(
        "studies",
        engine,
        schema=schema,
        if_exists="append",
        index=False,
        method="multi",
    )

    tables["conditions"].to_sql(
        "conditions",
        engine,
        schema=schema,
        if_exists="append",
        index=False,
        method="multi",
    )

    tables["interventions"].to_sql(
        "interventions",
        engine,
        schema=schema,
        if_exists="append",
        index=False,
        method="multi",
    )

    tables["locations"].to_sql(
        "locations",
        engine,
        schema=schema,
        if_exists="append",
        index=False,
        method="multi",
    )

    # Resolve generated identifiers
    study_conditions = build_study_conditions(
        engine=engine,
        study_conditions=tables["study_conditions"],
        schema=schema,
    )

    study_interventions = build_study_interventions(
        engine=engine,
        study_interventions=tables["study_interventions"],
        schema=schema,
    )

    study_conditions.to_sql(
        "study_conditions",
        engine,
        schema=schema,
        if_exists="append",
        index=False,
        method="multi",
    )

    study_interventions.to_sql(
        "study_interventions",
        engine,
        schema=schema,
        if_exists="append",
        index=False,
        method="multi",
    )

    logger.info("Database load completed successfully.")
