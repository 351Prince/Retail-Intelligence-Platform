import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from src.utils.database import get_data

st.set_page_config(page_title="Sales Forecasting", layout="wide")

st.title("📈 Sales Forecasting")

df = get_data()
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

monthly = (
    df.groupby(df["OrderDate"].dt.to_period("M"))["Sales"]
      .sum()
      .reset_index()
)

monthly["OrderDate"] = monthly["OrderDate"].dt.to_timestamp()
monthly["Month"] = range(len(monthly))

X = monthly[["Month"]]
y = monthly["Sales"]

model = LinearRegression()
model.fit(X, y)

monthly["Predicted"] = model.predict(X)

future = pd.DataFrame({
    "Month": range(len(monthly), len(monthly) + 6)
})

future["Predicted"] = model.predict(future)
future["OrderDate"] = pd.date_range(
    monthly["OrderDate"].max() + pd.offsets.MonthBegin(),
    periods=6,
    freq="MS"
)

c1, c2 = st.columns(2)

c1.metric("Months Used", len(monthly))
c2.metric("Forecast Horizon", "6 Months")

st.divider()

fig1 = px.line(
    monthly,
    x="OrderDate",
    y=["Sales", "Predicted"],
    markers=True,
    title="Actual vs Predicted Sales"
)

st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(
    future,
    x="OrderDate",
    y="Predicted",
    markers=True,
    title="Next 6 Months Forecast"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Forecast Table")

st.dataframe(future, use_container_width=True)

st.download_button(
    "⬇ Download Forecast",
    future.to_csv(index=False),
    file_name="forecast.csv",
    mime="text/csv"
)
