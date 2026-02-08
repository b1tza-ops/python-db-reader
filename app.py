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
        print(f"- #{r['shopper_id']:>4} | {name:<22} | {email:<28} | {joined}")
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
        oid = o['order_id']
        print(f"Order #{oid} | Date: {o['order_date']} | Status: {o['order_status']})")
        items = items_by_order.get(oid, [])
        if not items:
            print("  (No items found)\n")
            continue

        for it in items:
            name = it["product_description"]
            maker = it["product_manufacturer"] or ""
            model = it["product_model"] or ""
            seller = it["seller_name"] or "Unknown seller"
            qty = it["quantity"]
            price = it["price"]
            line_total = qty * price

            extra = " ".join(x for x in [maker, model] if x).strip()
            if extra:
                extra = f" ({extra})"
            
            print(f' -{name}{extra}')
            print(f'   Seller: {seller} | Qty {qty} | Unit £{price:.2f} |  Line: £{line_total:.2f}')

    print (f" Order total : £{total_by_order.get(oid, 0):.2f}\n")     

def menu():
    while True:
        print("=== Parana DB Reader ===")
        print("1) List shoppers")
        print("2) Search shoppers (name/email)")
        print("3) View shopper by ID")
        print("4) Show DB schema (tables/columns)")
        print("5) Show shopper order histoy")
        print("6) Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            limit = prompt_int("How many shoppers? (default 10): ", default=10)
            rows = get_shoppers(limit=limit)
            # list view uses fewer columns, so we format it as a list
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
            print("\nThank you!\n")
            break

        else:
            print("\nInvalid option. Choose 1-4.\n")


if __name__ == "__main__":
    menu()
