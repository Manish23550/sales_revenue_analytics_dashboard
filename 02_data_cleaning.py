"""
Sales & Revenue Analytics Dashboard
Task 2: Python Data Cleaning
Uses Pandas and NumPy to clean the raw dataset.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings
warnings.filterwarnings("ignore")

print("=" * 65)
print("  SALES & REVENUE ANALYTICS — DATA CLEANING PIPELINE")
print("=" * 65)

# ─── 1. Load Raw Data ────────────────────────────────────────────────────────
df_raw = pd.read_csv("../data/raw/sales_raw.csv")
print(f"\n[1] Loaded raw data: {df_raw.shape[0]} rows × {df_raw.shape[1]} cols")

# ─── 2. Initial Inspection ───────────────────────────────────────────────────
print("\n[2] Data Quality Audit:")
print(f"    Duplicate rows  : {df_raw.duplicated().sum()}")
print(f"    Missing values  :\n{df_raw.isnull().sum().to_string()}")

# ─── 3. Remove Duplicates ────────────────────────────────────────────────────
df = df_raw.copy()
before = len(df)
df = df.drop_duplicates()
print(f"\n[3] Removed duplicates: {before - len(df)} rows removed → {len(df)} remain")

# ─── 4. Fix Data Types ───────────────────────────────────────────────────────
# Order_Date → datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

# Quantity → numeric (replace text placeholders with NaN)
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

# Numeric price/revenue columns
for col in ["Unit_Price", "Revenue", "Cost", "Profit"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print(f"\n[4] Fixed data types:")
print(df.dtypes.to_string())

# ─── 5. Handle Future Dates ──────────────────────────────────────────────────
cutoff = pd.Timestamp("2024-12-31")
future_mask = df["Order_Date"] > cutoff
print(f"\n[5] Future dates found: {future_mask.sum()} — setting to NaT")
df.loc[future_mask, "Order_Date"] = pd.NaT

# ─── 6. Handle Invalid Revenue/Cost/Profit ──────────────────────────────────
invalid_rev = (df["Revenue"] <= 0) | (df["Revenue"].isna())
print(f"\n[6] Invalid Revenue rows: {invalid_rev.sum()} — will be recalculated or dropped")

# Remove rows where we cannot recover data (both Revenue and Quantity null)
cannot_fix = df["Revenue"].isna() & df["Quantity"].isna()
df = df[~cannot_fix]

# Recalculate Revenue where it's ≤ 0 from Unit_Price * Quantity
mask_bad_rev = (df["Revenue"] <= 0) & df["Unit_Price"].notna() & df["Quantity"].notna()
df.loc[mask_bad_rev, "Revenue"] = df.loc[mask_bad_rev, "Unit_Price"] * df.loc[mask_bad_rev, "Quantity"]
df.loc[mask_bad_rev, "Cost"]    = df.loc[mask_bad_rev, "Cost"]
df.loc[mask_bad_rev, "Profit"]  = df.loc[mask_bad_rev, "Revenue"] - df.loc[mask_bad_rev, "Cost"]

# ─── 7. Fix Inconsistent Casing ──────────────────────────────────────────────
df["Region"]           = df["Region"].str.strip().str.title()
df["Product_Category"] = df["Product_Category"].str.strip().str.title()
df["Customer_Name"]    = df["Customer_Name"].str.strip().str.title()
df["Sales_Rep"]        = df["Sales_Rep"].str.strip().str.title()
print("\n[7] Standardised text casing: Region, Category, Customer_Name, Sales_Rep")

# ─── 8. Handle Missing Values ────────────────────────────────────────────────
# Region → mode by Sales_Rep
rep_region_map = df.dropna(subset=["Region", "Sales_Rep"])\
                   .groupby("Sales_Rep")["Region"].agg(lambda x: x.mode()[0] if len(x) > 0 else np.nan)
df["Region"] = df.apply(
    lambda r: rep_region_map.get(r["Sales_Rep"], r["Region"])
              if pd.isna(r["Region"]) else r["Region"], axis=1
)

# Product_Category → infer from Product_Name
prod_cat_map = df.dropna(subset=["Product_Category", "Product_Name"])\
                 .drop_duplicates("Product_Name").set_index("Product_Name")["Product_Category"]
df["Product_Category"] = df.apply(
    lambda r: prod_cat_map.get(r["Product_Name"], r["Product_Category"])
              if pd.isna(r["Product_Category"]) else r["Product_Category"], axis=1
)

# Quantity → median
qty_median = df["Quantity"].median()
df["Quantity"] = df["Quantity"].fillna(qty_median)

# Customer_Name & Sales_Rep → "Unknown"
df["Customer_Name"] = df["Customer_Name"].fillna("Unknown Customer")
df["Sales_Rep"]     = df["Sales_Rep"].fillna("Unknown Rep")

# Order_Date → drop rows with no date (can't be recovered)
df = df.dropna(subset=["Order_Date"])

print(f"\n[8] Missing values after imputation:")
print(df.isnull().sum().to_string())

# ─── 9. Recalculate Derived Columns ──────────────────────────────────────────
df["Quantity"]  = df["Quantity"].astype(int)
df["Revenue"]   = (df["Unit_Price"] * df["Quantity"]).round(2)
df["Profit"]    = (df["Revenue"] - df["Cost"]).round(2)
df["Profit_Margin_%"] = ((df["Profit"] / df["Revenue"]) * 100).round(2)

# ─── 10. Add Enrichment Columns ──────────────────────────────────────────────
df["Year"]          = df["Order_Date"].dt.year
df["Month"]         = df["Order_Date"].dt.month
df["Month_Name"]    = df["Order_Date"].dt.strftime("%B")
df["Quarter"]       = df["Order_Date"].dt.quarter.apply(lambda q: f"Q{q}")
df["Day_of_Week"]   = df["Order_Date"].dt.day_name()
df["Week_Number"]   = df["Order_Date"].dt.isocalendar().week.astype(int)

# Revenue Tier
def revenue_tier(rev):
    if rev >= 50000:  return "Premium"
    elif rev >= 20000: return "High"
    elif rev >= 5000:  return "Medium"
    else:              return "Low"

df["Revenue_Tier"] = df["Revenue"].apply(revenue_tier)

# Profit Category
df["Profit_Category"] = pd.cut(
    df["Profit_Margin_%"],
    bins=[-np.inf, 10, 25, 40, np.inf],
    labels=["Low Margin", "Medium Margin", "High Margin", "Excellent Margin"]
)

print(f"\n[9-10] Derived & enrichment columns added:")
new_cols = ["Profit_Margin_%", "Year", "Month", "Month_Name", "Quarter",
            "Day_of_Week", "Week_Number", "Revenue_Tier", "Profit_Category"]
print(f"  {new_cols}")

# ─── 11. Final Validation ────────────────────────────────────────────────────
print(f"\n[11] Final Dataset Summary:")
print(f"    Rows    : {len(df)}")
print(f"    Columns : {len(df.columns)}")
print(f"    Date range : {df['Order_Date'].min().date()} → {df['Order_Date'].max().date()}")
print(f"    Total Revenue : ₹{df['Revenue'].sum():,.0f}")
print(f"    Total Profit  : ₹{df['Profit'].sum():,.0f}")
print(f"    Avg Margin    : {df['Profit_Margin_%'].mean():.1f}%")

# ─── 12. Export Cleaned Dataset ──────────────────────────────────────────────
os.makedirs("../data/cleaned", exist_ok=True)
out_path = "../data/cleaned/sales_cleaned.csv"
df.to_csv(out_path, index=False)
print(f"\n✅ Cleaned dataset saved: {out_path}")
print("=" * 65)
