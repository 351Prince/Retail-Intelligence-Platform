import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.utils.database import get_data

st.set_page_config(page_title="Pareto Analysis", layout="wide")

st.title("📊 Pareto Analysis (80/20 Rule)")

df = get_data()

pareto = (
    df.groupby("Product", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

pareto["Cumulative Sales"] = pareto["Sales"].cumsum()
pareto["Cumulative %"] = (
    pareto["Cumulative Sales"] /
    pareto["Sales"].sum()
) * 100

fig = go.Figure()

fig.add_bar(
    x=pareto["Product"],
    y=pareto["Sales"],
    name="Revenue"
)

fig.add_scatter(
    x=pareto["Product"],
    y=pareto["Cumulative %"],
    name="Cumulative %",
    yaxis="y2",
    mode="lines+markers"
)

fig.update_layout(
    title="Pareto Chart",
    xaxis_title="Product",
    yaxis_title="Revenue",
    yaxis2=dict(
        title="Cumulative %",
        overlaying="y",
        side="right",
        range=[0,100]
    ),
    height=650
)

st.plotly_chart(fig, use_container_width=True)

top80 = pareto[pareto["Cumulative %"] <= 80]

c1, c2, c3 = st.columns(3)

c1.metric(
    "Products",
    len(pareto)
)

c2.metric(
    "Top 80% Products",
    len(top80)
)

c3.metric(
    "Revenue",
    f"${pareto['Sales'].sum():,.0f}"
)

st.divider()

st.subheader("🏆 Top Revenue Contributors")

st.dataframe(top80, use_container_width=True)

st.divider()

st.subheader("🤖 Business Insight")

st.success(
    f"""
Top {len(top80)} products contribute approximately
80% of total revenue.

Recommendation:

• Increase inventory of these products.

• Prioritize marketing budget on them.

• Review pricing of low-selling products.

• Bundle low-selling products with best sellers.
"""
)
