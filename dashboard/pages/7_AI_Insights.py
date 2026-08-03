import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from src.utils.database import get_data

st.set_page_config(
    page_title="AI Business Insights",
    layout="wide"
)

st.title("🤖 AI Business Insights")

df = get_data()

# ---------------- KPIs ----------------

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100

best_product = (
    df.groupby("Product")["Sales"]
      .sum()
      .idxmax()
)

worst_product = (
    df.groupby("Product")["Sales"]
      .sum()
      .idxmin()
)

best_region = (
    df.groupby("Region")["Sales"]
      .sum()
      .idxmax()
)

worst_region = (
    df.groupby("Region")["Sales"]
      .sum()
      .idxmin()
)

best_category = (
    df.groupby("Category")["Profit"]
      .sum()
      .idxmax()
)

top_payment = (
    df.groupby("PaymentMode")["Sales"]
      .sum()
      .idxmax()
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Revenue",
    f"${total_sales:,.0f}"
)

c2.metric(
    "Profit",
    f"${total_profit:,.0f}"
)

c3.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)

st.divider()

st.subheader("📋 Executive Insights")

st.success(f"✅ Highest Revenue Product : **{best_product}**")

st.success(f"✅ Best Performing Region : **{best_region}**")

st.success(f"✅ Most Profitable Category : **{best_category}**")

st.info(f"💳 Preferred Payment Mode : **{top_payment}**")

st.warning(f"⚠ Lowest Revenue Product : **{worst_product}**")

st.error(f"🚨 Weakest Region : **{worst_region}**")

st.divider()

st.subheader("🧠 AI Recommendations")

recommendations = [
    f"Increase inventory for {best_product}.",
    f"Run promotional campaigns in {worst_region}.",
    f"Focus marketing on {best_region}.",
    f"Expand products under {best_category}.",
    f"Offer cashback on {top_payment} transactions.",
    "Monitor low-performing products every month.",
    "Review pricing strategy for weak-performing regions.",
    "Increase repeat customer campaigns.",
]

for i, rec in enumerate(recommendations, start=1):
    st.write(f"{i}. {rec}")

st.divider()

st.subheader("📌 Business Summary")

st.markdown(f"""
- Total Revenue : **${total_sales:,.0f}**
- Total Profit : **${total_profit:,.0f}**
- Profit Margin : **{profit_margin:.2f}%**
- Best Product : **{best_product}**
- Weak Product : **{worst_product}**
- Best Region : **{best_region}**
- Weak Region : **{worst_region}**
- Best Category : **{best_category}**
- Preferred Payment : **{top_payment}**
""")
