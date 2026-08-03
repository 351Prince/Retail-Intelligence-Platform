import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils.database import get_data

st.set_page_config(page_title="ABC Inventory Analysis", layout="wide")

st.title("📦 ABC Inventory Analysis")

df = get_data()

abc = (
    df.groupby("Product", as_index=False)["Sales"]
      .sum()
      .sort_values("Sales", ascending=False)
)

abc["Cumulative"] = abc["Sales"].cumsum()
abc["CumPct"] = abc["Cumulative"] / abc["Sales"].sum() * 100

def classify(x):
    if x <= 80:
        return "A"
    elif x <= 95:
        return "B"
    return "C"

abc["Class"] = abc["CumPct"].apply(classify)

c1, c2, c3 = st.columns(3)

c1.metric("A Items", (abc["Class"] == "A").sum())
c2.metric("B Items", (abc["Class"] == "B").sum())
c3.metric("C Items", (abc["Class"] == "C").sum())

fig = px.bar(
    abc,
    x="Product",
    y="Sales",
    color="Class",
    title="ABC Classification by Revenue",
    text="Class"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Inventory Classification")

st.dataframe(abc, use_container_width=True)

st.info("""
### Inventory Strategy

🟢 A Items:
- High revenue
- Maintain stock
- Daily monitoring

🟡 B Items:
- Weekly monitoring
- Moderate inventory

🔴 C Items:
- Low priority
- Reduce excess stock
""")
