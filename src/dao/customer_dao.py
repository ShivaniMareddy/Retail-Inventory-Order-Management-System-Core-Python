from typing import Optional, Dict, List
from src.config import SupabaseConfig

class CustomerDAO:
    def __init__(self):
        self.db = SupabaseConfig.get_client()

    def create(self, name: str, email: str, phone: str, city: str | None = None) -> Dict:
        payload = {"name": name, "email": email, "phone": phone}
        if city: payload["city"] = city
        self.db.table("customers").insert(payload).execute()
        resp = self.db.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else {}

    def get_by_id(self, cust_id: int) -> Optional[Dict]:
        resp = self.db.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list(self, limit: int = 100) -> List[Dict]:
        resp = self.db.table("customers").select("*").order("cust_id").limit(limit).execute()
        return resp.data or []

    def update(self, cust_id: int, fields: Dict) -> Optional[Dict]:
        self.db.table("customers").update(fields).eq("cust_id", cust_id).execute()
        resp = self.db.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete(self, cust_id: int) -> Optional[Dict]:
        before = self.db.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        row = before.data[0] if before.data else None
        self.db.table("customers").delete().eq("cust_id", cust_id).execute()
        return row
