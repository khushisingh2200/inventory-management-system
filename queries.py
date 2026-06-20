import sqlite3
import pandas as pd

conn = sqlite3.connect("inventory.db")

def run_query(title, query):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))
    return df

# ── Query 1: All products with supplier name (JOIN) ──
run_query("Products with Supplier Details", """
    SELECT p.product_name,
           p.category,
           p.price,
           p.stock_quantity,
           s.supplier_name,
           s.country
    FROM products p
    JOIN suppliers s ON p.supplier_id = s.supplier_id
    ORDER BY p.category
""")

# ── Query 2: Low stock alert ──
run_query("Low Stock Alert — Needs Reordering", """
    SELECT p.product_name,
           p.stock_quantity,
           p.reorder_level,
           s.supplier_name,
           s.email
    FROM products p
    JOIN suppliers s ON p.supplier_id = s.supplier_id
    WHERE p.stock_quantity <= p.reorder_level
    ORDER BY p.stock_quantity ASC
""")

# ── Query 3: Total sales by product ──
run_query("Total Revenue by Product", """
    SELECT p.product_name,
           p.category,
           COUNT(s.sale_id)    as total_orders,
           SUM(s.quantity)     as units_sold,
           SUM(s.total_amount) as total_revenue
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.product_name, p.category
    ORDER BY total_revenue DESC
""")

# ── Query 4: Top customers by spending ──
run_query("Top Customers by Total Spending", """
    SELECT c.customer_name,
           c.country,
           COUNT(s.sale_id)    as total_purchases,
           SUM(s.total_amount) as total_spent
    FROM sales s
    JOIN customers c ON s.customer_id = c.customer_id
    GROUP BY c.customer_name, c.country
    ORDER BY total_spent DESC
""")

# ── Query 5: Pending orders with details ──
run_query("Pending Orders", """
    SELECT o.order_id,
           p.product_name,
           s.supplier_name,
           o.quantity,
           o.order_date,
           o.status
    FROM orders o
    JOIN products p  ON o.product_id  = p.product_id
    JOIN suppliers s ON o.supplier_id = s.supplier_id
    WHERE o.status = 'Pending'
    ORDER BY o.order_date ASC
""")

# ── Query 6: Revenue by category ──
run_query("Revenue by Product Category", """
    SELECT p.category,
           COUNT(s.sale_id)    as total_sales,
           SUM(s.quantity)     as units_sold,
           SUM(s.total_amount) as total_revenue,
           ROUND(AVG(s.total_amount), 2) as avg_sale_value
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_revenue DESC
""")

# ── Query 7: Supplier performance ──
run_query("Supplier Order Summary", """
    SELECT s.supplier_name,
           s.country,
           COUNT(o.order_id)  as total_orders,
           SUM(o.quantity)    as total_units_ordered,
           SUM(CASE WHEN o.status = 'Delivered' THEN 1 ELSE 0 END) as delivered,
           SUM(CASE WHEN o.status = 'Pending'   THEN 1 ELSE 0 END) as pending
    FROM orders o
    JOIN suppliers s ON o.supplier_id = s.supplier_id
    GROUP BY s.supplier_name, s.country
    ORDER BY total_orders DESC
""")

# ── Query 8: Monthly sales trend ──
run_query("Monthly Sales Trend", """
    SELECT strftime('%Y-%m', sale_date) as month,
           COUNT(sale_id)               as total_sales,
           SUM(quantity)                as units_sold,
           ROUND(SUM(total_amount), 2)  as revenue
    FROM sales
    GROUP BY month
    ORDER BY month ASC
""")

conn.close()
print("\nAll queries complete")