import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Inventory Management System", layout="wide")
st.title("📦 Inventory Management Dashboard")
st.markdown("Real-time inventory tracking, sales analysis, and supplier management")

conn = sqlite3.connect("inventory.db")

# ── KPI Row ──
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

total_products  = pd.read_sql_query("SELECT COUNT(*) as c FROM products", conn)["c"][0]
total_suppliers = pd.read_sql_query("SELECT COUNT(*) as c FROM suppliers", conn)["c"][0]
total_revenue   = pd.read_sql_query("SELECT ROUND(SUM(total_amount),2) as c FROM sales", conn)["c"][0]
low_stock       = pd.read_sql_query("SELECT COUNT(*) as c FROM products WHERE stock_quantity <= reorder_level", conn)["c"][0]

col1.metric("Total Products",   total_products)
col2.metric("Total Suppliers",  total_suppliers)
col3.metric("Total Revenue",    f"€{total_revenue:,.2f}")
col4.metric("⚠️ Low Stock Items", low_stock)

st.markdown("---")

# ── Row 1: Low Stock Alert + Revenue by Category ──
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⚠️ Low Stock Alert")
    low_stock_df = pd.read_sql_query("""
        SELECT p.product_name, p.stock_quantity, p.reorder_level,
               s.supplier_name, s.email
        FROM products p
        JOIN suppliers s ON p.supplier_id = s.supplier_id
        WHERE p.stock_quantity <= p.reorder_level
        ORDER BY p.stock_quantity ASC
    """, conn)
    st.dataframe(low_stock_df, use_container_width=True)

with col_right:
    st.subheader("Revenue by Category")
    revenue_df = pd.read_sql_query("""
        SELECT p.category,
               ROUND(SUM(s.total_amount), 2) as total_revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """, conn)
    fig1 = px.bar(revenue_df, x="category", y="total_revenue",
                  color="total_revenue", color_continuous_scale="Blues",
                  title="Revenue by Product Category")
    st.plotly_chart(fig1, use_container_width=True)

# ── Row 2: Top Customers + Supplier Performance ──
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Top Customers by Spending")
    customers_df = pd.read_sql_query("""
        SELECT c.customer_name, c.country,
               ROUND(SUM(s.total_amount), 2) as total_spent
        FROM sales s
        JOIN customers c ON s.customer_id = c.customer_id
        GROUP BY c.customer_name, c.country
        ORDER BY total_spent DESC
    """, conn)
    fig2 = px.bar(customers_df, x="customer_name", y="total_spent",
                  color="total_spent", color_continuous_scale="Teal",
                  title="Top Customers by Revenue")
    st.plotly_chart(fig2, use_container_width=True)

with col_right2:
    st.subheader("Supplier Delivery Performance")
    supplier_df = pd.read_sql_query("""
        SELECT s.supplier_name,
               SUM(CASE WHEN o.status = 'Delivered' THEN 1 ELSE 0 END) as delivered,
               SUM(CASE WHEN o.status = 'Pending'   THEN 1 ELSE 0 END) as pending
        FROM orders o
        JOIN suppliers s ON o.supplier_id = s.supplier_id
        GROUP BY s.supplier_name
    """, conn)
    fig3 = px.bar(supplier_df, x="supplier_name",
                  y=["delivered", "pending"],
                  barmode="group",
                  title="Delivered vs Pending Orders by Supplier",
                  color_discrete_map={"delivered": "#1F4E79", "pending": "#FF6B6B"})
    fig3.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig3, use_container_width=True)

# ── Row 3: Monthly Revenue Trend ──
st.subheader("Monthly Revenue Trend")
monthly_df = pd.read_sql_query("""
    SELECT strftime('%Y-%m', sale_date) as month,
           ROUND(SUM(total_amount), 2)  as revenue
    FROM sales
    GROUP BY month
    ORDER BY month ASC
""", conn)
fig4 = px.line(monthly_df, x="month", y="revenue",
               markers=True, color_discrete_sequence=["#1F4E79"],
               title="Monthly Revenue Trend")
fig4.update_layout(xaxis_title="Month", yaxis_title="Revenue (€)")
st.plotly_chart(fig4, use_container_width=True)

# ── Row 4: All products table ──
st.markdown("---")
st.subheader("📋 Full Product Inventory")
products_df = pd.read_sql_query("""
    SELECT p.product_name, p.category, p.price,
           p.stock_quantity, p.reorder_level,
           s.supplier_name,
           CASE WHEN p.stock_quantity <= p.reorder_level
                THEN '⚠️ Reorder' ELSE '✓ OK' END as stock_status
    FROM products p
    JOIN suppliers s ON p.supplier_id = s.supplier_id
    ORDER BY p.category
""", conn)
st.dataframe(products_df, use_container_width=True)

conn.close()