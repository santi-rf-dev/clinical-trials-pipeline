import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


def fetch_studies(
    base_url: str,
    request_timeout_seconds: int,
    max_studies: int,
    page_size: int,
) -> list[dict[str, Any]]:
    """Fetch clinical trial studies from the ClinicalTrials.gov API with pagination."""

    # Validate input parameters
    if request_timeout_seconds <= 0:
        raise ValueError("request_timeout_seconds must be greater than 0.")

    if max_studies <= 0:
        raise ValueError("max_studies must be greater than 0.")

    if page_size <= 0:
        raise ValueError("page_size must be greater than 0.")

    studies: list[dict[str, Any]] = []
    next_page_token: str | None = None

    while True:
        # Build request parameters
        params: dict[str, Any] = {
            "pageSize": page_size,
            "format": "json",
        }

        if next_page_token is not None:
            params["pageToken"] = next_page_token

        logger.info(
            "Requesting studies from ClinicalTrials.gov. Current total: %s",
            len(studies),
        )

        # Request the next page
        response = requests.get(
            base_url,
            params=params,
            timeout=request_timeout_seconds,
        )

        # Raise an exception if the request failed
        response.raise_for_status()

        # Parse the API response
        data = response.json()
        page_studies = data.get("studies", [])

        # Append retrieved studies
        studies.extend(page_studies)

        logger.info(
            "Retrieved %s studies. Accumulated total: %s",
            len(page_studies),
            len(studies),
        )

        # Return the requested number of studies
        if len(studies) >= max_studies:
            return studies[:max_studies]

        next_page_token = data.get("nextPageToken")

        # Stop when no more pages are available
        if not next_page_token:
            break

    return studies
