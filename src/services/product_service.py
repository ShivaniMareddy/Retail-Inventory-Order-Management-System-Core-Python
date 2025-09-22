from typing import Dict, List
from src.dao.product_dao import ProductDAO

class ProductError(Exception): pass

class ProductService:
    def __init__(self):
        self.repo = ProductDAO()

    def add(self, name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Dict:
        if price <= 0:
            raise ProductError("Price must be greater than 0")
        if self.repo.get_by_sku(sku):
            raise ProductError(f"SKU already exists: {sku}")
        return self.repo.create(name, sku, price, stock, category)

    def update(self, prod_id: int, **fields) -> Dict:
        if "price" in fields and fields["price"] <= 0:
            raise ProductError("Price must be greater than 0")
        existing = self.repo.get_by_id(prod_id)
        if not existing:
            raise ProductError("Product not found")
        return self.repo.update(prod_id, fields)

    def delete(self, prod_id: int) -> Dict:
        existing = self.repo.get_by_id(prod_id)
        if not existing:
            raise ProductError("Product not found")
        return self.repo.delete(prod_id)

    def list(self, limit: int = 100) -> List[Dict]:
        return self.repo.list(limit)
