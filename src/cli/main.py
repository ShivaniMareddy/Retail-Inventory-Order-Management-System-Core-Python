'''import argparse
import json
from src.services import product_service, order_service
from src.dao import product_dao, customer_dao
 
def cmd_product_add(args):
    try:
        p = product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_product_list(args):
    ps = product_dao.list_products(limit=100)
    print(json.dumps(ps, indent=2, default=str))
 
def cmd_customer_add(args):
    try:
        c = customer_dao.create_customer(args.name, args.email, args.phone, args.city)
        print("Created customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_order_create(args):
    # items provided as prod_id:qty strings
    items = []
    for item in args.item:
        try:
            pid, qty = item.split(":")
            items.append({"prod_id": int(pid), "quantity": int(qty)})
        except Exception:
            print("Invalid item format:", item)
            return
    try:
        ord = order_service.create_order(args.customer, items)
        print("Order created:")
        print(json.dumps(ord, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_order_show(args):
    try:
        o = order_service.get_order_details(args.order)
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_order_cancel(args):
    try:
        o = order_service.cancel_order(args.order)
        print("Order cancelled (updated):")
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")
 
    # product add/list
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)
 
    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)
 
    # customer add
    pcust = sub.add_parser("customer")
    pcust_sub = pcust.add_subparsers(dest="action")
    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)
 
    # order
    porder = sub.add_parser("order")
    porder_sub = porder.add_subparsers(dest="action")
 
    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
    createo.set_defaults(func=cmd_order_create)
 
    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)
 
    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)
 
    return parser
 
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)
 
if __name__ == "__main__":
    main()
 '''
import argparse
import json
from src.services.product_service import ProductService
from src.services.customer_service import CustomerService
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService
from src.services.report_service import ReportService

# Services
product_service = ProductService()
customer_service = CustomerService()
order_service = OrderService()
payment_service = PaymentService()
report_service = ReportService()

# --------------------- Product Handlers --------------------- #
def cmd_product_add(args):
    try:
        p = product_service.add(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:", json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_list(args):
    try:
        products = product_service.list()
        print(json.dumps(products, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_update(args):
    try:
        fields = {k:v for k,v in vars(args).items() if k in ["name","sku","price","stock","category"] and v is not None}
        updated = product_service.update(args.id, **fields)
        print("Updated product:", json.dumps(updated, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_delete(args):
    try:
        deleted = product_service.delete(args.id)
        print("Deleted product:", json.dumps(deleted, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# --------------------- Customer Handlers --------------------- #
def cmd_customer_add(args):
    try:
        c = customer_service.add(args.name, args.email, args.phone, args.city)
        print("Created customer:", json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_list(args):
    try:
        customers = customer_service.list()
        print(json.dumps(customers, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_update(args):
    try:
        fields = {k:v for k,v in vars(args).items() if k in ["name","email","phone","city"] and v is not None}
        updated = customer_service.update(args.id, **fields)
        print("Updated customer:", json.dumps(updated, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_delete(args):
    try:
        deleted = customer_service.delete(args.id)
        print("Deleted customer:", json.dumps(deleted, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# --------------------- Order Handlers --------------------- #
def cmd_order_create(args):
    try:
        items = [{"prod_id": int(i.split(":")[0]), "quantity": int(i.split(":")[1])} for i in args.item]
        o = order_service.create_order(args.customer, items)
        print("Order created:", json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_list(args):
    try:
        orders = order_service.list_orders(args.customer)
        print(json.dumps(orders, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_cancel(args):
    try:
        o = order_service.cancel_order(args.order)
        print("Order cancelled:", json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# --------------------- Payment Handlers --------------------- #
def cmd_payment_process(args):
    try:
        p = payment_service.process_payment(args.order, args.method)
        print("Payment processed:", json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_payment_refund(args):
    try:
        p = payment_service.refund(args.order)
        print("Payment refunded:", json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# --------------------- Reporting Handlers --------------------- #
def cmd_report_top_products(args):
    data = report_service.top_selling_products()
    print("Top Selling Products:", json.dumps(data, indent=2, default=str))

def cmd_report_total_revenue(args):
    revenue = report_service.total_revenue_last_month()
    print(f"Total revenue last month: {revenue}")

def cmd_report_orders_per_customer(args):
    data = report_service.total_orders_per_customer()
    print("Total orders per customer:", json.dumps(data, indent=2, default=str))

def cmd_report_customers_multi_orders(args):
    data = report_service.customers_with_multiple_orders()
    print("Customers with more than 2 orders:", json.dumps(data, indent=2, default=str))

# --------------------- Parser Setup --------------------- #
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # Products
    p_prod = sub.add_parser("product")
    prod_sub = p_prod.add_subparsers(dest="action")
    addp = prod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category")
    addp.set_defaults(func=cmd_product_add)

    listp = prod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)

    updatep = prod_sub.add_parser("update")
    updatep.add_argument("--id", type=int, required=True)
    updatep.add_argument("--name")
    updatep.add_argument("--sku")
    updatep.add_argument("--price", type=float)
    updatep.add_argument("--stock", type=int)
    updatep.add_argument("--category")
    updatep.set_defaults(func=cmd_product_update)

    deletep = prod_sub.add_parser("delete")
    deletep.add_argument("--id", type=int, required=True)
    deletep.set_defaults(func=cmd_product_delete)

    # Customers
    p_cust = sub.add_parser("customer")
    cust_sub = p_cust.add_subparsers(dest="action")
    addc = cust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city")
    addc.set_defaults(func=cmd_customer_add)

    listc = cust_sub.add_parser("list")
    listc.set_defaults(func=cmd_customer_list)

    updatec = cust_sub.add_parser("update")
    updatec.add_argument("--id", type=int, required=True)
    updatec.add_argument("--name")
    updatec.add_argument("--email")
    updatec.add_argument("--phone")
    updatec.add_argument("--city")
    updatec.set_defaults(func=cmd_customer_update)

    deletec = cust_sub.add_parser("delete")
    deletec.add_argument("--id", type=int, required=True)
    deletec.set_defaults(func=cmd_customer_delete)

    # Orders
    p_order = sub.add_parser("order")
    order_sub = p_order.add_subparsers(dest="action")
    createo = order_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty")
    createo.set_defaults(func=cmd_order_create)

    listo = order_sub.add_parser("list")
    listo.add_argument("--customer", type=int, required=True)
    listo.set_defaults(func=cmd_order_list)

    canco = order_sub.add_parser("cancel")
    canco.add_argument("--order", type=int, required=True)
    canco.set_defaults(func=cmd_order_cancel)

    # Payments
    p_pay = sub.add_parser("payment")
    pay_sub = p_pay.add_subparsers(dest="action")
    processp = pay_sub.add_parser("process")
    processp.add_argument("--order", type=int, required=True)
    processp.add_argument("--method", required=True)
    processp.set_defaults(func=cmd_payment_process)

    refundp = pay_sub.add_parser("refund")
    refundp.add_argument("--order", type=int, required=True)
    refundp.set_defaults(func=cmd_payment_refund)

    # Reports
    p_report = sub.add_parser("report")
    report_sub = p_report.add_subparsers(dest="action")
    top_prod = report_sub.add_parser("top-products")
    top_prod.set_defaults(func=cmd_report_top_products)
    revenue = report_sub.add_parser("revenue-last-month")
    revenue.set_defaults(func=cmd_report_total_revenue)
    orders_cust = report_sub.add_parser("orders-per-customer")
    orders_cust.set_defaults(func=cmd_report_orders_per_customer)
    multi_orders = report_sub.add_parser("customers-multi-orders")
    multi_orders.set_defaults(func=cmd_report_customers_multi_orders)

    return parser

# --------------------- Main --------------------- #
def main():
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

