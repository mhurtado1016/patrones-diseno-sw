from repositories.base import JsonRepository


class ProductRepository(JsonRepository):
    collection = "products"

    def find_by_category(self, category: str) -> list:
        return [p for p in self.all() if p["category"].lower() == category.lower()]
