from typing import Optional, Dict
from src.config import SupabaseConfig

class PaymentDAO:
    def __init__(self):
        self.db = SupabaseConfig.get_client()

    def create(self, order_id: int, amount: float) -> Dict:
        self.db.table("payments").insert({"order_id": order_id, "amount": amount, "status": "PENDING"}).execute()
        return self.get_by_order(order_id)

    def mark_paid(self, payment_id: int, method: str) -> Dict:
        self.db.table("payments").update({"status": "PAID", "method": method, "paid_at": "now()"}).eq("payment_id", payment_id).execute()
        resp = self.db.table("payments").select("*").eq("payment_id", payment_id).limit(1).execute()
        return resp.data[0]

    def mark_refunded(self, payment_id: int) -> Dict:
        self.db.table("payments").update({"status": "REFUNDED"}).eq("payment_id", payment_id).execute()
        resp = self.db.table("payments").select("*").eq("payment_id", payment_id).limit(1).execute()
        return resp.data[0]

    def get_by_order(self, order_id: int) -> Optional[Dict]:
        resp = self.db.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None
