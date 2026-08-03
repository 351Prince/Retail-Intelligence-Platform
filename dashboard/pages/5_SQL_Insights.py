import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="SQL Insights", layout="wide")

st.title("🗄️ SQL Insights Dashboard")

conn = sqlite3.connect("database/retail.db")

total_sales = pd.read_sql("""
SELECT ROUND(SUM(Sales),2) AS TotalSales
FROM sales
""", conn)

top_products = pd.read_sql("""
SELECT Product,
ROUND(SUM(Sales),2) AS Revenue
FROM sales
GROUP BY Product
ORDER BY Revenue DESC
LIMIT 10
""", conn)

category_sales = pd.read_sql("""
SELECT Category,
ROUND(SUM(Sales),2) AS Revenue
FROM sales
GROUP BY Category
ORDER BY Revenue DESC
""", conn)

region_sales = pd.read_sql("""
SELECT Region,
ROUND(SUM(Sales),2) AS Revenue
FROM sales
GROUP BY Region
ORDER BY Revenue DESC
""", conn)

payment = pd.read_sql("""
SELECT PaymentMode,
COUNT(*) AS Orders
FROM sales
GROUP BY PaymentMode
ORDER BY Orders DESC
""", conn)

conn.close()

st.metric(
    "Total Sales",
    f"${float(total_sales.iloc[0,0]):,.0f}"
)

c1, c2 = st.columns(2)

fig1 = px.bar(
    top_products,
    x="Product",
    y="Revenue",
    color="Revenue",
    title="Top Products"
)

c1.plotly_chart(fig1, use_container_width=True)

fig2 = px.pie(
    region_sales,
    names="Region",
    values="Revenue",
    title="Region Revenue"
)

c2.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(
    category_sales,
    x="Category",
    y="Revenue",
    color="Revenue",
    title="Category Revenue"
)

st.plotly_chart(fig3, use_container_width=True)

fig4 = px.pie(
    payment,
    names="PaymentMode",
    values="Orders",
    title="Payment Distribution"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("Top Products")

st.dataframe(top_products, use_container_width=True)

st.subheader("Category Revenue")

st.dataframe(category_sales, use_container_width=True)

st.subheader("Region Revenue")

st.dataframe(region_sales, use_container_width=True)
