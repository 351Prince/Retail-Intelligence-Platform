import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import plotly.express as px
from src.utils.database import get_data

st.set_page_config(page_title="Customer Analytics", layout="wide")

st.title("👥 Customer Analytics")

df = get_data()

# Top 20 cities only
top_cities = (
    df.groupby("City", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(20)
)

city = st.sidebar.multiselect(
    "Select City",
    top_cities["City"].tolist(),
    default=top_cities["City"].tolist()
)

filtered = df[df["City"].isin(city)]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Cities", filtered["City"].nunique())
c2.metric("Orders", len(filtered))
c3.metric("Revenue", f"${filtered['Sales'].sum():,.0f}")
c4.metric("Profit", f"${filtered['Profit'].sum():,.0f}")

st.divider()

fig1 = px.bar(
    top_cities,
    x="City",
    y="Sales",
    color="Sales",
    title="Top 20 Cities by Revenue"
)

st.plotly_chart(fig1, use_container_width=True)

payment = (
    filtered.groupby("PaymentMode", as_index=False)["Sales"]
    .sum()
)

fig2 = px.pie(
    payment,
    names="PaymentMode",
    values="Sales",
    title="Payment Mode Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

profit = (
    filtered.groupby("City", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

fig3 = px.bar(
    profit,
    x="City",
    y="Profit",
    color="Profit",
    title="Profit by City"
)

st.plotly_chart(fig3, use_container_width=True)

st.dataframe(filtered.head(1000), use_container_width=True)
