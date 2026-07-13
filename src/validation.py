import pandas as pd


def validate_tables(tables: dict[str, pd.DataFrame]) -> None:
    """Run all data quality validations before loading the database."""

    # Validate each entity independently
    validate_studies(tables["studies"])
    validate_locations(tables["locations"])

    # Validate referential integrity across tables
    validate_relationships(tables)


def validate_studies(studies: pd.DataFrame) -> None:
    """Validate study data."""

    # Validate mandatory study identifiers
    if studies["nct_id"].isna().any():
        raise ValueError("studies contains null nct_id values.")

    # Validate uniqueness of study identifiers
    if studies["nct_id"].duplicated().any():
        raise ValueError("studies contains duplicate nct_id values.")

    # Validate enrollment values
    invalid_enrollment = studies["enrollment_count"].dropna().lt(0)

    if invalid_enrollment.any():
        raise ValueError("studies contains negative enrollment values.")


def validate_locations(locations: pd.DataFrame) -> None:
    """Validate location data."""

    # Validate geographic coordinates
    invalid_latitude = locations["latitude"].dropna().between(-90, 90).eq(False)
    invalid_longitude = locations["longitude"].dropna().between(-180, 180).eq(False)

    if invalid_latitude.any():
        raise ValueError("locations contains invalid latitude values.")

    if invalid_longitude.any():
        raise ValueError("locations contains invalid longitude values.")


def validate_relationships(
    tables: dict[str, pd.DataFrame],
) -> None:
    """Validate referential integrity between tables."""

    # Validate foreign key relationships
    study_ids = set(tables["studies"]["nct_id"])

    for table_name in (
        "study_conditions",
        "study_interventions",
        "locations",
    ):
        orphan_ids = set(tables[table_name]["nct_id"]) - study_ids

        if orphan_ids:
            raise ValueError(f"{table_name} contains orphan study references.")
