import sqlite3

# ── Connect ──
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# ── Drop tables if they exist ──
cursor.executescript("""
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS suppliers;
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS sales;
""")

# ── Create tables ──
cursor.executescript("""
    CREATE TABLE suppliers (
        supplier_id   INTEGER PRIMARY KEY,
        supplier_name TEXT NOT NULL,
        contact       TEXT,
        country       TEXT,
        email         TEXT
    );

    CREATE TABLE products (
        product_id     INTEGER PRIMARY KEY,
        product_name   TEXT NOT NULL,
        category       TEXT,
        price          REAL,
        stock_quantity INTEGER,
        reorder_level  INTEGER,
        supplier_id    INTEGER,
        FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    );

    CREATE TABLE customers (
        customer_id   INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        city          TEXT,
        country       TEXT,
        email         TEXT
    );

    CREATE TABLE orders (
        order_id    INTEGER PRIMARY KEY,
        product_id  INTEGER,
        supplier_id INTEGER,
        quantity    INTEGER,
        order_date  TEXT,
        status      TEXT,
        FOREIGN KEY (product_id)  REFERENCES products(product_id),
        FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    );

    CREATE TABLE sales (
        sale_id     INTEGER PRIMARY KEY,
        product_id  INTEGER,
        customer_id INTEGER,
        quantity    INTEGER,
        sale_date   TEXT,
        total_amount REAL,
        FOREIGN KEY (product_id)  REFERENCES products(product_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
""")

# ── Insert suppliers ──
cursor.executemany("""
    INSERT INTO suppliers VALUES (?,?,?,?,?)
""", [
    (1, "TechSupply GmbH",     "+49 30 1234567",  "Germany", "contact@techsupply.de"),
    (2, "ElectroHub Ltd",      "+44 20 9876543",  "UK",      "info@electrohub.co.uk"),
    (3, "GlobalParts Inc",     "+1 415 5551234",  "USA",     "sales@globalparts.com"),
    (4, "AsiaComponents Co",   "+86 21 8765432",  "China",   "export@asiacomp.cn"),
    (5, "EuroTech Solutions",  "+33 1 23456789",  "France",  "hello@eurotech.fr"),
])

# ── Insert products ──
cursor.executemany("""
    INSERT INTO products VALUES (?,?,?,?,?,?,?)
""", [
    (1,  "Laptop Pro 15",       "Electronics",  1299.99, 45,  10, 1),
    (2,  "Wireless Mouse",      "Accessories",    29.99, 150, 30, 2),
    (3,  "USB-C Hub",           "Accessories",    49.99,  8,  20, 3),
    (4,  "Monitor 27inch",      "Electronics",   399.99, 25,  10, 1),
    (5,  "Mechanical Keyboard", "Accessories",    89.99, 60,  15, 2),
    (6,  "Webcam HD",           "Electronics",    79.99,  5,  10, 4),
    (7,  "Desk Lamp LED",       "Office",         34.99, 80,  20, 5),
    (8,  "Notebook A4",         "Stationery",      4.99, 200, 50, 5),
    (9,  "Headphones Pro",      "Electronics",   199.99, 30,  10, 3),
    (10, "Standing Desk",       "Furniture",     499.99,  3,   5, 4),
])

# ── Insert customers ──
cursor.executemany("""
    INSERT INTO customers VALUES (?,?,?,?,?)
""", [
    (1, "Mueller GmbH",        "Berlin",    "Germany", "orders@mueller.de"),
    (2, "Schmidt & Co",        "Munich",    "Germany", "buy@schmidt.de"),
    (3, "Alpine Solutions",    "Vienna",    "Austria", "info@alpine.at"),
    (4, "TechStart Paris",     "Paris",     "France",  "tech@techstart.fr"),
    (5, "Nordic Systems",      "Stockholm", "Sweden",  "orders@nordic.se"),
])

# ── Insert orders ──
cursor.executemany("""
    INSERT INTO orders VALUES (?,?,?,?,?,?)
""", [
    (1,  1, 1, 10, "2026-01-05", "Delivered"),
    (2,  2, 2, 50, "2026-01-10", "Delivered"),
    (3,  3, 3, 20, "2026-01-15", "Pending"),
    (4,  4, 1, 5,  "2026-02-01", "Delivered"),
    (5,  5, 2, 30, "2026-02-10", "Delivered"),
    (6,  6, 4, 15, "2026-02-20", "Pending"),
    (7,  7, 5, 40, "2026-03-01", "Delivered"),
    (8,  8, 5, 100,"2026-03-05", "Delivered"),
    (9,  9, 3, 20, "2026-03-10", "Pending"),
    (10, 10,4, 2,  "2026-03-15", "Delivered"),
])

# ── Insert sales ──
cursor.executemany("""
    INSERT INTO sales VALUES (?,?,?,?,?,?)
""", [
    (1,  1, 1, 2,  "2026-01-10", 2599.98),
    (2,  2, 2, 10, "2026-01-15",  299.90),
    (3,  4, 3, 1,  "2026-01-20",  399.99),
    (4,  5, 1, 5,  "2026-02-05",  449.95),
    (5,  9, 4, 3,  "2026-02-10",  599.97),
    (6,  7, 5, 10, "2026-02-15",  349.90),
    (7,  1, 2, 1,  "2026-03-01", 1299.99),
    (8,  3, 3, 5,  "2026-03-05",  249.95),
    (9,  6, 4, 2,  "2026-03-10",  159.98),
    (10, 8, 5, 50, "2026-03-15",  249.50),
])

conn.commit()
conn.close()
print("✓ Database created with 5 tables and sample data")
print("  Suppliers: 5 rows")
print("  Products:  10 rows")
print("  Customers: 5 rows")
print("  Orders:    10 rows")
print("  Sales:     10 rows")