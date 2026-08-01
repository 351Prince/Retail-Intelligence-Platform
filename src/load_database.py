import sqlite3
import pandas as pd

# Read CSV
df = pd.read_csv("data/raw/retail_data.csv")

# Create Database
conn = sqlite3.connect("database/retail.db")

# Load Table
df.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False
)

print("=" * 60)
print("Database Created Successfully")
print("Table Name : sales")
print("Rows :", len(df))
print("=" * 60)

conn.close()
