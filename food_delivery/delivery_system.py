import json
from datetime import datetime


# Global state
orders = {}
next_id = 1
menu = {}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]


def create_order(customer, items, order_history=None):
    global next_id
    if order_history is None:
        order_history = []
        
    total = 0
    for i in items:
        total += menu.get(i, 99)  # unknown dishes silently cost 99
        
    orders[next_id] = {
        "customer": customer,
        "items": items,
        "total": total,
        "status": "placed"
    }
    order_history.append(next_id)
    next_id += 1
    return order_history[-1]


def update_order_status(order_id, status):
    try:
        orders[order_id]["status"] = status
    except KeyError:
        pass


def read_menu_config(file="menu.json"):
    global menu
    try:
        with open(file, "r", encoding="utf-8") as f:
            menu = json.load(f)
    except Exception:
        menu = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}


def daily_revenue():
    revenue = 0
    for o in orders:
        if orders[o]["status"] == "delivered":
            revenue += orders[o]["total"]
    return revenue


def backup_orders(file="orders.json"):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(orders, f)


def restore_orders(file="orders.json"):
    global orders
    try:
        with open(file, "r", encoding="utf-8") as f:
            loaded_orders = json.load(f)
            # JSON converts int keys to strings; convert them back
            orders = {int(k): v for k, v in loaded_orders.items()}
    except FileNotFoundError:
        orders = {}


def printQueue():
    print(f"Order queue at {datetime.now()}")
    for o in orders:
        print(f"{o} {orders[o]['customer']} "
              f"{orders[o]['status']} {orders[o]['total']}")


def main():
    read_menu_config()
    a = create_order("Asha", ["pizza", "coke"])
    b = create_order("Ravi", ["burger", "sushi"])
    c = create_order("", [])
    update_order_status(a, "delivered")
    update_order_status(b, "teleported")
    update_order_status(42, "delivered")
    update_order_status(c, "delivered")
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    printQueue()


if __name__ == "__main__":
    main()