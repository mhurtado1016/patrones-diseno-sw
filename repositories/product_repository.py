from repositories.base import IdentifiedRepository


class ProductRepository(IdentifiedRepository):
    collection = "products"

    def exists(self, product_id: int) -> bool:
        return self.find_by_id(product_id) is not None

    def find_by_category(self, category: str) -> list:
        return [p for p in self.all() if p["category"].lower() == category.lower()]
