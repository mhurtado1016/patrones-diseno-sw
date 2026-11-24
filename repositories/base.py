"""Patrón Repository: encapsula el acceso a datos de una colección."""
from utils.database_connection import DatabaseConnection


class JsonRepository:
    """Operaciones comunes a cualquier colección (sin suponer que tiene 'id')."""
    collection = None  # cada subclase define su colección

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def all(self) -> list:
        return self._db.get_collection(self.collection)

    def add(self, data: dict) -> dict:
        items = self.all()
        items.append(data)
        self._db.save_collection(self.collection, items)
        return data


class IdentifiedRepository(JsonRepository):
    """Colecciones cuyos elementos tienen 'id' autogenerado."""

    def find_by_id(self, item_id: int):
        return next((i for i in self.all() if i.get("id") == item_id), None)

    @staticmethod
    def _next_id(items: list) -> int:
        # max+1 en vez de len+1: evita ids duplicados tras eliminar elementos
        return max((i.get("id", 0) for i in items), default=0) + 1

    def add(self, data: dict) -> dict:
        items = self.all()
        item = {"id": self._next_id(items), **data}
        items.append(item)
        self._db.save_collection(self.collection, items)
        return item
