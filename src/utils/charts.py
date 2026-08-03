import plotly.express as px

def sales_by_category(df):
    data = (
        df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    return px.bar(
        data,
        x="Category",
        y="Sales",
        color="Sales",
        title="Sales by Category"
    )

def sales_by_region(df):
    data = (
        df.groupby("Region", as_index=False)["Sales"]
        .sum()
    )

    return px.pie(
        data,
        names="Region",
        values="Sales",
        title="Sales by Region"
    )

def top_products(df):
    data = (
        df.groupby("Product", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    return px.bar(
        data,
        x="Product",
        y="Sales",
        color="Sales",
        title="Top 10 Products"
    )

def monthly_sales(df):
    temp = df.copy()

    temp["OrderDate"] = temp["OrderDate"].astype("datetime64[ns]")

    temp["Month"] = temp["OrderDate"].dt.strftime("%Y-%m")

    data = (
        temp.groupby("Month", as_index=False)["Sales"]
        .sum()
    )

    return px.line(
        data,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )
