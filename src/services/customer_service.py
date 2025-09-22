from typing import Dict, List
from src.dao.customer_dao import CustomerDAO

class CustomerError(Exception): pass

class CustomerService:
    def __init__(self):
        self.repo = CustomerDAO()

    def add(self, name: str, email: str, phone: str, city: str | None = None) -> Dict:
        return self.repo.create(name, email, phone, city)

    def update(self, cust_id: int, **fields) -> Dict:
        existing = self.repo.get_by_id(cust_id)
        if not existing:
            raise CustomerError("Customer not found")
        return self.repo.update(cust_id, fields)

    def delete(self, cust_id: int) -> Dict:
        existing = self.repo.get_by_id(cust_id)
        if not existing:
            raise CustomerError("Customer not found")
        return self.repo.delete(cust_id)

    def list(self, limit: int = 100) -> List[Dict]:
        return self.repo.list(limit)
