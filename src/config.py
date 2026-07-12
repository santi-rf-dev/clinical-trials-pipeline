import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    """Application configuration loaded from environment variables."""

    # ClinicalTrials.gov API
    base_url: str = os.environ["BASE_URL"]
    request_timeout_seconds: int = int(os.environ["REQUEST_TIMEOUT_SECONDS"])
    max_studies: int = int(os.environ["MAX_STUDIES"])
    page_size: int = int(os.environ["PAGE_SIZE"])

    # PostgreSQL
    db_host: str = os.environ["DB_HOST"]
    db_port: int = int(os.environ["DB_PORT"])
    db_name: str = os.environ["DB_NAME"]
    db_schema: str = os.environ["DB_SCHEMA"]
    db_user: str = os.environ["DB_USER"]
    db_password: str = os.environ["DB_PASSWORD"]
