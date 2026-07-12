# tests/test_validation.py

import pandas as pd
import pytest

from src.validation import validate_studies


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
