"""ask485 development configuration."""

import pathlib
SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

# Database file is var/insta485.sqlite3
ASK485_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATABASE_FILENAME = ASK485_ROOT/'var'/'insta485.sqlite3'