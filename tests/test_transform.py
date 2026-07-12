from datetime import date

import pytest

from src.transform import (
    clean_text,
    normalize_name,
    parse_partial_date,
    transform_studies,
)


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("2008", date(2008, 1, 1)),
        ("2008-09", date(2008, 9, 1)),
        ("2008-09-15", date(2008, 9, 15)),
        (None, None),
        ("", None),
    ],
)
def test_parse_partial_date(raw_value, expected):
    assert parse_partial_date(raw_value) == expected


def test_parse_partial_date_invalid_format():
    with pytest.raises(
        ValueError,
        match="Unsupported date format",
    ):
        parse_partial_date("15/09/2008")


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("  Breast Cancer  ", "BREAST CANCER"),
        ("Drug A", "DRUG A"),
        (" placebo ", "PLACEBO"),
    ],
)
def test_normalize_name(raw_value, expected):
    assert normalize_name(raw_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("  Clinical trial  ", "Clinical trial"),
        ("   ", None),
        (None, None),
    ],
)
def test_clean_text(raw_value, expected):
    assert clean_text(raw_value) == expected


def test_transform_studies_creates_expected_tables():
    raw_studies = [
        {
            "protocolSection": {
                "identificationModule": {
                    "nctId": "NCT00000001",
                    "briefTitle": " Example trial ",
                    "organization": {
                        "fullName": "Example University",
                        "class": "OTHER",
                    },
                },
                "statusModule": {
                    "overallStatus": "COMPLETED",
                    "startDateStruct": {
                        "date": "2020-01",
                    },
                    "completionDateStruct": {
                        "date": "2021-06-15",
                    },
                },
                "designModule": {
                    "studyType": "INTERVENTIONAL",
                    "phases": ["PHASE2"],
                    "enrollmentInfo": {
                        "count": 100,
                        "type": "ACTUAL",
                    },
                },
                "conditionsModule": {
                    "conditions": [
                        "Breast Cancer",
                        " breast cancer ",
                    ]
                },
                "armsInterventionsModule": {
                    "interventions": [
                        {
                            "name": "Drug A",
                            "type": "DRUG",
                        },
                        {
                            "name": " drug a ",
                            "type": "DRUG",
                        },
                    ]
                },
                "contactsLocationsModule": {
                    "locations": [
                        {
                            "facility": "Hospital A",
                            "city": "Barcelona",
                            "country": "Spain",
                            "geoPoint": {
                                "lat": 41.38,
                                "lon": 2.17,
                            },
                        }
                    ]
                },
            }
        }
    ]

    tables = transform_studies(raw_studies)

    assert set(tables) == {
        "studies",
        "conditions",
        "study_conditions",
        "interventions",
        "study_interventions",
        "locations",
    }

    assert len(tables["studies"]) == 1
    assert len(tables["conditions"]) == 1
    assert len(tables["study_conditions"]) == 1
    assert len(tables["interventions"]) == 1
    assert len(tables["study_interventions"]) == 1
    assert len(tables["locations"]) == 1

    study = tables["studies"].iloc[0]

    assert study["nct_id"] == "NCT00000001"
    assert study["brief_title"] == "Example trial"
    assert study["phase"] == "PHASE2"
    assert study["start_date"] == date(2020, 1, 1)
    assert study["completion_date"] == date(2021, 6, 15)
    assert study["enrollment_count"] == 100

    condition = tables["conditions"].iloc[0]
    assert condition["condition_name"] == "BREAST CANCER"

    intervention = tables["interventions"].iloc[0]
    assert intervention["intervention_name"] == "DRUG A"
    assert intervention["intervention_type"] == "DRUG"

    location = tables["locations"].iloc[0]
    assert location["city"] == "Barcelona"
    assert location["country"] == "Spain"
    assert location["latitude"] == 41.38
    assert location["longitude"] == 2.17


def test_transform_studies_skips_study_without_nct_id():
    raw_studies = [
        {
            "protocolSection": {
                "identificationModule": {
                    "briefTitle": "Study without identifier",
                }
            }
        }
    ]

    tables = transform_studies(raw_studies)

    assert tables["studies"].empty
    assert tables["conditions"].empty
    assert tables["study_conditions"].empty
    assert tables["interventions"].empty
    assert tables["study_interventions"].empty
    assert tables["locations"].empty