from typing import Optional, Dict, List
from src.config import SupabaseConfig

class OrderDAO:
    def __init__(self):
        self.db = SupabaseConfig.get_client()

    def create(self, cust_id: int, items: List[Dict], total_amount: float) -> Dict:
        payload = {"cust_id": cust_id, "status": "PLACED", "total_amount": total_amount}
        self.db.table("orders").insert(payload).execute()
        resp = self.db.table("orders").select("*").order("order_id", desc=True).limit(1).execute()
        order = resp.data[0]

        for item in items:
            product_id = item["prod_id"]
            qty = item["quantity"]
            price_resp = self.db.table("products").select("price").eq("prod_id", product_id).limit(1).execute()
            price = price_resp.data[0]["price"]
            self.db.table("order_items").insert({
                "order_id": order["order_id"],
                "prod_id": product_id,
                "quantity": qty,
                "price": price
            }).execute()
            # Deduct stock
            self.db.table("products").update({"stock": self.db.table("products").select("stock").eq("prod_id", product_id).execute().data[0]["stock"] - qty}).eq("prod_id", product_id).execute()

        return order

    def get_by_id(self, order_id: int) -> Optional[Dict]:
        resp = self.db.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def cancel(self, order_id: int) -> Dict:
        existing = self.get_by_id(order_id)
        if not existing or existing["status"] != "PLACED":
            raise ValueError("Only PLACED orders can be cancelled")
        # restore stock
        items = self.db.table("order_items").select("*").eq("order_id", order_id).execute().data
        for item in items:
            self.db.table("products").update({
                "stock": self.db.table("products").select("stock").eq("prod_id", item["prod_id"]).execute().data[0]["stock"] + item["quantity"]
            }).eq("prod_id", item["prod_id"]).execute()
        # update status
        self.db.table("orders").update({"status": "CANCELLED"}).eq("order_id", order_id).execute()
        return self.get_by_id(order_id)
