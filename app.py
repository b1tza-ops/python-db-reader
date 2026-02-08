"""
CLI application layer.
Handles user input, menu flow, and output formatting.
"""

from db import get_shoppers, get_shopper_by_id, search_shoppers


def prompt_int(message: str, default: int | None = None) -> int:
    while True:
        raw = input(message).strip()
        if raw == "" and default is not None:
            return default
        try:
            value = int(raw)
            if value < 1:
                print("Please enter a number >= 1.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def print_shopper_list(rows):
    if not rows:
        print("\nNo results found.\n")
        return

    print("\nResults:")
    for r in rows:
        name = f"{r.get('shopper_first_name', '')} {r.get('shopper_surname', '')}".strip()
        email = r.get("shopper_email_address", "")
        joined = r.get("date_joined", "")
        print(f"- #{r['shopper_id']:>5} | {name:<22} | {email:<28} | {joined}")
    print("")


def print_shopper_details(s):
    print("\nShopper details:")
    print(f"ID:            {s['shopper_id']}")
    print(f"Account ref:   {s['shopper_account_ref']}")
    print(f"Name:          {s['shopper_first_name']} {s['shopper_surname']}")
    print(f"Email:         {s['shopper_email_address']}")
    print(f"Date of birth: {s['date_of_birth']}")
    print(f"Gender:        {s['gender']}")
    print(f"Date joined:   {s['date_joined']}\n")


def print_order_history(orders, items_by_order, total_by_order):
    if not orders:
        print("\nNo orders found for this shopper.\n")
        return

    print("")
    for o in orders:
        oid = o["order_id"]
        print(f"Order #{oid} | Date: {o['order_date']} | Status: {o['order_status']}")

        items = items_by_order.get(oid, [])
        if not items:
            print("  (No items found)\n")
            continue

        for it in items:
            name = it.get("product_description", "Unknown product")
            maker = it.get("product_manufacturer") or ""
            model = it.get("product_model") or ""
            seller = it.get("seller_name") or "Unknown seller"
            qty = it.get("quantity", 0)
            price = float(it.get("price", 0) or 0)
            line_total = qty * price

            extra = " ".join(x for x in [maker, model] if x).strip()
            if extra:
                extra = f" ({extra})"

            print(f"  - {name}{extra}")
            print(f"    Seller: {seller} | Qty: {qty} | Unit: £{price:.2f} | Line: £{line_total:.2f}")

        print(f"  Order total: £{float(total_by_order.get(oid, 0) or 0):.2f}\n")


def olist_menu():
    """
    Olist dataset menu (Phase 2).
    Requires db_olist.py in the project root.
    """
    while True:
        print("\n=== Olist DB Reader ===")
        print("1) List customers")
        print("2) Search customers (city/state)")
        print("3) Order history by customer_unique_id (with items)")
        print("4) Back")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            from db_olist import get_customers

            limit = prompt_int("How many customers? (default 10): ", default=10)
            customers = get_customers(limit=limit)

            print("")
            for c in customers:
                print(f"{c['customer_id']} | {c['customer_city']} | {c['customer_state']}")
            print("")

        elif choice == "2":
            from db_olist import search_customers

            city = input("City (blank for any): ").strip()
            state = input("State (blank for any, e.g. SP): ").strip()
            limit = prompt_int("Max results? (default 50): ", default=50)

            rows = search_customers(city=city, state=state, limit=limit)
            if not rows:
                print("\nNo customers found.\n")
                continue

            print("")
            for c in rows:
                print(f"{c['customer_id']} | {c['customer_unique_id']} | {c['customer_city']} | {c['customer_state']}")
            print("")

        elif choice == "3":
            from db_olist import get_orders_by_customer_unique_id, get_order_items

            cuid = input("Enter customer_unique_id: ").strip()
            limit = prompt_int("How many orders to show? (default 5): ", default=5)

            orders = get_orders_by_customer_unique_id(cuid, limit=limit)
            if not orders:
                print("\nNo orders found.\n")
                continue

            print("")
            for o in orders:
                print(f"Order {o['order_id']} | {o['order_status']} | {o['order_purchase_timestamp']}")
                items = get_order_items(o["order_id"])

                if not items:
                    print("  (No items found)")
                else:
                    for it in items[:15]:
                        cat = it.get("product_category_name") or "unknown_category"
                        price = float(it.get("price", 0) or 0)
                        freight = float(it.get("freight_value", 0) or 0)
                        print(f"  - {cat} | Price: {price:.2f} | Freight: {freight:.2f}")

                total_price = sum(float(i.get("price", 0) or 0) for i in items)
                total_freight = sum(float(i.get("freight_value", 0) or 0) for i in items)
                print(f"  Totals: Items £{total_price:.2f} | Freight £{total_freight:.2f}\n")

        elif choice == "4":
            break

        else:
            print("\nInvalid option. Choose 1-4.\n")


def menu():
    while True:
        print("=== Parana DB Reader ===")
        print("1) List shoppers")
        print("2) Search shoppers (name/email)")
        print("3) View shopper by ID")
        print("4) Show DB schema (tables/columns)")
        print("5) Show shopper order history")
        print("6) Olist (big dataset) menu")
        print("7) Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            limit = prompt_int("How many shoppers? (default 10): ", default=10)
            rows = get_shoppers(limit=limit)
            print_shopper_list(rows)

        elif choice == "2":
            keyword = input("Search keyword (name/email): ").strip()
            if not keyword:
                print("Keyword cannot be empty.\n")
                continue
            limit = prompt_int("Max results? (default 20): ", default=20)
            rows = search_shoppers(keyword, limit=limit)
            print_shopper_list(rows)

        elif choice == "3":
            sid = prompt_int("Enter shopper ID: ")
            shopper = get_shopper_by_id(sid)
            if not shopper:
                print(f"\nNo shopper found with ID {sid}.\n")
                continue
            print_shopper_details(shopper)

        elif choice == "4":
            from db import list_tables, describe_table

            tables = list_tables()
            print("\nDatabase tables:")
            for t in tables:
                print(f"- {t}")

            print("\nTable schemas:")
            for t in tables:
                print(f"== {t} ==")
                cols = describe_table(t)
                for c in cols:
                    print(f"  - {c['name']} ({c['type']})")
                print("")

        elif choice == "5":
            from db import get_shopper_orders, get_order_items, calculate_order_total

            sid = prompt_int("Enter shopper ID: ")
            limit = prompt_int("How many orders to show? (default 10): ", default=10)

            orders = get_shopper_orders(shopper_id=sid, limit=limit)

            items_by_order = {}
            total_by_order = {}

            for o in orders:
                oid = o["order_id"]
                items_by_order[oid] = get_order_items(oid)
                total_by_order[oid] = calculate_order_total(oid)

            print_order_history(orders, items_by_order, total_by_order)

        elif choice == "6":
            olist_menu()

        elif choice == "7":
            print("\nThank you!\n")
            break

        else:
            print("\nInvalid option. Choose 1-7.\n")


if __name__ == "__main__":
    menu()
x