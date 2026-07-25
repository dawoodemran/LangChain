from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "SalesDB" / "sales.db"

SEED_ORDERS = [
    ("John Doe", "Laptop", 1, 1000.00, 1000.00),
    ("Jane Smith", "Smartphone", 2, 500.00, 1000.00),
    ("Bob Johnson", "Tablet", 3, 200.00, 600.00),
]


def init_db() -> Path:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL
            )
            """
        )

        cursor.execute("SELECT COUNT(*) FROM orders")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
                INSERT INTO orders (customer_name, product_name, quantity, price, total)
                VALUES (?, ?, ?, ?, ?)
                """,
                SEED_ORDERS,
            )
        conn.commit()

    return DB_PATH


if __name__ == "__main__":
    database_path = init_db()
    print(f"Database ready at {database_path}")
