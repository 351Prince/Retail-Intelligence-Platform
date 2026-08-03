import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import plotly.express as px
from src.utils.database import get_data

st.set_page_config(page_title="Inventory Analytics", layout="wide")

st.title("📦 Inventory Analytics")

df = get_data()

product = st.sidebar.multiselect(
    "Product",
    sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)

filtered = df[df["Product"].isin(product)]

inventory = (
    filtered.groupby("Product", as_index=False)
    .agg(
        Quantity=("Quantity", "sum"),
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

c1, c2, c3 = st.columns(3)

c1.metric("Products", len(inventory))
c2.metric("Units Sold", int(inventory["Quantity"].sum()))
c3.metric("Revenue", f"${inventory['Revenue'].sum():,.0f}")

st.divider()

fig1 = px.bar(
    inventory.sort_values("Quantity", ascending=False),
    x="Product",
    y="Quantity",
    color="Quantity",
    title="Units Sold by Product"
)

st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    inventory.sort_values("Revenue", ascending=False),
    x="Product",
    y="Revenue",
    color="Revenue",
    title="Revenue by Product"
)

st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(
    inventory.sort_values("Profit", ascending=False),
    x="Product",
    y="Profit",
    color="Profit",
    title="Profit by Product"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Inventory Summary")
st.dataframe(inventory, use_container_width=True)
