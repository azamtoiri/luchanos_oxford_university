"""File with settings and configs for the project"""

from typing import cast
from decouple import config

def _str_config(searching_path: str, *args, **kwargs) -> str:
    """Convert to string"""
    obj = config(searching_path, *args, **kwargs)

    return cast(str, obj)


class Connection:
    """Config connection to database"""
    REAL_DATABASE_URL = _str_config("REAL_DATABASE_URL")
    TEST_DATABASE_URL = _str_config("TEST_DATABASE_URL")
