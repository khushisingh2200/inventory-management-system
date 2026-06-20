# Inventory Management System

A relational database system built with SQLite and Python, featuring 5 linked tables, 8 business SQL queries, and an interactive Streamlit dashboard for inventory tracking and supplier management.

---

## What This Project Does

1. Designs a relational database with 5 linked tables using foreign keys
2. Populates realistic business data — products, suppliers, customers, orders, sales
3. Runs 8 business SQL queries to answer real operational questions
4. Presents findings in an interactive Streamlit dashboard with KPI metrics

---

## Database Structure

    suppliers ──→ products ──→ orders
                      ↓
                  sales ──→ customers

**5 Tables:**
- suppliers — supplier details and contact information
- products — product catalogue with stock levels and reorder points
- customers — customer details by country
- orders — purchase orders from suppliers
- sales — customer sales transactions

---

## Project Structure

    inventory-management-system/
    ├── create_db.py
    ├── queries.py
    ├── app.py
    ├── requirements.txt
    └── README.md

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| SQLite | Relational database |
| pandas | Data processing |
| Streamlit | Interactive dashboard |
| Plotly | Charts and visualisations |

---

## SQL Concepts Demonstrated

- JOIN across multiple tables
- FOREIGN KEY constraints for data integrity
- GROUP BY with SUM and COUNT
- CASE WHEN inside SUM for conditional aggregation
- strftime for monthly trend analysis
- WHERE with comparison operators for stock alerts

---

## Business Queries Included

| Query | Business Question |
|-------|------------------|
| Products with Supplier Details | Which supplier provides each product? |
| Low Stock Alert | Which products need reordering now? |
| Revenue by Product | Which products generate most revenue? |
| Top Customers | Who are the highest spending customers? |
| Pending Orders | Which orders are still outstanding? |
| Revenue by Category | Which product category performs best? |
| Supplier Performance | Which suppliers have delivery issues? |
| Monthly Sales Trend | How is revenue trending month on month? |

---

## How to Run

**Step 1 — Install dependencies:**
```bash
pip install -r requirements.txt
```

**Step 2 — Create database:**
```bash
python create_db.py
```

**Step 3 — Run queries:**
```bash
python queries.py
```

**Step 4 — Launch dashboard:**
```bash
streamlit run app.py
```

---

## Dashboard Features

- 4 KPI metrics — total products, suppliers, revenue, low stock count
- Low stock alert table with supplier contact details
- Revenue by product category bar chart
- Top customers by spending
- Supplier delivery performance comparison
- Monthly revenue trend line chart
- Full product inventory table with stock status