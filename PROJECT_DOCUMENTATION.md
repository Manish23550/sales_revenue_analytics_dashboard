# Sales & Revenue Analytics Dashboard
## Complete Project Documentation

---

## 1. PROJECT ARCHITECTURE

```
sales_analytics/
│
├── data/
│   ├── raw/
│   │   └── sales_raw.csv           ← Generated with intentional data quality issues
│   └── cleaned/
│       └── sales_cleaned.csv       ← Cleaned, enriched, ready for analysis
│
├── scripts/
│   ├── 01_generate_data.py         ← Synthetic dataset generation
│   ├── 02_data_cleaning.py         ← Pandas/NumPy cleaning pipeline
│   ├── 03_eda.py                   ← EDA with Matplotlib & Seaborn
│   └── 04_load_to_postgres.py      ← SQLAlchemy → PostgreSQL loader
│
├── sql/
│   └── sales_analytics_queries.sql ← Schema + 35 analytical SQL queries
│
├── eda/
│   ├── 01_kpi_overview.png
│   ├── 02_monthly_revenue_trend.png
│   ├── 03_revenue_profit_by_category.png
│   ├── 04_regional_performance.png
│   ├── 05_top_products.png
│   ├── 06_customer_segmentation.png
│   ├── 07_revenue_heatmap.png
│   ├── 08_profit_margin_analysis.png
│   ├── 09_quarterly_comparison.png
│   └── 10_sales_rep_performance.png
│
├── dashboard/
│   ├── PowerBI_Sales_Dashboard.pbix
│   └── DAX_Measures.txt
│
├── docs/
│   ├── PROJECT_DOCUMENTATION.md    ← This file
│   └── DATA_DICTIONARY.md
│
└── README.md
```

---

## 2. BUSINESS PROBLEM STATEMENT

A mid-sized retail company operating across 5 regions in India lacks a
centralised view of its sales and profitability data. Decision-makers rely
on fragmented Excel sheets and ad-hoc reports, causing:

- Delayed visibility into revenue trends and underperforming products.
- Inability to segment customers or track Sales Rep productivity.
- No mechanism to measure YoY / MoM growth or forecast demand.

**Goal:** Build an end-to-end analytics solution — from raw data ingestion
to an interactive Power BI executive dashboard — that delivers actionable
insights and supports data-driven decisions.

---

## 3. OBJECTIVES

| #  | Objective                                                       |
|----|----------------------------------------------------------------|
| 1  | Generate a realistic, analysis-ready retail dataset            |
| 2  | Clean and enrich raw data using Python (Pandas / NumPy)        |
| 3  | Perform deep EDA with 10 publication-quality visualisations    |
| 4  | Store data in PostgreSQL with a star-schema and 35 SQL queries |
| 5  | Build a 4-page interactive Power BI dashboard                  |
| 6  | Write 20+ DAX measures for business KPIs                       |
| 7  | Document insights, recommendations, and interview prep         |

---

## 4. DATA DICTIONARY

### Table: fact_orders

| Column           | Type         | Description                              |
|------------------|--------------|------------------------------------------|
| order_id         | VARCHAR(15)  | Unique order identifier (ORD10001…)      |
| order_date       | DATE         | Date the order was placed                |
| customer_id      | VARCHAR(10)  | FK → dim_customers (CUST0001…)           |
| product_name     | VARCHAR(100) | FK → dim_products                        |
| sales_rep        | VARCHAR(100) | Name of Sales Representative             |
| region           | VARCHAR(50)  | Region: North/South/East/West/Central    |
| quantity         | INT          | Number of units ordered                  |
| unit_price       | NUMERIC(12,2)| Price per unit (₹)                       |
| revenue          | NUMERIC(12,2)| unit_price × quantity (₹)               |
| cost             | NUMERIC(12,2)| Cost of goods sold (₹)                  |
| profit           | NUMERIC(12,2)| revenue − cost (₹)                      |
| profit_margin    | NUMERIC(6,2) | (profit / revenue) × 100 (%)            |
| revenue_tier     | VARCHAR(20)  | Low / Medium / High / Premium            |
| year             | INT          | Extracted year from order_date           |
| month            | INT          | Extracted month (1–12)                   |
| month_name       | VARCHAR(15)  | Month name (January…December)            |
| quarter          | VARCHAR(2)   | Q1 / Q2 / Q3 / Q4                        |
| day_of_week      | VARCHAR(10)  | Monday…Sunday                            |
| week_number      | INT          | ISO week number (1–53)                   |

### Table: dim_customers

| Column        | Type         | Description              |
|---------------|--------------|--------------------------|
| customer_id   | VARCHAR(10)  | Primary key              |
| customer_name | VARCHAR(100) | Full customer name        |

### Table: dim_products

| Column           | Type         | Description              |
|------------------|--------------|--------------------------|
| product_name     | VARCHAR(100) | Primary key              |
| product_category | VARCHAR(50)  | Electronics/Clothing/… |

### Table: dim_regions

| Column      | Type        | Description    |
|-------------|-------------|----------------|
| region_id   | SERIAL      | Primary key    |
| region_name | VARCHAR(50) | Unique region  |

### Table: dim_reps

| Column   | Type         | Description           |
|----------|--------------|-----------------------|
| rep_id   | SERIAL       | Primary key           |
| rep_name | VARCHAR(100) | Sales Representative  |
| region   | VARCHAR(50)  | Assigned region       |

---

## 5. WORKFLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA PIPELINE WORKFLOW                       │
└─────────────────────────────────────────────────────────────────┘

  [Script 01]             [Script 02]           [Script 03]
  Data Generation    →    Data Cleaning    →     EDA
  01_generate_data.py     02_data_cleaning.py    03_eda.py
       │                       │                     │
       ▼                       ▼                     ▼
  sales_raw.csv          sales_cleaned.csv     10 PNG Charts
  1,250 rows             1,200 rows            (../eda/)
  13 columns             22 columns


  [Script 04]             [SQL File]            [Power BI]
  Load to PostgreSQL  →   35 SQL Queries   →   Dashboard
  04_load_to_postgres.py  sales_analytics       4 Pages
       │                  _queries.sql          20+ DAX
       ▼                       │                measures
  PostgreSQL DB          Business KPIs
  Star Schema            Window Functions
                         CTEs, Rankings
```

---

## 6. POWER BI DASHBOARD DESIGN

### Page 1 — Executive Dashboard
**Visuals:**
- KPI Cards: Total Revenue | Total Profit | Profit Margin% | Total Orders
- Line Chart: Monthly Revenue Trend (2023 vs 2024)
- Bar Chart: Quarterly Revenue Comparison
- Slicer: Year | Region | Quarter

### Page 2 — Sales Dashboard
**Visuals:**
- Clustered Bar: Revenue by Region
- Donut Chart: Revenue Share by Product Category
- Area Chart: Monthly Sales Trend by Category
- Table: Top 10 Orders by Revenue
- Slicer: Region | Product Category | Month

### Page 3 — Customer Dashboard
**Visuals:**
- Table: Top 20 Customers (Revenue, Profit, Orders)
- Pie Chart: Customer Segment Distribution (Bronze/Silver/Gold/Platinum)
- Bar Chart: Repeat vs One-time Customers by Region
- KPI: Total Unique Customers | Avg Order Value | Avg Customer Revenue
- Slicer: Region | Customer Segment

### Page 4 — Product Dashboard
**Visuals:**
- Bar Chart: Top 10 Products by Revenue
- Heatmap (Matrix): Category × Month Revenue
- Scatter Plot: Revenue vs Profit Margin by Product
- Table: Bottom 5 Products (low performance alert)
- Slicer: Product Category | Region | Year

---

## 7. DAX MEASURES (20+)

```dax
-- 1. Total Revenue
Total Revenue = SUM(fact_orders[revenue])

-- 2. Total Profit
Total Profit = SUM(fact_orders[profit])

-- 3. Profit Margin %
Profit Margin % =
    DIVIDE([Total Profit], [Total Revenue], 0) * 100

-- 4. Total Orders
Total Orders = COUNTROWS(fact_orders)

-- 5. Average Order Value
Avg Order Value =
    DIVIDE([Total Revenue], [Total Orders], 0)

-- 6. Total Quantity Sold
Total Quantity = SUM(fact_orders[quantity])

-- 7. Total Cost
Total Cost = SUM(fact_orders[cost])

-- 8. Unique Customers
Unique Customers = DISTINCTCOUNT(fact_orders[customer_id])

-- 9. Revenue per Customer
Revenue per Customer =
    DIVIDE([Total Revenue], [Unique Customers], 0)

-- 10. YTD Revenue
YTD Revenue =
    TOTALYTD([Total Revenue], fact_orders[order_date])

-- 11. Previous Year Revenue
PY Revenue =
    CALCULATE([Total Revenue],
              SAMEPERIODLASTYEAR(fact_orders[order_date]))

-- 12. YoY Revenue Growth %
YoY Growth % =
    DIVIDE([Total Revenue] - [PY Revenue],
           NULLIF([PY Revenue], 0), 0) * 100

-- 13. MoM Revenue Growth %
MoM Growth % =
    VAR current_month = [Total Revenue]
    VAR prev_month    =
        CALCULATE([Total Revenue],
                  DATEADD(fact_orders[order_date], -1, MONTH))
    RETURN
    DIVIDE(current_month - prev_month, NULLIF(prev_month, 0), 0) * 100

-- 14. Running Total Revenue
Running Total Revenue =
    CALCULATE(
        [Total Revenue],
        FILTER(
            ALL(fact_orders[order_date]),
            fact_orders[order_date] <= MAX(fact_orders[order_date])
        )
    )

-- 15. Cumulative Profit
Cumulative Profit =
    CALCULATE(
        [Total Profit],
        FILTER(
            ALL(fact_orders[order_date]),
            fact_orders[order_date] <= MAX(fact_orders[order_date])
        )
    )

-- 16. Previous Month Revenue
PM Revenue =
    CALCULATE([Total Revenue],
              DATEADD(fact_orders[order_date], -1, MONTH))

-- 17. Q4 Revenue
Q4 Revenue =
    CALCULATE([Total Revenue],
              fact_orders[quarter] = "Q4")

-- 18. Electronics Revenue
Electronics Revenue =
    CALCULATE([Total Revenue],
              RELATED(dim_products[product_category]) = "Electronics")

-- 19. Top Region Revenue
Top Region Revenue =
    MAXX(
        VALUES(fact_orders[region]),
        [Total Revenue]
    )

-- 20. Profit Flag (Good/Average/Poor)
Profit Flag =
    SWITCH(TRUE(),
        [Profit Margin %] >= 50, "Excellent",
        [Profit Margin %] >= 30, "Good",
        [Profit Margin %] >= 15, "Average",
        "Poor"
    )

-- 21. Revenue vs Target (assume ₹3 Cr annual)
Revenue vs Target % =
    DIVIDE([YTD Revenue], 30000000, 0) * 100

-- 22. High Value Orders (> ₹50,000)
High Value Orders =
    COUNTROWS(
        FILTER(fact_orders, fact_orders[revenue] > 50000)
    )
```

---

## 8. KEY INSIGHTS & RECOMMENDATIONS

### Revenue Insights
1. **Electronics dominates** with the highest category revenue, driven by
   Laptops and Monitors. Focus on upselling accessories.
2. **Q4 surge**: October–December accounts for ~35% of annual revenue —
   align marketing budgets and inventory before festive season.
3. **2024 showed positive YoY growth** — investigate which sub-categories
   drove the uptick.

### Regional Insights
4. **North and West regions** are top revenue contributors; Central region
   is under-performing — explore targeted campaigns.
5. **Sales Rep productivity** varies significantly within regions — best
   performers handle 2× the revenue of bottom performers.

### Customer Insights
6. **~60% of customers are one-time buyers** — implement a loyalty programme
   and re-engagement email campaigns to improve retention.
7. **Top 10 customers contribute 25%+ of revenue** — assign dedicated
   account managers to high-value clients.
8. **Average Order Value** is highest in Electronics — bundle deals can
   boost AOV across lower-performing categories.

### Product Insights
9. **Books category** has the lowest revenue but reasonable margins —
   digital/subscription upsell opportunity.
10. **Robot Vacuum Cleaner and Laptop Pro** are star performers —
    ensure perpetual stock availability.

### Recommendations
- Launch a "Summer Sale" campaign targeting the slow May–July period.
- Introduce tiered customer loyalty programme (Bronze → Platinum).
- Set monthly revenue targets per Sales Rep tracked via Power BI dashboard.
- Automate data pipeline with Apache Airflow for daily refresh.

---

## 9. RESUME CONTENT

### Project Description (2 lines)
> Built an end-to-end retail Sales & Revenue Analytics Dashboard processing
> 1,200+ orders using Python (Pandas, NumPy), PostgreSQL (35 SQL queries),
> and Power BI (4-page dashboard with 20+ DAX measures), delivering
> actionable insights on revenue trends, customer segmentation, and KPIs.

### Key Achievements
- Cleaned and enriched 1,250-row raw dataset, resolving duplicates,
  missing values, and data type errors using a structured Pandas pipeline.
- Designed a star-schema PostgreSQL database with 5 tables and wrote
  35 optimised queries covering CTEs, window functions, and business KPIs.
- Created 10 EDA visualisations revealing ₹5.26 Cr total revenue,
  54.7% average profit margin, and Q4 seasonal spikes of 35%.
- Developed an interactive Power BI dashboard with YoY growth, RFM
  segmentation, and running totals refreshable from PostgreSQL.

### Resume Bullet Points
- **Data Engineering:** Designed ETL pipeline (Python → PostgreSQL)
  processing 1,200 retail sales records with automated cleaning & validation.
- **SQL Analytics:** Wrote 35 SQL queries (CTEs, window functions, ranking)
  uncovering 25% customer concentration risk and regional revenue gaps.
- **Visualisation:** Built 4-page Power BI dashboard with 20+ DAX measures
  tracking ₹5.26 Cr revenue, MoM growth, and customer lifetime value.
- **EDA:** Generated 10 Seaborn/Matplotlib charts identifying Q4 revenue
  surge and top-10 products contributing 40% of total revenue.

### How to Explain in an Interview
> "This project simulates a real-world retail analytics scenario. I started
> by generating a 1,200-record dataset with intentional data quality issues,
> then built a Pandas pipeline to clean and enrich it. I loaded the data
> into a PostgreSQL star schema and wrote 35 queries — ranging from basic
> aggregations to advanced window functions and CTEs — to answer business
> questions around revenue growth, customer segmentation, and product
> performance. Finally, I connected PostgreSQL to Power BI and built a
> 4-page dashboard with 20+ DAX measures including YoY growth, YTD revenue,
> and RFM-based customer segments. The project demonstrates the complete
> data analyst workflow from raw data to executive reporting."

---

## 10. INTERVIEW PREPARATION

### A — 20 SQL Interview Questions

**Basic**
1. What is the difference between WHERE and HAVING?
   > WHERE filters rows before aggregation; HAVING filters after GROUP BY.

2. Explain the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN.
   > INNER: only matching rows. LEFT: all left rows + matched right.
   > FULL OUTER: all rows from both tables, NULLs where no match.

3. What does DISTINCT do, and when would you use it?
   > Removes duplicate rows in the result set.

4. What is the difference between DELETE, TRUNCATE, and DROP?
   > DELETE: removes rows (can use WHERE); TRUNCATE: removes all rows
   > fast (no log); DROP: removes the entire table structure.

5. How do you find the second highest revenue in a table?
   > SELECT MAX(revenue) FROM fact_orders
   >   WHERE revenue < (SELECT MAX(revenue) FROM fact_orders);

**Intermediate**
6. What is a CTE and how is it different from a subquery?
   > CTE (Common Table Expression) is a named temporary result set defined
   > with WITH clause. More readable than nested subqueries; can be
   > referenced multiple times.

7. Write a query to find customers who placed orders in both 2023 and 2024.
   > SELECT customer_id FROM fact_orders WHERE year=2023
   > INTERSECT
   > SELECT customer_id FROM fact_orders WHERE year=2024;

8. Explain RANK() vs DENSE_RANK() vs ROW_NUMBER().
   > ROW_NUMBER: unique sequential number even for ties.
   > RANK: same rank for ties, skips next number.
   > DENSE_RANK: same rank for ties, no gaps.

9. What are window functions? Give an example.
   > Functions that perform calculations across a set of rows related to
   > the current row WITHOUT collapsing them into one row.
   > Example: SUM(revenue) OVER (PARTITION BY region ORDER BY order_date)

10. How do you calculate a running total in SQL?
    > SUM(revenue) OVER (ORDER BY order_date
    >     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

**Advanced**
11. What is the difference between NTILE and PERCENT_RANK?
    > NTILE(n) divides rows into n equal buckets.
    > PERCENT_RANK gives relative position as (rank-1)/(total-1).

12. How would you find duplicate rows and remove them?
    > Using ROW_NUMBER() OVER (PARTITION BY key_cols ORDER BY id),
    > then DELETE where row_number > 1.

13. What is query optimisation? How do you improve a slow query?
    > Add appropriate indexes, avoid SELECT *, use EXISTS instead of IN
    > for subqueries, partition large tables, analyse EXPLAIN ANALYZE.

14. Explain the difference between correlated and non-correlated subqueries.
    > Correlated: references outer query (runs once per row — slower).
    > Non-correlated: independent of outer query (runs once).

15. What are indexes? What types exist in PostgreSQL?
    > B-Tree (default, range), Hash (equality), GIN (array/JSON),
    > BRIN (large sequential data), Partial indexes with WHERE.

16. How do you pivot data in SQL without PIVOT keyword?
    > Using conditional aggregation:
    > SUM(CASE WHEN category='Electronics' THEN revenue ELSE 0 END)

17. What is the difference between EXISTS and IN?
    > EXISTS stops at first match (efficient for large datasets).
    > IN evaluates all values. EXISTS is preferred with subqueries.

18. Write a query to get month-over-month growth percentage.
    > Use LAG() window function:
    > (revenue - LAG(revenue) OVER (ORDER BY month)) /
    > LAG(revenue) OVER (ORDER BY month) * 100

19. What is a materialized view? How is it different from a regular view?
    > A materialized view stores the query results physically on disk.
    > Regular views are virtual (re-executed each time).

20. Explain ACID properties in databases.
    > Atomicity (all or nothing), Consistency (valid state),
    > Isolation (concurrent transactions don't interfere),
    > Durability (committed data persists).

---

### B — 20 Python Interview Questions

1. What is the difference between a list and a tuple in Python?
   > List is mutable; tuple is immutable. Tuples are faster.

2. What does df.dropna() vs df.fillna() do?
   > dropna: removes rows/columns with NaN.
   > fillna: replaces NaN with a specified value/method.

3. How do you handle duplicate rows in a DataFrame?
   > df.drop_duplicates() — optionally specify subset of columns.

4. What is the difference between loc and iloc?
   > loc: label-based indexing. iloc: integer position-based indexing.

5. How do you merge two DataFrames in Pandas?
   > pd.merge(df1, df2, on='key', how='inner/left/right/outer')

6. What is groupby() and how does it work?
   > Groups rows by one or more columns; then apply aggregate functions
   > (sum, mean, count) to each group.

7. How do you convert a column to datetime in Pandas?
   > pd.to_datetime(df['date_col'], errors='coerce')

8. What is the apply() function in Pandas?
   > Applies a function along an axis of a DataFrame (row or column).

9. What are lambda functions? Give an example.
   > Anonymous one-line functions: df['col'].apply(lambda x: x*2)

10. How do you handle missing values in a numeric column?
    > df['col'].fillna(df['col'].median(), inplace=True) or
    > df['col'].interpolate()

11. What is the difference between map(), apply(), and applymap()?
    > map: element-wise on Series. apply: row/col on DataFrame.
    > applymap (now map in newer Pandas): element-wise on DataFrame.

12. How do you reshape data using pivot_table()?
    > pd.pivot_table(df, values='revenue', index='region',
    >                columns='quarter', aggfunc='sum')

13. What is NumPy and how is it different from Pandas?
    > NumPy: fast array operations on homogeneous numerical data.
    > Pandas: built on NumPy; handles heterogeneous, labelled data.

14. How do you detect outliers using IQR in Python?
    > Q1, Q3 = df['col'].quantile([0.25, 0.75])
    > IQR = Q3 - Q1
    > outliers = df[(df['col'] < Q1-1.5*IQR) | (df['col'] > Q3+1.5*IQR)]

15. What is the difference between deep copy and shallow copy?
    > Shallow copy: references same objects. Deep copy: creates new objects.
    > Use df.copy() (deep=True) for Pandas DataFrames.

16. How do you read/write CSV files in Pandas?
    > pd.read_csv('file.csv') / df.to_csv('file.csv', index=False)

17. What does value_counts() do?
    > Returns a Series with unique value frequencies in descending order.

18. How do you create calculated columns in Pandas?
    > df['profit'] = df['revenue'] - df['cost']

19. What is SQLAlchemy and how is it used with Pandas?
    > Python SQL toolkit/ORM. Used with pd.read_sql() and df.to_sql()
    > to read/write DataFrames directly to/from databases.

20. How would you optimise a slow Pandas operation on 1M+ rows?
    > Use vectorised operations instead of apply/loops.
    > Use Dask for parallel processing. Use appropriate dtypes
    > (e.g. category dtype). Use chunksize in read_csv.

---

### C — 20 Power BI Interview Questions

1. What is the difference between a Measure and a Calculated Column?
   > Measures are computed at query time (dynamic). Calculated columns
   > are computed at refresh time and stored in the model.

2. What does CALCULATE() do in DAX?
   > Evaluates an expression in a modified filter context.
   > Most important DAX function.

3. Explain the difference between ALL() and ALLEXCEPT().
   > ALL() removes all filters from a table/column.
   > ALLEXCEPT() removes all filters EXCEPT specified columns.

4. What is the difference between SUMX and SUM?
   > SUM aggregates an existing column.
   > SUMX iterates row-by-row and evaluates an expression first.

5. What are Slicers and how are they different from Filters?
   > Slicers are visual filters on the canvas. Report/page/visual
   > filters are in the Filters pane. Both change filter context.

6. What is the Star Schema and why is it used in Power BI?
   > Central fact table connected to multiple dimension tables.
   > Simplifies relationships, improves query performance.

7. How do you create YTD (Year-to-Date) measures in DAX?
   > TOTALYTD([Measure], DimDate[Date])

8. What is the role of a Date Table in Power BI?
   > Required for time intelligence functions (SAMEPERIODLASTYEAR,
   > TOTALYTD, etc.). Must be marked as Date Table.

9. What is DirectQuery vs Import mode?
   > Import: data copied into Power BI (faster, limited size).
   > DirectQuery: queries sent live to source (always fresh, slower).

10. How do you handle many-to-many relationships in Power BI?
    > Use a bridge table to break M:M into two 1:M relationships,
    > or use composite models in Power BI.

11. Explain RELATED() and RELATEDTABLE().
    > RELATED(): returns a value from a related table (many-to-one).
    > RELATEDTABLE(): returns a table of related rows (one-to-many).

12. What is context transition in DAX?
    > When a measure is used inside an iterator (SUMX, FILTER),
    > row context is automatically converted to filter context.

13. How do you show % of total in a visual?
    > Measure = DIVIDE([Sales], CALCULATE([Sales], ALL(Table)))

14. What is the difference between FILTER() and CALCULATETABLE()?
    > FILTER: row-by-row filtering of a table.
    > CALCULATETABLE: applies filter context modifications.

15. What is Row-Level Security (RLS) in Power BI?
    > Restricts data access for specific users by defining roles
    > with DAX filter expressions.

16. How do you create a dynamic title in Power BI?
    > Use a measure returning text, then set visual title to
    > "Field Value" and select that measure.

17. What are Bookmarks in Power BI?
    > Saved states of a page (filters, visuals, slicers).
    > Used for storytelling, navigation buttons, toggle effects.

18. What is the USERELATIONSHIP() function?
    > Activates an inactive relationship between two tables within
    > a CALCULATE expression.

19. How do you create a Rolling 3-Month Average in DAX?
    > CALCULATE([Revenue],
    >     DATESINPERIOD(DimDate[Date], LASTDATE(DimDate[Date]), -3, MONTH))

20. What is a waterfall chart and when would you use it?
    > Shows incremental positive/negative values building up to a total.
    > Used to visualise profit breakdown or budget variance.

---

### D — Project-Based Interview Questions

**Q: Walk me through your project from start to finish.**
> "I designed it as a full data analyst workflow. First, I generated 1,250
> records of synthetic retail sales data with realistic issues — missing
> values, duplicates, inconsistent casing, and invalid dates. Then I cleaned
> it using a Pandas pipeline, reducing to 1,200 high-quality rows with 22
> columns including derived fields like profit margin, revenue tier, and
> calendar dimensions. Next I ran EDA, generating 10 charts covering
> monthly trends, regional heatmaps, and customer segmentation. I loaded
> the data into a PostgreSQL star schema and wrote 35 queries covering
> everything from basic aggregations to CTEs and window functions. Finally,
> I connected Power BI to PostgreSQL and built a 4-page dashboard with 22
> DAX measures."

**Q: What data quality issues did you encounter and how did you fix them?**
> "Six types: (1) Missing values — imputed Region from Sales Rep mapping,
> Product Category from Product Name lookup, Quantity from median.
> (2) 45 duplicate rows — removed with drop_duplicates().
> (3) Quantity stored as strings ('N/A', 'unknown') — coerced to numeric
> with pd.to_numeric(errors='coerce').
> (4) Mixed case in Region column — standardised with str.title().
> (5) 10 rows with negative/zero Revenue — recalculated from Unit Price ×
> Quantity. (6) 5 future dates — set to NaT and dropped from analysis."

**Q: What was your most interesting insight from the EDA?**
> "The Q4 seasonal spike — October to December contributed approximately
> 35% of annual revenue. This aligns with Diwali, Christmas, and year-end
> spending. Also, the Electronics category had the highest absolute revenue
> but Books had a comparable profit margin percentage, suggesting Books is
> a high-efficiency low-volume category worth exploring for digital/
> subscription upsell."

**Q: Why did you choose a star schema for PostgreSQL?**
> "Star schema separates concerns: the fact table holds measurable events
> (orders) while dimension tables hold descriptive attributes (customers,
> products, regions). This design reduces redundancy, simplifies JOIN
> queries, and mirrors exactly how Power BI expects data — with
> one-to-many relationships from dimensions to facts. It also makes
> adding new dimensions (e.g., a date dimension for time intelligence)
> straightforward."

**Q: Explain one of your complex SQL queries.**
> "Query 20 uses a CTE to compute RFM scores — Recency, Frequency, and
> Monetary value — for each customer. I first aggregate order counts,
> total revenue, and days since last purchase. Then I use NTILE(4) window
> functions to rank each customer into quartiles on all three dimensions.
> Finally, I sum the three scores and classify customers as Champion,
> Loyal, Potential Loyalist, or At Risk. This directly mirrors how
> marketing teams segment customers for targeted campaigns."
