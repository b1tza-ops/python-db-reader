import sqlite3

from pathlib import Path

DB_PATH = Path("data/olist.db")

def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at: {DB_PATH.resolve()}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_customers(limit: int = 20):
    query = """
        SELECT
            customer_id,
            customer_unique_id,
            customer_zip_code_prefix,
            customer_city,
            customer_state
        FROM olist_customers
        LIMIT ?
    """
    with get_connection() as conn:
        rows = conn.execute(query, (limit,)).fetchall()
        return [dict(r) for r in rows]
    
def get_customer_orders(customer_id: str, limit: int = 20):
    query = """
        SELECT
            order_id,
            customer_id,
            order_status,
            order_purchase_timestamp
        FROM olist_orders
        WHERE customer_id = ?
        ORDER BY order_purchase_timestamp DESC
        LIMIT ?
    """
    with get_connection() as conn:
        rows = conn.execute(query, (customer_id, limit)).fetchall()
        return [dict(r) for r in rows]
    
def get_order_items(order_id: str):
    query = """
        SELECT
            oi.product_id,
            oi.price,
            oi.freight_value,
            p.product_category_name,
            p.product_photos_qty
        FROM olist_order_items oi
        JOIN olist_products p ON oi.product_id = p.product_id
        WHERE oi.order_id = ?
    """
    with get_connection() as conn:
        rows = conn.execute(query, (order_id,)).fetchall()
        return [dict(r) for r in rows]

def search_customers(city: str = "", state: str ="", limit: int = 50):
    query= """
        SELECT
            customer_id,
            customer_unique_id,
            customer_city,
            customer_state
        FROM olist_customers
        WHERE
            (? = '' OR LOWER(customer_city) LIKE '%' || LOWER(?) || '%')
            AND (? = '' OR UPPER(customer_state) = UPPER(?))
            LIMIT ?
        """
    with get_connection() as conn:
        rows = conn.execute(query, (city, city, state, state, limit)).fetchall()
        return [dict(r) for r in rows]

def get_orders_by_customer_unique_id(unique_id: str, limit: int = 20):
    query = """
        SELECT
            o.order_id,
            o.customer_id,
            o.order_status,
            o.order_purchase_timestamp
        FROM olist_orders o
        JOIN olist_customers c ON o.customer_id = c.customer_id
        WHERE c.customer_unique_id = ?
        ORDER BY o.order_purchase_timestamp DESC
        LIMIT ?
    """
    with get_connection() as conn:
        rows = conn.execute(query, (unique_id, limit)).fetchall()
        return [dict(r) for r in rows]