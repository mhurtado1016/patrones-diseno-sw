import json
import os
import shutil
from pathlib import Path

import pytest

from app import create_app
from auth.token_validator import TokenValidator
from repositories.factory import RepositoryFactory
from repositories.favorite_repository import FavoriteRepository
from repositories.product_repository import ProductRepository
from utils.database_connection import DatabaseConnection

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def db_file(tmp_path):
    path = tmp_path / "db.json"
    shutil.copy(ROOT / "db_bck.json", path)
    DatabaseConnection.reset()
    yield path
    DatabaseConnection.reset()


def test_strategy_alternative_validator_is_used(db_file):
    class OnlyAdmin(TokenValidator):
        def is_valid(self, token):
            return token == "admin-token"

    client = create_app(str(db_file), token_validator=OnlyAdmin()).test_client()
    assert client.get("/products", headers={"Authorization": "abcd12345"}).status_code == 401
    assert client.get("/products", headers={"Authorization": "admin-token"}).status_code == 200


def test_validators_are_isolated_between_apps(db_file):
    class Nobody(TokenValidator):
        def is_valid(self, token):
            return False

    strict = create_app(str(db_file), token_validator=Nobody()).test_client()
    default = create_app(str(db_file)).test_client()
    h = {"Authorization": "abcd12345"}
    assert strict.get("/products", headers=h).status_code == 401
    assert default.get("/products", headers=h).status_code == 200


def test_factory_unknown_repository(db_file):
    with pytest.raises(ValueError):
        RepositoryFactory(str(db_file)).create("users")


def test_singleton_one_instance_per_path(db_file):
    assert DatabaseConnection(str(db_file)) is DatabaseConnection(str(db_file))


def test_data_persisted_to_file(db_file):
    repo = RepositoryFactory(str(db_file)).create("products")
    repo.add({"name": "Scarf", "category": "women", "price": 12.0})
    on_disk = json.loads(db_file.read_text())
    assert any(p["name"] == "Scarf" for p in on_disk["products"])


def test_atomic_write_leaves_no_temp_files_and_valid_json(db_file):
    repo = RepositoryFactory(str(db_file)).create("categories")
    for i in range(5):
        repo.add({"name": f"c{i}"})
    assert [f for f in os.listdir(db_file.parent) if f.endswith(".tmp")] == []
    json.loads(db_file.read_text())


def test_failed_write_keeps_original_file(db_file, monkeypatch):
    before = db_file.read_text()
    db = DatabaseConnection(str(db_file))

    def boom(*a, **k):
        raise OSError("disk full")

    monkeypatch.setattr(os, "replace", boom)
    with pytest.raises(OSError):
        db.save_collection("categories", [])
    assert db_file.read_text() == before
    assert [f for f in os.listdir(db_file.parent) if f.endswith(".tmp")] == []


def test_favorite_repository_has_no_id_lookup():
    # Liskov: FavoriteRepository ya no hereda find_by_id
    assert not hasattr(FavoriteRepository, "find_by_id")
    assert hasattr(ProductRepository, "find_by_id")


def test_failed_write_does_not_change_memory(db_file, monkeypatch):
    db = DatabaseConnection(str(db_file))
    n = len(db.get_collection("categories"))
    monkeypatch.setattr(os, "replace", lambda *a, **k: (_ for _ in ()).throw(OSError("x")))
    with pytest.raises(OSError):
        db.save_collection("categories", [])
    assert len(db.get_collection("categories")) == n
