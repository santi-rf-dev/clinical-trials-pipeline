import pandas as pd
import pytest

from src.validation import validate_locations, validate_relationships, validate_studies

# Study validations


def test_validate_studies_accepts_valid_data():
    studies = pd.DataFrame(
        {
            "nct_id": ["NCT001"],
            "enrollment_count": [100],
        }
    )

    validate_studies(studies)


def test_validate_studies_rejects_null_nct_id():
    studies = pd.DataFrame(
        {
            "nct_id": [None],
            "enrollment_count": [100],
        }
    )

    with pytest.raises(
        ValueError,
        match="null nct_id",
    ):
        validate_studies(studies)


def test_validate_studies_rejects_duplicate_nct_ids():
    studies = pd.DataFrame(
        {
            "nct_id": ["NCT001", "NCT001"],
            "enrollment_count": [100, 200],
        }
    )

    with pytest.raises(
        ValueError,
        match="duplicate nct_id",
    ):
        validate_studies(studies)


def test_validate_studies_rejects_negative_enrollment():
    studies = pd.DataFrame(
        {
            "nct_id": ["NCT001"],
            "enrollment_count": [-10],
        }
    )

    with pytest.raises(
        ValueError,
        match="negative enrollment",
    ):
        validate_studies(studies)


# Location validations


def test_validate_locations_accepts_valid_coordinates():
    locations = pd.DataFrame(
        {
            "latitude": [41.38, None],
            "longitude": [2.17, None],
        }
    )

    validate_locations(locations)


def test_validate_locations_rejects_invalid_latitude():
    locations = pd.DataFrame(
        {
            "latitude": [95],
            "longitude": [2],
        }
    )

    with pytest.raises(
        ValueError,
        match="invalid latitude",
    ):
        validate_locations(locations)


def test_validate_locations_rejects_invalid_longitude():
    locations = pd.DataFrame(
        {
            "latitude": [41],
            "longitude": [190],
        }
    )

    with pytest.raises(
        ValueError,
        match="invalid longitude",
    ):
        validate_locations(locations)


# Relationship validations


def test_validate_relationships_accepts_valid_references():
    tables = {
        "studies": pd.DataFrame(
            {
                "nct_id": ["NCT001"],
            }
        ),
        "study_conditions": pd.DataFrame(
            {
                "nct_id": ["NCT001"],
            }
        ),
        "study_interventions": pd.DataFrame(
            {
                "nct_id": ["NCT001"],
            }
        ),
        "locations": pd.DataFrame(
            {
                "nct_id": ["NCT001"],
            }
        ),
    }

    validate_relationships(tables)


def test_validate_relationships_rejects_orphan_studies():
    tables = {
        "studies": pd.DataFrame(
            {
                "nct_id": ["NCT001"],
            }
        ),
        "study_conditions": pd.DataFrame(
            {
                "nct_id": ["NCT999"],
            }
        ),
        "study_interventions": pd.DataFrame(
            {
                "nct_id": [],
            }
        ),
        "locations": pd.DataFrame(
            {
                "nct_id": [],
            }
        ),
    }

    with pytest.raises(
        ValueError,
        match="orphan study references",
    ):
        validate_relationships(tables)
