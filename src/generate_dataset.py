import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

np.random.seed(42)
random.seed(42)

# Test ke liye 10000 rows
# Baad me isse 500000 kar denge
rows = 500000

products = [
    "Laptop",
    "Phone",
    "Headphones",
    "Keyboard",
    "Mouse",
    "Monitor",
    "Tablet",
    "Camera",
    "Printer",
    "Speaker"
]

categories = [
    "Electronics",
    "Accessories",
    "Office"
]

regions = [
    "North",
    "South",
    "East",
    "West"
]

payment_modes = [
    "UPI",
    "Card",
    "Cash",
    "Net Banking"
]

data = []

for i in range(rows):

    quantity = random.randint(1, 5)

    price = random.randint(100, 5000)

    discount = random.choice([0, 5, 10, 15, 20])

    sales = quantity * price * (1 - discount / 100)

    cost = sales * random.uniform(0.50, 0.80)

    profit = sales - cost

    data.append([
        i + 1,
        fake.date_between(start_date="-3y", end_date="today"),
        fake.city(),
        random.choice(regions),
        random.choice(products),
        random.choice(categories),
        quantity,
        price,
        discount,
        round(sales, 2),
        round(cost, 2),
        round(profit, 2),
        random.choice(payment_modes)
    ])

df = pd.DataFrame(
    data,
    columns=[
        "OrderID",
        "OrderDate",
        "City",
        "Region",
        "Product",
        "Category",
        "Quantity",
        "UnitPrice",
        "Discount",
        "Sales",
        "Cost",
        "Profit",
        "PaymentMode"
    ]
)

df.to_csv("data/raw/retail_data.csv", index=False)

print("=" * 60)
print("Retail Dataset Generated Successfully")
print("=" * 60)
print(df.head())
print()
print("Shape :", df.shape)
print("Saved :", "data/raw/retail_data.csv")
print("=" * 60)

