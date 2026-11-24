from repositories.base import JsonRepository


class FavoriteRepository(JsonRepository):
    """Los favoritos se identifican por (user_id, product_id); no tienen id propio."""
    collection = "favorites"

    def remove(self, user_id: int, product_id: int) -> None:
        remaining = [f for f in self.all()
                     if not (f["user_id"] == user_id and f["product_id"] == product_id)]
        self._db.save_collection(self.collection, remaining)
