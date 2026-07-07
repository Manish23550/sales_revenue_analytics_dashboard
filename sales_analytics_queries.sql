-- =============================================================
--  Sales & Revenue Analytics Dashboard
--  Task 4: PostgreSQL Database — Schema + 30+ SQL Queries
--  Database: sales_analytics
-- =============================================================

-- ─── 0. DATABASE SETUP ───────────────────────────────────────
-- Run in psql as superuser:
-- CREATE DATABASE sales_analytics;
-- \c sales_analytics

-- ─── 1. CREATE SCHEMA & TABLES ───────────────────────────────

CREATE SCHEMA IF NOT EXISTS sales;

DROP TABLE IF EXISTS sales.fact_orders CASCADE;
DROP TABLE IF EXISTS sales.dim_customers CASCADE;
DROP TABLE IF EXISTS sales.dim_products  CASCADE;
DROP TABLE IF EXISTS sales.dim_regions   CASCADE;
DROP TABLE IF EXISTS sales.dim_reps      CASCADE;
DROP TABLE IF EXISTS sales.dim_date      CASCADE;

-- Dimension: Customers
CREATE TABLE sales.dim_customers (
    customer_id   VARCHAR(10)  PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL
);

-- Dimension: Products
CREATE TABLE sales.dim_products (
    product_name     VARCHAR(100) PRIMARY KEY,
    product_category VARCHAR(50)  NOT NULL
);

-- Dimension: Regions
CREATE TABLE sales.dim_regions (
    region_id   SERIAL       PRIMARY KEY,
    region_name VARCHAR(50)  UNIQUE NOT NULL
);

-- Dimension: Sales Reps
CREATE TABLE sales.dim_reps (
    rep_id   SERIAL       PRIMARY KEY,
    rep_name VARCHAR(100) UNIQUE NOT NULL,
    region   VARCHAR(50)
);

-- Dimension: Date
CREATE TABLE sales.dim_date (
    date_key    DATE PRIMARY KEY,
    year        INT,
    quarter     VARCHAR(2),
    month       INT,
    month_name  VARCHAR(15),
    week_number INT,
    day_of_week VARCHAR(10)
);

-- Fact: Orders
CREATE TABLE sales.fact_orders (
    order_id         VARCHAR(15)    PRIMARY KEY,
    order_date       DATE           NOT NULL,
    customer_id      VARCHAR(10)    REFERENCES sales.dim_customers(customer_id),
    product_name     VARCHAR(100)   REFERENCES sales.dim_products(product_name),
    sales_rep        VARCHAR(100),
    region           VARCHAR(50),
    quantity         INT            NOT NULL CHECK (quantity > 0),
    unit_price       NUMERIC(12,2)  NOT NULL,
    revenue          NUMERIC(12,2)  NOT NULL,
    cost             NUMERIC(12,2)  NOT NULL,
    profit           NUMERIC(12,2)  NOT NULL,
    profit_margin    NUMERIC(6,2),
    revenue_tier     VARCHAR(20),
    year             INT,
    month            INT,
    month_name       VARCHAR(15),
    quarter          VARCHAR(2),
    day_of_week      VARCHAR(10),
    week_number      INT,
    created_at       TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_orders_date     ON sales.fact_orders(order_date);
CREATE INDEX idx_orders_region   ON sales.fact_orders(region);
CREATE INDEX idx_orders_category ON sales.fact_orders(product_name);
CREATE INDEX idx_orders_customer ON sales.fact_orders(customer_id);

-- ─── 2. IMPORT DATA (via psql COPY) ──────────────────────────
-- Run after exporting cleaned CSV:
--
-- COPY sales.dim_customers(customer_id, customer_name)
-- SELECT DISTINCT customer_id, customer_name FROM staging;
--
-- Or use Python script:
-- python scripts/04_load_to_postgres.py

-- ─── 3. VERIFY DATA ──────────────────────────────────────────
SELECT COUNT(*) AS total_orders FROM sales.fact_orders;
SELECT MIN(order_date), MAX(order_date) FROM sales.fact_orders;


-- =============================================================
--  30+ ANALYTICAL SQL QUERIES
-- =============================================================

-- ────────────────────────────────────────────────────────────
-- SECTION A: BASIC SELECT & FILTER (Queries 1–5)
-- ────────────────────────────────────────────────────────────

-- Q1: All orders from 2024 sorted by Revenue descending
SELECT
    order_id,
    order_date,
    customer_id,
    product_name,
    region,
    quantity,
    revenue,
    profit
FROM sales.fact_orders
WHERE EXTRACT(YEAR FROM order_date) = 2024
ORDER BY revenue DESC;


-- Q2: Orders with Revenue > ₹50,000
SELECT
    order_id,
    order_date,
    customer_id,
    product_name,
    revenue,
    profit,
    profit_margin
FROM sales.fact_orders
WHERE revenue > 50000
ORDER BY revenue DESC;


-- Q3: All orders from the 'Electronics' category in North region
SELECT
    fo.order_id,
    fo.order_date,
    dc.customer_name,
    dp.product_category,
    fo.product_name,
    fo.quantity,
    fo.revenue
FROM sales.fact_orders fo
JOIN sales.dim_customers dc ON fo.customer_id = dc.customer_id
JOIN sales.dim_products  dp ON fo.product_name = dp.product_name
WHERE dp.product_category = 'Electronics'
  AND fo.region = 'North'
ORDER BY fo.order_date;


-- Q4: Orders placed on weekends
SELECT
    order_id,
    order_date,
    day_of_week,
    revenue
FROM sales.fact_orders
WHERE day_of_week IN ('Saturday', 'Sunday')
ORDER BY order_date;


-- Q5: Low-margin orders (profit margin < 20%)
SELECT
    order_id,
    order_date,
    product_name,
    revenue,
    cost,
    profit,
    profit_margin
FROM sales.fact_orders
WHERE profit_margin < 20
ORDER BY profit_margin ASC;


-- ────────────────────────────────────────────────────────────
-- SECTION B: AGGREGATION & GROUP BY (Queries 6–12)
-- ────────────────────────────────────────────────────────────

-- Q6: Total Revenue, Profit, and Orders per Region
SELECT
    region,
    COUNT(order_id)                              AS total_orders,
    SUM(revenue)                                 AS total_revenue,
    SUM(profit)                                  AS total_profit,
    ROUND(AVG(profit_margin), 2)                 AS avg_profit_margin,
    ROUND(SUM(profit) / NULLIF(SUM(revenue),0) * 100, 2) AS overall_margin_pct
FROM sales.fact_orders
GROUP BY region
ORDER BY total_revenue DESC;


-- Q7: Monthly Revenue Trend
SELECT
    year,
    month,
    month_name,
    COUNT(order_id)        AS orders,
    SUM(quantity)          AS units_sold,
    ROUND(SUM(revenue),2)  AS revenue,
    ROUND(SUM(profit),2)   AS profit,
    ROUND(AVG(profit_margin),2) AS avg_margin
FROM sales.fact_orders
GROUP BY year, month, month_name
ORDER BY year, month;


-- Q8: Revenue by Product Category
SELECT
    dp.product_category,
    COUNT(fo.order_id)          AS total_orders,
    SUM(fo.quantity)            AS units_sold,
    ROUND(SUM(fo.revenue), 2)   AS total_revenue,
    ROUND(SUM(fo.profit),  2)   AS total_profit,
    ROUND(AVG(fo.profit_margin),2) AS avg_margin_pct
FROM sales.fact_orders fo
JOIN sales.dim_products dp ON fo.product_name = dp.product_name
GROUP BY dp.product_category
ORDER BY total_revenue DESC;


-- Q9: Top 10 Products by Revenue
SELECT
    product_name,
    COUNT(order_id)           AS times_ordered,
    SUM(quantity)             AS units_sold,
    ROUND(SUM(revenue), 2)    AS total_revenue,
    ROUND(SUM(profit),  2)    AS total_profit
FROM sales.fact_orders
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;


-- Q10: Sales Rep Leaderboard
SELECT
    sales_rep,
    region,
    COUNT(order_id)          AS total_orders,
    ROUND(SUM(revenue), 2)   AS total_revenue,
    ROUND(SUM(profit),  2)   AS total_profit,
    ROUND(AVG(revenue), 2)   AS avg_order_value
FROM sales.fact_orders
GROUP BY sales_rep, region
ORDER BY total_revenue DESC;


-- Q11: Quarterly Performance
SELECT
    year,
    quarter,
    ROUND(SUM(revenue), 2) AS quarterly_revenue,
    ROUND(SUM(profit),  2) AS quarterly_profit,
    COUNT(order_id)        AS orders
FROM sales.fact_orders
GROUP BY year, quarter
ORDER BY year, quarter;


-- Q12: Revenue Tier Distribution
SELECT
    revenue_tier,
    COUNT(*)                 AS order_count,
    ROUND(SUM(revenue), 2)  AS total_revenue,
    ROUND(AVG(revenue), 2)  AS avg_revenue
FROM sales.fact_orders
GROUP BY revenue_tier
ORDER BY total_revenue DESC;


-- ────────────────────────────────────────────────────────────
-- SECTION C: HAVING (Queries 13–15)
-- ────────────────────────────────────────────────────────────

-- Q13: Customers with total spending > ₹500,000
SELECT
    dc.customer_name,
    COUNT(fo.order_id)         AS total_orders,
    ROUND(SUM(fo.revenue), 2)  AS total_spent,
    ROUND(AVG(fo.revenue), 2)  AS avg_order_value
FROM sales.fact_orders fo
JOIN sales.dim_customers dc ON fo.customer_id = dc.customer_id
GROUP BY dc.customer_name
HAVING SUM(fo.revenue) > 500000
ORDER BY total_spent DESC;


-- Q14: Products ordered more than 50 times
SELECT
    product_name,
    COUNT(order_id)  AS order_count,
    SUM(quantity)    AS total_units,
    SUM(revenue)     AS total_revenue
FROM sales.fact_orders
GROUP BY product_name
HAVING COUNT(order_id) > 50
ORDER BY order_count DESC;


-- Q15: Regions with avg profit margin > 50%
SELECT
    region,
    ROUND(AVG(profit_margin), 2) AS avg_margin_pct,
    COUNT(order_id)              AS orders,
    SUM(revenue)                 AS revenue
FROM sales.fact_orders
GROUP BY region
HAVING AVG(profit_margin) > 50
ORDER BY avg_margin_pct DESC;


-- ────────────────────────────────────────────────────────────
-- SECTION D: JOINS (Queries 16–18)
-- ────────────────────────────────────────────────────────────

-- Q16: Full Order Detail Report (multi-table JOIN)
SELECT
    fo.order_id,
    fo.order_date,
    dc.customer_name,
    dp.product_category,
    fo.product_name,
    fo.region,
    fo.sales_rep,
    fo.quantity,
    fo.unit_price,
    fo.revenue,
    fo.profit,
    fo.profit_margin
FROM sales.fact_orders  fo
JOIN sales.dim_customers dc ON fo.customer_id  = dc.customer_id
JOIN sales.dim_products  dp ON fo.product_name = dp.product_name
ORDER BY fo.order_date DESC;


-- Q17: Customer purchase history with category breakdown
SELECT
    dc.customer_name,
    dp.product_category,
    COUNT(fo.order_id)          AS orders,
    SUM(fo.quantity)            AS units,
    ROUND(SUM(fo.revenue), 2)   AS revenue
FROM sales.fact_orders  fo
JOIN sales.dim_customers dc ON fo.customer_id  = dc.customer_id
JOIN sales.dim_products  dp ON fo.product_name = dp.product_name
GROUP BY dc.customer_name, dp.product_category
ORDER BY dc.customer_name, revenue DESC;


-- Q18: Sales Reps with their region and performance
SELECT
    dr.rep_name,
    dr.region,
    COUNT(fo.order_id)           AS orders,
    ROUND(SUM(fo.revenue),  2)   AS revenue,
    ROUND(SUM(fo.profit),   2)   AS profit,
    ROUND(AVG(fo.profit_margin), 2) AS avg_margin
FROM sales.dim_reps dr
LEFT JOIN sales.fact_orders fo ON dr.rep_name = fo.sales_rep
GROUP BY dr.rep_name, dr.region
ORDER BY revenue DESC NULLS LAST;


-- ────────────────────────────────────────────────────────────
-- SECTION E: CTEs (Queries 19–22)
-- ────────────────────────────────────────────────────────────

-- Q19: CTE — Monthly Revenue with MoM Growth
WITH monthly_revenue AS (
    SELECT
        year,
        month,
        month_name,
        SUM(revenue) AS revenue
    FROM sales.fact_orders
    GROUP BY year, month, month_name
),
with_growth AS (
    SELECT
        year,
        month,
        month_name,
        revenue,
        LAG(revenue) OVER (ORDER BY year, month) AS prev_month_revenue
    FROM monthly_revenue
)
SELECT
    year,
    month,
    month_name,
    ROUND(revenue, 2)          AS revenue,
    ROUND(prev_month_revenue, 2) AS prev_revenue,
    ROUND(
        (revenue - prev_month_revenue) / NULLIF(prev_month_revenue, 0) * 100, 2
    ) AS mom_growth_pct
FROM with_growth
ORDER BY year, month;


-- Q20: CTE — Customer RFM Segmentation
WITH customer_stats AS (
    SELECT
        dc.customer_name,
        COUNT(fo.order_id)          AS frequency,
        ROUND(SUM(fo.revenue), 2)   AS monetary,
        MAX(fo.order_date)          AS last_order_date,
        CURRENT_DATE - MAX(fo.order_date)::DATE AS recency_days
    FROM sales.fact_orders fo
    JOIN sales.dim_customers dc ON fo.customer_id = dc.customer_id
    GROUP BY dc.customer_name
),
rfm AS (
    SELECT
        customer_name,
        frequency,
        monetary,
        recency_days,
        NTILE(4) OVER (ORDER BY recency_days  ASC)  AS r_score,
        NTILE(4) OVER (ORDER BY frequency     DESC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary      DESC) AS m_score
    FROM customer_stats
)
SELECT
    customer_name,
    frequency,
    monetary,
    recency_days,
    r_score, f_score, m_score,
    (r_score + f_score + m_score) AS rfm_total,
    CASE
        WHEN (r_score + f_score + m_score) >= 10 THEN 'Champion'
        WHEN (r_score + f_score + m_score) >= 7  THEN 'Loyal Customer'
        WHEN (r_score + f_score + m_score) >= 5  THEN 'Potential Loyalist'
        ELSE 'At Risk'
    END AS customer_segment
FROM rfm
ORDER BY rfm_total DESC;


-- Q21: CTE — Category Contribution to Total Revenue
WITH category_rev AS (
    SELECT
        dp.product_category,
        SUM(fo.revenue) AS cat_revenue
    FROM sales.fact_orders fo
    JOIN sales.dim_products dp ON fo.product_name = dp.product_name
    GROUP BY dp.product_category
),
total AS (
    SELECT SUM(cat_revenue) AS grand_total FROM category_rev
)
SELECT
    cr.product_category,
    ROUND(cr.cat_revenue, 2) AS revenue,
    ROUND(cr.cat_revenue / t.grand_total * 100, 2) AS pct_of_total
FROM category_rev cr
CROSS JOIN total t
ORDER BY revenue DESC;


-- Q22: CTE — Running Revenue Target (assume ₹3 Cr annual target)
WITH monthly AS (
    SELECT
        year, month, month_name,
        SUM(revenue) AS monthly_rev
    FROM sales.fact_orders
    WHERE year = 2024
    GROUP BY year, month, month_name
)
SELECT
    month,
    month_name,
    ROUND(monthly_rev, 2)               AS monthly_revenue,
    ROUND(SUM(monthly_rev) OVER (ORDER BY month), 2) AS ytd_revenue,
    30000000                            AS annual_target,
    ROUND(SUM(monthly_rev) OVER (ORDER BY month) / 30000000 * 100, 2) AS target_achieved_pct
FROM monthly
ORDER BY month;


-- ────────────────────────────────────────────────────────────
-- SECTION F: WINDOW FUNCTIONS (Queries 23–27)
-- ────────────────────────────────────────────────────────────

-- Q23: Running Total Revenue (cumulative)
SELECT
    order_date,
    order_id,
    revenue,
    ROUND(SUM(revenue) OVER (ORDER BY order_date, order_id
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2)
        AS running_total_revenue
FROM sales.fact_orders
ORDER BY order_date;


-- Q24: Revenue Rank by Region
SELECT
    order_id,
    order_date,
    region,
    product_name,
    revenue,
    RANK()       OVER (PARTITION BY region ORDER BY revenue DESC) AS rank_in_region,
    DENSE_RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS dense_rank_region
FROM sales.fact_orders
ORDER BY region, rank_in_region;


-- Q25: Moving Average (3-month rolling revenue)
WITH monthly AS (
    SELECT
        year, month,
        SUM(revenue) AS monthly_rev
    FROM sales.fact_orders
    GROUP BY year, month
)
SELECT
    year, month,
    ROUND(monthly_rev, 2) AS revenue,
    ROUND(AVG(monthly_rev) OVER (
        ORDER BY year, month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_3m_avg
FROM monthly
ORDER BY year, month;


-- Q26: Percentile Rank of Orders by Revenue
SELECT
    order_id,
    revenue,
    ROUND(PERCENT_RANK() OVER (ORDER BY revenue) * 100, 2) AS percentile_rank,
    NTILE(4) OVER (ORDER BY revenue)                        AS quartile
FROM sales.fact_orders
ORDER BY revenue DESC;


-- Q27: First and Last Order per Customer
SELECT DISTINCT
    customer_id,
    FIRST_VALUE(order_date) OVER (
        PARTITION BY customer_id ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS first_order_date,
    LAST_VALUE(order_date)  OVER (
        PARTITION BY customer_id ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_order_date,
    COUNT(order_id) OVER (PARTITION BY customer_id)               AS total_orders
FROM sales.fact_orders
ORDER BY total_orders DESC;


-- ────────────────────────────────────────────────────────────
-- SECTION G: RANKING FUNCTIONS (Queries 28–30)
-- ────────────────────────────────────────────────────────────

-- Q28: Top 5 products per category by Revenue
WITH ranked AS (
    SELECT
        dp.product_category,
        fo.product_name,
        ROUND(SUM(fo.revenue), 2) AS total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY dp.product_category
            ORDER BY SUM(fo.revenue) DESC
        ) AS rn
    FROM sales.fact_orders fo
    JOIN sales.dim_products dp ON fo.product_name = dp.product_name
    GROUP BY dp.product_category, fo.product_name
)
SELECT product_category, product_name, total_revenue, rn AS rank
FROM ranked
WHERE rn <= 5
ORDER BY product_category, rank;


-- Q29: Region Rank by Quarter
SELECT
    region,
    quarter,
    year,
    ROUND(SUM(revenue), 2) AS quarterly_revenue,
    RANK() OVER (
        PARTITION BY quarter, year
        ORDER BY SUM(revenue) DESC
    ) AS rank_in_quarter
FROM sales.fact_orders
GROUP BY region, quarter, year
ORDER BY year, quarter, rank_in_quarter;


-- Q30: Top 3 Sales Reps per Region
WITH rep_perf AS (
    SELECT
        region,
        sales_rep,
        ROUND(SUM(revenue), 2) AS revenue,
        ROW_NUMBER() OVER (
            PARTITION BY region
            ORDER BY SUM(revenue) DESC
        ) AS rn
    FROM sales.fact_orders
    WHERE sales_rep <> 'Unknown Rep'
    GROUP BY region, sales_rep
)
SELECT region, sales_rep, revenue, rn AS rank
FROM rep_perf
WHERE rn <= 3
ORDER BY region, rank;


-- ────────────────────────────────────────────────────────────
-- SECTION H: BUSINESS KPI QUERIES (Queries 31–35)
-- ────────────────────────────────────────────────────────────

-- Q31: Overall Business KPIs
SELECT
    COUNT(order_id)                                   AS total_orders,
    COUNT(DISTINCT customer_id)                       AS unique_customers,
    ROUND(SUM(revenue), 2)                            AS total_revenue,
    ROUND(SUM(profit),  2)                            AS total_profit,
    ROUND(AVG(revenue), 2)                            AS avg_order_value,
    ROUND(SUM(profit) / NULLIF(SUM(revenue),0) * 100, 2) AS overall_profit_margin_pct,
    ROUND(SUM(revenue) / COUNT(DISTINCT customer_id), 2)  AS revenue_per_customer
FROM sales.fact_orders;


-- Q32: YoY Revenue Growth (2023 vs 2024)
WITH yearly AS (
    SELECT
        year,
        SUM(revenue) AS annual_revenue,
        SUM(profit)  AS annual_profit
    FROM sales.fact_orders
    GROUP BY year
)
SELECT
    year,
    ROUND(annual_revenue, 2) AS revenue,
    ROUND(annual_profit,  2) AS profit,
    ROUND(
        (annual_revenue - LAG(annual_revenue) OVER (ORDER BY year))
        / NULLIF(LAG(annual_revenue) OVER (ORDER BY year), 0) * 100, 2
    ) AS yoy_revenue_growth_pct
FROM yearly;


-- Q33: Customer Lifetime Value (CLV) Approximation
SELECT
    dc.customer_name,
    COUNT(fo.order_id)                   AS purchase_count,
    ROUND(SUM(fo.revenue), 2)            AS lifetime_revenue,
    ROUND(AVG(fo.revenue), 2)            AS avg_order_value,
    ROUND(SUM(fo.profit),  2)            AS lifetime_profit,
    ROUND(AVG(fo.profit_margin), 2)      AS avg_margin_pct
FROM sales.fact_orders fo
JOIN sales.dim_customers dc ON fo.customer_id = dc.customer_id
GROUP BY dc.customer_name
ORDER BY lifetime_revenue DESC
LIMIT 20;


-- Q34: Repeat vs One-time Customers
WITH cust_orders AS (
    SELECT customer_id, COUNT(order_id) AS order_count
    FROM sales.fact_orders
    GROUP BY customer_id
)
SELECT
    CASE WHEN order_count = 1 THEN 'One-time' ELSE 'Repeat' END AS customer_type,
    COUNT(*) AS customer_count,
    ROUND(AVG(order_count), 2) AS avg_orders
FROM cust_orders
GROUP BY 1;


-- Q35: Low Performing Products (< ₹50,000 Total Revenue)
SELECT
    fo.product_name,
    dp.product_category,
    COUNT(fo.order_id)         AS orders,
    ROUND(SUM(fo.revenue), 2)  AS total_revenue,
    ROUND(AVG(fo.profit_margin), 2) AS avg_margin
FROM sales.fact_orders fo
JOIN sales.dim_products dp ON fo.product_name = dp.product_name
GROUP BY fo.product_name, dp.product_category
HAVING SUM(fo.revenue) < 50000
ORDER BY total_revenue ASC;

-- =============================================================
-- END OF SQL SCRIPTS
-- Total Queries: 35 (Basic: 5, Aggregation: 7, HAVING: 3,
--                    JOINs: 3, CTEs: 4, Window: 5,
--                    Ranking: 3, KPIs: 5)
-- =============================================================
