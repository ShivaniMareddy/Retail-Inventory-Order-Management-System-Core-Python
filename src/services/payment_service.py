from src.dao.payment_dao import PaymentDAO
from src.dao.order_dao import OrderDAO

class PaymentError(Exception): pass

class PaymentService:
    def __init__(self):
        self.repo = PaymentDAO()
        self.order_repo = OrderDAO()

    def process_payment(self, order_id: int, method: str):
        payment = self.repo.get_by_order(order_id)
        if not payment:
            # Create payment if missing
            order = self.order_repo.get_by_id(order_id)
            if not order:
                raise PaymentError("Order not found")
            payment = self.repo.create(order_id, order["total_amount"])
        if payment["status"] != "PENDING":
            raise PaymentError("Payment already processed")
        self.repo.mark_paid(payment["payment_id"], method)
        # Mark order completed
        self.order_repo.db.table("orders").update({"status": "COMPLETED"}).eq("order_id", order_id).execute()
        return self.repo.get_by_order(order_id)

    def refund(self, order_id: int):
        payment = self.repo.get_by_order(order_id)
        if not payment or payment["status"] != "PAID":
            raise PaymentError("Only PAID payments can be refunded")
        self.repo.mark_refunded(payment["payment_id"])
        # Cancel order
        self.order_repo.cancel(order_id)
        return self.repo.get_by_order(order_id)
