"""
Database access layer.
Contains only SQL queries and database logic.


"""


import sqlite3
from pathlib import Path

DB_PATH = Path("data/parana.db")


def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at: {DB_PATH.resolve()}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_shoppers(limit: int = 20):
    query = """
        SELECT
            shopper_id,
            shopper_account_ref,
            shopper_first_name,
            shopper_surname,
            shopper_email_address,
            date_of_birth,
            gender,
            date_joined
        FROM shoppers
        ORDER BY date_joined DESC
        LIMIT ?
    """
    with get_connection() as conn:
        rows = conn.execute(query, (limit,)).fetchall()
        return [dict(r) for r in rows]


def get_shopper_by_id(shopper_id: int):
    query = """
        SELECT
            shopper_id,
            shopper_account_ref,
            shopper_first_name,
            shopper_surname,
            shopper_email_address,
            date_of_birth,
            gender,
            date_joined
        FROM shoppers
        WHERE shopper_id = ?
    """
    with get_connection() as conn:
        row = conn.execute(query, (shopper_id,)).fetchone()
        return dict(row) if row else None


def search_shoppers(keyword: str, limit: int = 20):
    """
    Search by first name, surname, or email (case-insensitive).
    """
    query = """
        SELECT
            shopper_id,
            shopper_first_name,
            shopper_surname,
            shopper_email_address,
            date_joined
        FROM shoppers
        WHERE
            LOWER(shopper_first_name) LIKE '%' || LOWER(?) || '%'
            OR LOWER(shopper_surname) LIKE '%' || LOWER(?) || '%'
            OR LOWER(shopper_email_address) LIKE '%' || LOWER(?) || '%'
        ORDER BY date_joined DESC
        LIMIT ?
    """
    with get_connection() as conn:
        rows = conn.execute(query, (keyword, keyword, keyword, limit)).fetchall()
        return [dict(r) for r in rows]

def list_tables():
    # Return a list of table names in the database. #
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT name FROM sqlite_master
            WHERE type= 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name""").fetchall()
        return[r['name'] for r in rows]

def describe_table(table_name: str):
    # Return a list of column names and types for the given table. #
    with get_connection() as conn:
        rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()

        return [{
            'cid': r[0],
            'name': r[1],
            'type': r[2],
            'notnull': r[3],
            'default_value': r[4],
            'pk': r[5]
        }
        for r in rows]

def get_shopper_orders(shopper_id: int, limit: int = 20):
    """ 
    Return a list of orders for a shopper, including order ID, date, total amount, and status.
    
    """
    query = """
        SELECT
            order_id,
            shopper_id,
            order_date,
            order_status
        FROM shopper_orders
        WHERE shopper_id = ?
        ORDER BY order_date DESC
        LIMIT ?
    """
    with get_connection() as conn:
        rows = conn.execute(query, (shopper_id, limit)).fetchall()
        return [dict(r) for r in rows]
    
def get_order_items(order_id: int):
    """
    Returns line items for a given order, joined with product + seller info.
    """
    query = """
        SELECT
            op.order_id,
            op.product_id,
            op.seller_id,
            op.quantity,
            op.price,
            op.ordered_product_status,

            p.product_code,
            p.product_description,
            p.product_manufacturer,
            p.product_model,

            s.seller_name,
            s.seller_email_address
        FROM ordered_products op
        JOIN products p ON p.product_id = op.product_id
        JOIN sellers s ON s.seller_id = op.seller_id
        WHERE op.order_id = ?
        ORDER BY p.product_description ASC
    """
    with get_connection() as conn:
        rows = conn.execute(query, (order_id,)).fetchall()
        return [dict(r) for r in rows]

def calculate_order_total(order_id: int) -> float:

    """ 
    Calculates total for an order using ordered_products (quantity * price).

    """
    query = """
        SELECT COALESCE(SUM(quantity * price), 0) AS total
        FROM ordered_products
        WHERE order_id = ?
    """
    with get_connection() as conn:
        row = conn.execute(query, (order_id,)).fetchone()
        return row['total'] if row and row['total'] is not None else 0.0
    

def get_customers(limit: int = 20):
    query = """
        SLERCET
            customer_id,
            customer_unique_id,
            customer_city
            customer_state
        FROM olist_customers
        LIMIT?"""
    
    with get_connection() as conn:
        rows = conn.execute(query, (limit,)).fetchall()
        return [dict(r) for r in rows]
    
def get_customers_orders(customer_id: str, limit: int =20):
    query ="""
        SELECT
            order_id,
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
        JOIN olist_products p ON p.product_id = oi.product_id
        WHERE oi.order_id = ?
    """
    with get_connection() as conn:
        rows = conn.execute(query, (order_id,)).fetchall()
        return [dict(r) for r in rows]  