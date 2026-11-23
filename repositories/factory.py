"""Patrón Factory: único lugar que sabe cómo construir cada repositorio."""
import config
from repositories.category_repository import CategoryRepository
from repositories.favorite_repository import FavoriteRepository
from repositories.product_repository import ProductRepository
from utils.database_connection import DatabaseConnection


class RepositoryFactory:
    _registry = {
        "products": ProductRepository,
        "categories": CategoryRepository,
        "favorites": FavoriteRepository,
    }

    def __init__(self, db_path: str = None):
        self._db = DatabaseConnection(db_path or config.DB_PATH)

    def create(self, name: str):
        try:
            return self._registry[name](self._db)
        except KeyError:
            raise ValueError(f"Repositorio desconocido: {name}")
