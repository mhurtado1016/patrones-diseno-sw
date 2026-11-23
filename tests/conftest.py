import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
from utils.database_connection import DatabaseConnection  # noqa: E402

AUTH = {"Authorization": "abcd12345"}


@pytest.fixture
def client(tmp_path):
    db = tmp_path / "db.json"
    shutil.copy(ROOT / "db_bck.json", db)
    DatabaseConnection.reset()
    with open(db) as f:
        json.load(f)
    yield create_app(str(db)).test_client()
    DatabaseConnection.reset()


@pytest.fixture
def auth():
    return AUTH
