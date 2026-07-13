from datetime import date
from typing import Any

import pandas as pd


def parse_partial_date(value: str | None) -> date | None:
    """
    Parse a partial ISO date into a Python date.

    Supported formats:
    - YYYY
    - YYYY-MM
    - YYYY-MM-DD

    Args:
        value: Date string to parse.

    Returns:
        Parsed date or None when the value is empty.

    Raises:
        ValueError: If the date format is unsupported or invalid.
    """
    if not value:
        return None

    date_formats = {
        4: "%Y",
        7: "%Y-%m",
        10: "%Y-%m-%d",
    }

    date_format = date_formats.get(len(value))

    if date_format is None:
        raise ValueError(f"Unsupported date format: {value}")

    try:
        return pd.to_datetime(value, format=date_format).date()
    except ValueError as exc:
        raise ValueError(f"Unsupported date format: {value}") from exc


def normalize_name(value: str) -> str:
    """Normalize a name for consistent deduplication."""
    return value.strip().upper()


def clean_text(value: str | None) -> str | None:
    """Remove leading and trailing whitespace from optional text fields."""
    if value is None:
        return None

    cleaned_value = value.strip()
    return cleaned_value or None


def transform_studies(
    raw_studies: list[dict[str, Any]],
) -> dict[str, pd.DataFrame]:
    """
    Transform raw ClinicalTrials.gov studies into normalized tables.

    Args:
        raw_studies: Raw study dictionaries returned by the API.

    Returns:
        Dictionary containing one DataFrame per destination table.
    """
    # Initialize destination records
    study_rows: list[dict[str, Any]] = []
    condition_rows: list[dict[str, Any]] = []
    study_condition_rows: list[dict[str, Any]] = []
    intervention_rows: list[dict[str, Any]] = []
    study_intervention_rows: list[dict[str, Any]] = []
    location_rows: list[dict[str, Any]] = []

    # Process each study
    for raw_study in raw_studies:
        protocol = raw_study.get("protocolSection", {})

        # Read selected protocol modules
        identification = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        conditions_module = protocol.get("conditionsModule", {})
        interventions_module = protocol.get("armsInterventionsModule", {})
        locations_module = protocol.get("contactsLocationsModule", {})

        nct_id = identification.get("nctId")

        # Skip studies without a valid identifier
        if not nct_id:
            continue

        organization = identification.get("organization", {})
        enrollment = design.get("enrollmentInfo", {})
        phases = design.get("phases", [])

        phase = ", ".join(phases) if phases else None

        # Build study record
        study_rows.append(
            {
                "nct_id": nct_id,
                "brief_title": clean_text(identification.get("briefTitle")),
                "official_title": clean_text(identification.get("officialTitle")),
                "organization_name": clean_text(organization.get("fullName")),
                "organization_class": organization.get("class"),
                "overall_status": status.get("overallStatus"),
                "study_type": design.get("studyType"),
                "phase": phase,
                "enrollment_count": enrollment.get("count"),
                "enrollment_type": enrollment.get("type"),
                "start_date": parse_partial_date(
                    status.get("startDateStruct", {}).get("date")
                ),
                "primary_completion_date": parse_partial_date(
                    status.get(
                        "primaryCompletionDateStruct",
                        {},
                    ).get("date")
                ),
                "completion_date": parse_partial_date(
                    status.get("completionDateStruct", {}).get("date")
                ),
            }
        )

        # Build condition records
        for condition in conditions_module.get("conditions", []):
            condition_name = normalize_name(condition)

            condition_rows.append(
                {
                    "condition_name": condition_name,
                }
            )

            study_condition_rows.append(
                {
                    "nct_id": nct_id,
                    "condition_name": condition_name,
                }
            )

        # Build intervention records
        for intervention in interventions_module.get(
            "interventions",
            [],
        ):
            intervention_name = clean_text(intervention.get("name"))
            intervention_type = intervention.get("type")

            # Skip incomplete intervention records
            if not intervention_name or not intervention_type:
                continue

            intervention_name = normalize_name(intervention_name)

            intervention_rows.append(
                {
                    "intervention_name": intervention_name,
                    "intervention_type": intervention_type,
                }
            )

            study_intervention_rows.append(
                {
                    "nct_id": nct_id,
                    "intervention_name": intervention_name,
                    "intervention_type": intervention_type,
                }
            )

        # Build location records
        for location in locations_module.get("locations", []):
            geo_point = location.get("geoPoint", {})

            location_rows.append(
                {
                    "nct_id": nct_id,
                    "facility": clean_text(location.get("facility")),
                    "city": clean_text(location.get("city")),
                    "state": clean_text(location.get("state")),
                    "country": clean_text(location.get("country")),
                    "zip_code": clean_text(location.get("zip")),
                    "latitude": geo_point.get("lat"),
                    "longitude": geo_point.get("lon"),
                }
            )

    # Create destination DataFrames
    tables = {
        "studies": pd.DataFrame(study_rows),
        "conditions": pd.DataFrame(condition_rows),
        "study_conditions": pd.DataFrame(study_condition_rows),
        "interventions": pd.DataFrame(intervention_rows),
        "study_interventions": pd.DataFrame(study_intervention_rows),
        "locations": pd.DataFrame(location_rows),
    }

    # Normalize lookup and relationship tables
    tables["conditions"] = tables["conditions"].drop_duplicates(
        subset=["condition_name"]
    )

    tables["study_conditions"] = tables["study_conditions"].drop_duplicates(
        subset=["nct_id", "condition_name"]
    )

    tables["interventions"] = tables["interventions"].drop_duplicates(
        subset=["intervention_name", "intervention_type"]
    )

    tables["study_interventions"] = tables["study_interventions"].drop_duplicates(
        subset=[
            "nct_id",
            "intervention_name",
            "intervention_type",
        ]
    )

    tables["locations"] = tables["locations"].drop_duplicates()

    # Reset DataFrame indexes
    for table_name, dataframe in tables.items():
        tables[table_name] = dataframe.reset_index(drop=True)

    return tables
