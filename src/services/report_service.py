from typing import List, Dict
from src.config import SupabaseConfig
from datetime import datetime, timedelta


class ReportService:
    """Generate sales and customer reports."""

    def __init__(self):
        self.sb = SupabaseConfig.get_client()

    def top_selling_products(self, limit: int = 5) -> List[Dict]:
        """
        Return top-selling products by total quantity sold.
        """
        resp = (
            self.sb.table("order_items")
            .select("prod_id, quantity, products(name)")
            .order("quantity", desc=True)
            .limit(limit)
            .execute()
        )
        return resp.data or []

    def total_revenue_last_month(self) -> float:
        """
        Return total revenue from orders completed in the last month.
        """
        today = datetime.utcnow()
        last_month_start = datetime(today.year, today.month - 1 if today.month > 1 else 12, 1)
        last_month_end = datetime(today.year, today.month, 1) - timedelta(seconds=1)

        resp = (
            self.sb.table("orders")
            .select("total_amount")
            .gte("order_date", last_month_start.isoformat())
            .lte("order_date", last_month_end.isoformat())
            .execute()
        )
        total = sum(o.get("total_amount", 0) for o in resp.data or [])
        return total

    def total_orders_per_customer(self) -> List[Dict]:
        """
        Return total orders placed by each customer.
        """
        # Supabase doesn’t support SQL aggregation directly via JS client; use RPC or Python aggregation
        resp = self.sb.table("orders").select("cust_id").execute()
        counts = {}
        for order in resp.data or []:
            cust = order["cust_id"]
            counts[cust] = counts.get(cust, 0) + 1
        return [{"cust_id": k, "total_orders": v} for k, v in counts.items()]

    def customers_with_multiple_orders(self, min_orders: int = 3) -> List[Dict]:
        """
        Return customers who placed more than `min_orders`.
        """
        all_counts = self.total_orders_per_customer()
        return [c for c in all_counts if c["total_orders"] >= min_orders]
