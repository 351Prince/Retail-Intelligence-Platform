import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import plotly.express as px
import pandas as pd
from src.utils.database import get_data

st.set_page_config(page_title="Sales Analytics", layout="wide")

st.title("💰 Sales Analytics")

df = get_data()

df["OrderDate"] = pd.to_datetime(df["OrderDate"])

st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

payments = st.sidebar.multiselect(
    "Payment Mode",
    sorted(df["PaymentMode"].unique()),
    default=sorted(df["PaymentMode"].unique())
)

start_date = df["OrderDate"].min().date()
end_date = df["OrderDate"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(start_date, end_date)
)

filtered = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["PaymentMode"].isin(payments))
]

if len(date_range) == 2:
    filtered = filtered[
        (filtered["OrderDate"] >= pd.Timestamp(date_range[0])) &
        (filtered["OrderDate"] <= pd.Timestamp(date_range[1]))
    ]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Revenue", f"${filtered['Sales'].sum():,.0f}")
c2.metric("Profit", f"${filtered['Profit'].sum():,.0f}")
c3.metric("Orders", len(filtered))
c4.metric("Avg Order", f"${filtered['Sales'].mean():,.0f}")

st.divider()

monthly = (
    filtered
    .groupby(filtered["OrderDate"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly["OrderDate"] = monthly["OrderDate"].astype(str)

fig1 = px.line(
    monthly,
    x="OrderDate",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig1, use_container_width=True)

category = (
    filtered.groupby("Category", as_index=False)["Sales"]
    .sum()
)

fig2 = px.bar(
    category,
    x="Category",
    y="Sales",
    color="Sales",
    title="Category Revenue"
)

st.plotly_chart(fig2, use_container_width=True)

products = (
    filtered.groupby("Product", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig3 = px.bar(
    products,
    x="Product",
    y="Sales",
    color="Sales",
    title="Top 10 Products"
)

st.plotly_chart(fig3, use_container_width=True)

st.download_button(
    "⬇ Download Filtered CSV",
    filtered.to_csv(index=False),
    file_name="sales_report.csv",
    mime="text/csv"
)

st.dataframe(filtered.head(1000), use_container_width=True)
