"""
Sales & Revenue Analytics Dashboard
Task 3: Exploratory Data Analysis (EDA)
Generates comprehensive visualisations using Matplotlib & Seaborn.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from matplotlib.gridspec import GridSpec
import os, warnings
warnings.filterwarnings("ignore")

# ─── Setup ───────────────────────────────────────────────────────────────────
df = pd.read_csv("../data/cleaned/sales_cleaned.csv", parse_dates=["Order_Date"])
os.makedirs("../eda", exist_ok=True)

PALETTE   = ["#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
BG_COLOR  = "#F8FAFC"
TEXT_COL  = "#1E293B"

plt.rcParams.update({
    "figure.facecolor": BG_COLOR,
    "axes.facecolor":   BG_COLOR,
    "text.color":       TEXT_COL,
    "axes.labelcolor":  TEXT_COL,
    "xtick.color":      TEXT_COL,
    "ytick.color":      TEXT_COL,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "font.family":      "DejaVu Sans",
})

def fmt_inr(x, pos=None):
    if x >= 1e7:  return f"₹{x/1e7:.1f}Cr"
    if x >= 1e5:  return f"₹{x/1e5:.1f}L"
    return f"₹{x:,.0f}"

def save(fig, name):
    path = f"../eda/{name}.png"
    fig.savefig(path, dpi=140, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  ✅ Saved: {path}")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 1 — KPI Overview
# ═══════════════════════════════════════════════════════════════════════════
print("\n[EDA 1] KPI Overview")
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
fig.suptitle("Sales & Revenue Analytics — KPI Overview", fontsize=16,
             fontweight="bold", y=1.02)

kpis = [
    ("Total Revenue",    f"₹{df['Revenue'].sum()/1e7:.2f} Cr",  PALETTE[0]),
    ("Total Profit",     f"₹{df['Profit'].sum()/1e7:.2f} Cr",   PALETTE[1]),
    ("Avg Profit Margin",f"{df['Profit_Margin_%'].mean():.1f}%", PALETTE[2]),
    ("Total Orders",     f"{len(df):,}",                          PALETTE[4]),
]
for ax, (label, val, col) in zip(axes, kpis):
    ax.set_facecolor(col)
    ax.text(0.5, 0.6, val, transform=ax.transAxes, fontsize=22, fontweight="bold",
            ha="center", va="center", color="white")
    ax.text(0.5, 0.25, label, transform=ax.transAxes, fontsize=11,
            ha="center", va="center", color="white", alpha=0.9)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values(): spine.set_visible(False)
plt.tight_layout()
save(fig, "01_kpi_overview")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 2 — Monthly Revenue Trend
# ═══════════════════════════════════════════════════════════════════════════
print("[EDA 2] Monthly Revenue Trend")
monthly = df.groupby(["Year", "Month"])["Revenue"].sum().reset_index()
monthly["Period"] = monthly["Year"].astype(str) + "-" + monthly["Month"].astype(str).str.zfill(2)
monthly = monthly.sort_values("Period")

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(monthly["Period"], monthly["Revenue"]/1e5, marker="o",
        color=PALETTE[0], linewidth=2.5, markersize=5)
ax.fill_between(monthly["Period"], monthly["Revenue"]/1e5, alpha=0.15, color=PALETTE[0])
ax.set_title("Monthly Revenue Trend (2023–2024)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Month"); ax.set_ylabel("Revenue (₹ Lakhs)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
save(fig, "02_monthly_revenue_trend")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 3 — Revenue & Profit by Category
# ═══════════════════════════════════════════════════════════════════════════
print("[EDA 3] Revenue & Profit by Category")
cat = df.groupby("Product_Category")[["Revenue", "Profit"]].sum().sort_values("Revenue", ascending=True)

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(cat))
w = 0.38
ax.barh(x - w/2, cat["Revenue"]/1e5, w, label="Revenue", color=PALETTE[0])
ax.barh(x + w/2, cat["Profit"]/1e5,  w, label="Profit",  color=PALETTE[1])
ax.set_yticks(x); ax.set_yticklabels(cat.index)
ax.set_title("Revenue & Profit by Product Category", fontsize=14, fontweight="bold")
ax.set_xlabel("Amount (₹ Lakhs)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
ax.legend()
plt.tight_layout()
save(fig, "03_revenue_profit_by_category")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 4 — Regional Performance
# ═══════════════════════════════════════════════════════════════════════════
print("[EDA 4] Regional Performance")
region = df.groupby("Region")[["Revenue", "Profit"]].sum().reset_index()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Regional Performance", fontsize=14, fontweight="bold")

axes[0].bar(region["Region"], region["Revenue"]/1e5, color=PALETTE)
axes[0].set_title("Revenue by Region"); axes[0].set_ylabel("₹ Lakhs")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))

wedges, texts, autotexts = axes[1].pie(
    region["Profit"], labels=region["Region"],
    colors=PALETTE, autopct="%1.1f%%", startangle=140,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5}
)
axes[1].set_title("Profit Share by Region")
plt.tight_layout()
save(fig, "04_regional_performance")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 5 — Top 10 Products
# ═══════════════════════════════════════════════════════════════════════════
print("[EDA 5] Top 10 Products by Revenue")
top_products = df.groupby("Product_Name")["Revenue"].sum().nlargest(10).sort_values()

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_products.index, top_products.values/1e5,
               color=sns.color_palette("Blues_d", 10))
for bar, val in zip(bars, top_products.values/1e5):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f"₹{val:.0f}L", va="center", fontsize=9)
ax.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
ax.set_xlabel("Revenue (₹ Lakhs)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
plt.tight_layout()
save(fig, "05_top_products")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 6 — Customer Segmentation (RFM-style)
# ═══════════════════════════════════════════════════════════════════════════
print("[EDA 6] Customer Segmentation")
cust = df.groupby("Customer_Name").agg(
    Orders=("Order_ID", "count"),
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum")
).reset_index()

cust["Segment"] = pd.cut(cust["Revenue"],
    bins=[0, 100000, 500000, 1500000, np.inf],
    labels=["Bronze", "Silver", "Gold", "Platinum"])

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Customer Segmentation", fontsize=14, fontweight="bold")

seg_counts = cust["Segment"].value_counts()
axes[0].pie(seg_counts, labels=seg_counts.index,
            colors=["#CD7F32", "#C0C0C0", "#FFD700", "#E5E4E2"],
            autopct="%1.1f%%", startangle=140,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5})
axes[0].set_title("Customer Segment Distribution")

top_cust = cust.nlargest(10, "Revenue")
axes[1].bar(top_cust["Customer_Name"], top_cust["Revenue"]/1e5, color=PALETTE[0])
axes[1].set_title("Top 10 Customers by Revenue")
axes[1].set_ylabel("₹ Lakhs")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
save(fig, "06_customer_segmentation")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 7 — Heatmap: Month × Category
# ═══════════════════════════════════════════════════════════════════════════
print("[EDA 7] Revenue Heatmap")
pivot = df.pivot_table(index="Product_Category", columns="Month_Name",
                        values="Revenue", aggfunc="sum")
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
pivot = pivot[[m for m in month_order if m in pivot.columns]]

fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(pivot/1e5, annot=True, fmt=".0f", cmap="Blues",
            linewidths=0.4, ax=ax, cbar_kws={"label": "₹ Lakhs"})
ax.set_title("Revenue Heatmap — Category × Month (₹ Lakhs)",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("Category")
plt.tight_layout()
save(fig, "07_revenue_heatmap")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 8 — Profit Margin Distribution
# ═══════════════════════════════════════════════════════════════════════════
print("[EDA 8] Profit Margin Distribution")
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Profit Margin Analysis", fontsize=14, fontweight="bold")

axes[0].hist(df["Profit_Margin_%"], bins=30, color=PALETTE[1], edgecolor="white")
axes[0].axvline(df["Profit_Margin_%"].mean(), color="red", linestyle="--",
                label=f"Mean: {df['Profit_Margin_%'].mean():.1f}%")
axes[0].set_title("Profit Margin Distribution")
axes[0].set_xlabel("Profit Margin (%)"); axes[0].set_ylabel("Frequency")
axes[0].legend()

pm_cat = df.groupby("Product_Category")["Profit_Margin_%"].mean().sort_values()
axes[1].barh(pm_cat.index, pm_cat.values, color=PALETTE[2])
axes[1].set_title("Avg Profit Margin by Category")
axes[1].set_xlabel("Profit Margin (%)")
for i, v in enumerate(pm_cat.values):
    axes[1].text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=9)
plt.tight_layout()
save(fig, "08_profit_margin_analysis")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 9 — Quarterly Comparison
# ═══════════════════════════════════════════════════════════════════════════
print("[EDA 9] Quarterly Revenue Comparison")
qtr = df.groupby(["Year", "Quarter"])["Revenue"].sum().reset_index()
qtr["Label"] = qtr["Year"].astype(str) + " " + qtr["Quarter"]

fig, ax = plt.subplots(figsize=(11, 5))
colors = [PALETTE[0] if y == 2023 else PALETTE[1] for y in qtr["Year"]]
bars = ax.bar(qtr["Label"], qtr["Revenue"]/1e5, color=colors)
ax.set_title("Quarterly Revenue Comparison (2023 vs 2024)",
             fontsize=14, fontweight="bold")
ax.set_ylabel("Revenue (₹ Lakhs)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f"₹{bar.get_height():.0f}L", ha="center", va="bottom", fontsize=9)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=PALETTE[0], label="2023"),
                   Patch(color=PALETTE[1], label="2024")])
plt.tight_layout()
save(fig, "09_quarterly_comparison")

# ═══════════════════════════════════════════════════════════════════════════
# FIG 10 — Sales Rep Performance
# ═══════════════════════════════════════════════════════════════════════════
print("[EDA 10] Sales Rep Performance")
rep = df.groupby("Sales_Rep")[["Revenue", "Profit"]].sum().sort_values("Revenue", ascending=False).head(15)

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(rep))
w = 0.35
ax.bar(x - w/2, rep["Revenue"]/1e5, w, label="Revenue", color=PALETTE[0])
ax.bar(x + w/2, rep["Profit"]/1e5,  w, label="Profit",  color=PALETTE[1])
ax.set_xticks(x); ax.set_xticklabels(rep.index, rotation=45, ha="right")
ax.set_title("Top 15 Sales Reps by Revenue & Profit", fontsize=14, fontweight="bold")
ax.set_ylabel("Amount (₹ Lakhs)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
ax.legend()
plt.tight_layout()
save(fig, "10_sales_rep_performance")

print("\n✅ All 10 EDA charts saved to ../eda/")
