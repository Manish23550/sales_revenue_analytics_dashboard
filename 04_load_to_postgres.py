"""
Sales & Revenue Analytics Dashboard
Task 4b: Load Cleaned Data into PostgreSQL
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os

# ─── Configuration ───────────────────────────────────────────────────────────
# Update with your PostgreSQL credentials
DB_USER = "postgres"
DB_PASS = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "sales_analytics"

CONN_STR = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def load_data():
    print("=" * 55)
    print("  PostgreSQL Data Loader — Sales Analytics")
    print("=" * 55)

    # Load cleaned CSV
    df = pd.read_csv("../data/cleaned/sales_cleaned.csv", parse_dates=["Order_Date"])
    print(f"\n✅ Loaded cleaned data: {len(df)} rows")

    # Create engine
    engine = create_engine(CONN_STR)

    with engine.connect() as conn:
        # ─── Populate dim_customers ───────────────────────────────────────
        cust = df[["Customer_ID", "Customer_Name"]].drop_duplicates("Customer_ID")
        cust.columns = ["customer_id", "customer_name"]
        cust.to_sql("dim_customers", engine, schema="sales",
                    if_exists="append", index=False, method="multi")
        print(f"✅ dim_customers: {len(cust)} rows loaded")

        # ─── Populate dim_products ────────────────────────────────────────
        prods = df[["Product_Name", "Product_Category"]].drop_duplicates("Product_Name")
        prods.columns = ["product_name", "product_category"]
        prods.to_sql("dim_products", engine, schema="sales",
                     if_exists="append", index=False, method="multi")
        print(f"✅ dim_products: {len(prods)} rows loaded")

        # ─── Populate dim_regions ─────────────────────────────────────────
        regions = df["Region"].dropna().drop_duplicates().to_frame()
        regions.columns = ["region_name"]
        regions.to_sql("dim_regions", engine, schema="sales",
                       if_exists="append", index=False, method="multi")
        print(f"✅ dim_regions: {len(regions)} rows loaded")

        # ─── Populate dim_reps ────────────────────────────────────────────
        reps = df[["Sales_Rep", "Region"]].drop_duplicates("Sales_Rep")
        reps.columns = ["rep_name", "region"]
        reps = reps[reps["rep_name"] != "Unknown Rep"]
        reps.to_sql("dim_reps", engine, schema="sales",
                    if_exists="append", index=False, method="multi")
        print(f"✅ dim_reps: {len(reps)} rows loaded")

        # ─── Populate fact_orders ─────────────────────────────────────────
        fact = df.rename(columns={
            "Order_ID":        "order_id",
            "Order_Date":      "order_date",
            "Customer_ID":     "customer_id",
            "Product_Name":    "product_name",
            "Sales_Rep":       "sales_rep",
            "Region":          "region",
            "Quantity":        "quantity",
            "Unit_Price":      "unit_price",
            "Revenue":         "revenue",
            "Cost":            "cost",
            "Profit":          "profit",
            "Profit_Margin_%": "profit_margin",
            "Revenue_Tier":    "revenue_tier",
            "Year":            "year",
            "Month":           "month",
            "Month_Name":      "month_name",
            "Quarter":         "quarter",
            "Day_of_Week":     "day_of_week",
            "Week_Number":     "week_number",
        })[[
            "order_id","order_date","customer_id","product_name",
            "sales_rep","region","quantity","unit_price","revenue",
            "cost","profit","profit_margin","revenue_tier",
            "year","month","month_name","quarter","day_of_week","week_number"
        ]]
        fact.to_sql("fact_orders", engine, schema="sales",
                    if_exists="append", index=False, method="multi", chunksize=200)
        print(f"✅ fact_orders: {len(fact)} rows loaded")

    print("\n✅ All data loaded into PostgreSQL successfully!")
    print("   Run sales_analytics_queries.sql in pgAdmin or psql to explore.")
    print("=" * 55)

if __name__ == "__main__":
    load_data()
