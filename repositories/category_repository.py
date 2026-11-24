from repositories.base import IdentifiedRepository


class CategoryRepository(IdentifiedRepository):
    collection = "categories"

    def find_by_name(self, name: str):
        return next((c for c in self.all() if c["name"] == name), None)

    def exists(self, name: str) -> bool:
        return any(c["name"].lower() == name.lower() for c in self.all())

    def remove_by_name(self, name: str) -> bool:
        items = self.all()
        remaining = [c for c in items if c["name"] != name]
        if len(remaining) == len(items):
            return False
        self._db.save_collection(self.collection, remaining)
        return True
