def calculate_kpis(df):
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    total_orders = int(len(df))
    avg_order_value = float(df["Sales"].mean())
    profit_margin = (total_profit / total_sales) * 100 if total_sales else 0

    return {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "total_orders": total_orders,
        "avg_order_value": round(avg_order_value, 2),
        "profit_margin": round(profit_margin, 2),
    }
