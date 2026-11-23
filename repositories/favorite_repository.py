from repositories.base import JsonRepository


class FavoriteRepository(JsonRepository):
    collection = "favorites"

    def add(self, data: dict) -> dict:
        # los favoritos se identifican por (user_id, product_id), no tienen id propio
        items = self.all()
        items.append(data)
        self._db.save_collection(self.collection, items)
        return data

    def remove(self, user_id: int, product_id: int) -> None:
        remaining = [f for f in self.all()
                     if not (f["user_id"] == user_id and f["product_id"] == product_id)]
        self._db.save_collection(self.collection, remaining)
