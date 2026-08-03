import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st

from src.utils.database import get_data
from src.utils.kpi import calculate_kpis
from src.utils.charts import (
    sales_by_category,
    sales_by_region,
    top_products,
    monthly_sales
)

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

df = get_data()
kpis = calculate_kpis(df)

st.title("📊 Executive Dashboard")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Revenue", f"${kpis['total_sales']:,.0f}")
c2.metric("Profit", f"${kpis['total_profit']:,.0f}")
c3.metric("Orders", f"{kpis['total_orders']:,}")
c4.metric("Avg Order", f"${kpis['avg_order_value']:,.0f}")
c5.metric("Margin", f"{kpis['profit_margin']}%")

left, right = st.columns(2)

left.plotly_chart(sales_by_category(df), use_container_width=True)
right.plotly_chart(sales_by_region(df), use_container_width=True)

st.plotly_chart(monthly_sales(df), use_container_width=True)
st.plotly_chart(top_products(df), use_container_width=True)
