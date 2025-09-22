from typing import List, Dict
from src.dao.order_dao import OrderDAO
from src.dao.customer_dao import CustomerDAO

class OrderError(Exception): pass

class OrderService:
    def __init__(self):
        self.repo = OrderDAO()
        self.customer_repo = CustomerDAO()

    def create(self, cust_id: int, items: List[Dict]) -> Dict:
        if not self.customer_repo.get_by_id(cust_id):
            raise OrderError("Customer not found")
        return self.repo.create(cust_id, items, total_amount=sum(
            self.repo.db.table("products").select("price").eq("prod_id", item["prod_id"]).execute().data[0]["price"] * item["quantity"]
            for item in items
        ))

    def cancel_order(self, order_id: int) -> Dict:
        return self.repo.cancel(order_id)

    def get_order_details(self, order_id: int) -> Dict:
        order = self.repo.get_by_id(order_id)
        if not order: return {}
        items = self.repo.db.table("order_items").select("*").eq("order_id", order_id).execute().data
        order["items"] = items
        return order
