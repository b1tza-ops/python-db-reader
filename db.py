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
