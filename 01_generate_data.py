"""
Sales & Revenue Analytics Dashboard
Task 1: Data Generation
Generates a realistic retail sales dataset with 1200+ records
including intentional data quality issues for cleaning practice.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ─── Seed for reproducibility ───────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

# ─── Reference Data ──────────────────────────────────────────────────────────
REGIONS = ["North", "South", "East", "West", "Central"]

SALES_REPS = {
    "North":   ["Alice Johnson", "Bob Martinez", "Carol White"],
    "South":   ["David Brown", "Emma Davis", "Frank Wilson"],
    "East":    ["Grace Lee", "Henry Taylor", "Iris Chen"],
    "West":    ["Jack Thompson", "Karen Moore", "Liam Garcia"],
    "Central": ["Mia Anderson", "Noah Harris", "Olivia Clark"],
}

PRODUCTS = {
    "Electronics": {
        "Laptop Pro 15": (75000, 52000),
        "Wireless Headphones": (8500, 4200),
        "Smart Watch Series 5": (22000, 13000),
        "4K Monitor 27\"": (35000, 22000),
        "Bluetooth Speaker": (4500, 2100),
        "USB-C Hub 7-in-1": (3200, 1500),
        "Mechanical Keyboard": (6500, 3200),
        "Gaming Mouse": (3800, 1800),
    },
    "Clothing": {
        "Men's Running Shoes": (5500, 2800),
        "Women's Yoga Pants": (2800, 1200),
        "Winter Jacket": (8900, 4500),
        "Casual T-Shirt": (799, 300),
        "Formal Blazer": (6500, 3200),
        "Sports Socks (Pack 6)": (450, 180),
        "Leather Wallet": (1800, 800),
        "Baseball Cap": (650, 250),
    },
    "Home & Kitchen": {
        "Air Fryer 5.5L": (9500, 5200),
        "Coffee Maker Deluxe": (7800, 4100),
        "Non-Stick Cookware Set": (5200, 2600),
        "Robot Vacuum Cleaner": (28000, 17000),
        "Blender Pro 1000W": (4500, 2200),
        "Water Purifier RO": (18000, 10500),
        "Instant Pot 8Qt": (12000, 6800),
        "Electric Kettle 1.7L": (2200, 1000),
    },
    "Sports": {
        "Yoga Mat Premium": (1800, 700),
        "Dumbbell Set 20kg": (6500, 3200),
        "Cycling Helmet": (3500, 1600),
        "Badminton Racket Set": (2800, 1200),
        "Resistance Bands Set": (1200, 450),
        "Protein Shaker Bottle": (650, 250),
        "Foam Roller": (1500, 600),
        "Jump Rope Steel": (800, 300),
    },
    "Books": {
        "Python for Data Analysis": (2500, 900),
        "SQL Mastery Guide": (1800, 650),
        "Business Intelligence Handbook": (3200, 1200),
        "Machine Learning Fundamentals": (2800, 1000),
        "Data Visualization Bible": (2200, 800),
        "Excel Advanced Techniques": (1500, 550),
        "Power BI Pro": (1900, 700),
        "Statistics for Data Science": (2100, 750),
    },
}

CUSTOMER_NAMES = [
    "Aarav Shah", "Priya Patel", "Rahul Gupta", "Sneha Mehta", "Vikram Singh",
    "Ananya Sharma", "Rohan Verma", "Pooja Nair", "Arjun Reddy", "Kavya Iyer",
    "Siddharth Joshi", "Deepika Rao", "Aditya Kumar", "Nisha Agarwal", "Ravi Tiwari",
    "Sunita Bose", "Manish Pandey", "Divya Chaudhary", "Suresh Pillai", "Meera Krishnan",
    "Amit Bansal", "Rekha Srivastava", "Nikhil Malhotra", "Anjali Desai", "Harish Mishra",
    "Rina Ghosh", "Tarun Saxena", "Shweta Dubey", "Gaurav Kapoor", "Neha Jain",
    "Pratik More", "Smita Patil", "Kiran Kulkarni", "Varun Naik", "Rujuta Deshpande",
    "Mihir Bhatt", "Hema Trivedi", "Sachin Parekh", "Leena Shah", "Dhruv Rawal",
    "Brijesh Yadav", "Geeta Chauhan", "Mohit Awasthi", "Puja Tripathi", "Sumit Roy",
    "Ritika Das", "Vivek Sen", "Nandita Chakraborty", "Rajesh Mukherjee", "Shilpa Basu",
]

def generate_customer_id(name):
    idx = CUSTOMER_NAMES.index(name) + 1
    return f"CUST{idx:04d}"

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# ─── Generate Base Records ───────────────────────────────────────────────────
records = []
order_id_counter = 10001
start_date = datetime(2023, 1, 1)
end_date   = datetime(2024, 12, 31)

for _ in range(1200):
    region      = random.choice(REGIONS)
    sales_rep   = random.choice(SALES_REPS[region])
    category    = random.choice(list(PRODUCTS.keys()))
    product     = random.choice(list(PRODUCTS[category].keys()))
    unit_price, unit_cost = PRODUCTS[category][product]

    # Add price variance ±10 %
    unit_price = round(unit_price * random.uniform(0.90, 1.10), 2)
    unit_cost  = round(unit_cost  * random.uniform(0.90, 1.10), 2)

    qty = random.randint(1, 10)

    # Seasonal boost: Q4 higher sales
    order_date = random_date(start_date, end_date)
    if order_date.month in [10, 11, 12]:
        qty = random.randint(2, 15)

    revenue = round(unit_price * qty, 2)
    cost    = round(unit_cost  * qty, 2)
    profit  = round(revenue - cost, 2)

    customer_name = random.choice(CUSTOMER_NAMES)
    customer_id   = generate_customer_id(customer_name)

    records.append({
        "Order_ID":         f"ORD{order_id_counter}",
        "Order_Date":       order_date.strftime("%Y-%m-%d"),
        "Customer_ID":      customer_id,
        "Customer_Name":    customer_name,
        "Product_Category": category,
        "Product_Name":     product,
        "Quantity":         qty,
        "Unit_Price":       unit_price,
        "Revenue":          revenue,
        "Cost":             cost,
        "Profit":           profit,
        "Region":           region,
        "Sales_Rep":        sales_rep,
    })
    order_id_counter += 1

df = pd.DataFrame(records)

# ─── Inject Data Quality Issues ──────────────────────────────────────────────

# 1. Missing values (≈5 % each)
for col in ["Customer_Name", "Product_Category", "Sales_Rep", "Region", "Quantity"]:
    mask = np.random.rand(len(df)) < 0.05
    df.loc[mask, col] = np.nan

# 2. Duplicate rows (50 exact duplicates)
dup_rows = df.sample(50, random_state=1)
df = pd.concat([df, dup_rows], ignore_index=True)

# 3. Wrong data types - convert Quantity column to object then inject strings
df["Quantity"] = df["Quantity"].astype(object)
bad_qty_idx = np.random.choice(df.index, 30, replace=False)
df.loc[bad_qty_idx, "Quantity"] = ["N/A", "unknown", "TBD"] * 10

# 4. Inconsistent casing
df.loc[np.random.choice(df.index, 40, replace=False), "Region"] = \
    df["Region"].dropna().sample(40, random_state=2).str.upper().values

# 5. Negative / zero Revenue outliers (10 records)
df.loc[np.random.choice(df.index, 10, replace=False), "Revenue"] = \
    np.random.choice([-500, 0, -1200], 10)

# 6. Future dates (5 records)
for idx in np.random.choice(df.index, 5, replace=False):
    df.at[idx, "Order_Date"] = "2025-06-15"

# ─── Export Raw CSV ──────────────────────────────────────────────────────────
os.makedirs("../data/raw", exist_ok=True)
out_path = "../data/raw/sales_raw.csv"
df.to_csv(out_path, index=False)

print(f"✅ Raw dataset saved: {out_path}")
print(f"   Total records : {len(df)}")
print(f"   Columns       : {list(df.columns)}")
print(f"\nData Quality Issues Injected:")
print(f"  • Missing values  : ~5% per key column")
print(f"  • Duplicate rows  : 50")
print(f"  • Wrong data types: 30 rows (Quantity as string)")
print(f"  • Case issues     : 40 rows (Region uppercase)")
print(f"  • Invalid Revenue : 10 rows (negative/zero)")
print(f"  • Future dates    : 5 rows (2025-06-15)")
