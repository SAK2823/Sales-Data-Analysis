
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load cleaned data
df = pd.read_csv("data/superstore_sales_cleaned.csv")

# Convert dates
for col in df.columns:
    if "date" in col.lower():
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Create output folder
Path("reports").mkdir(exist_ok=True)

# 1. Overall business performance
print("\n===== OVERALL PERFORMANCE =====")

for col in ["Sales", "Profit", "Quantity"]:
    if col in df.columns:
        print(f"Total {col}: {df[col].sum():,.2f}")

if "Sales" in df.columns and "Profit" in df.columns:
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()

    margin = (
        total_profit / total_sales * 100
        if total_sales != 0 else 0
    )

    print(f"Overall profit margin: {margin:.2f}%")

# 2. Category performance
if {"Category", "Sales", "Profit"}.issubset(df.columns):
    category = df.groupby("Category").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    ).sort_values("Total_Sales", ascending=False)

    print("\n===== CATEGORY PERFORMANCE =====")
    print(category.round(2))

    category.to_csv("reports/category_performance.csv")

    category["Total_Sales"].plot(
        kind="bar", title="Sales by Category",
        ylabel="Sales", xlabel="Category"
    )
    plt.tight_layout()
    plt.savefig("reports/sales_by_category.png")
    plt.close()

# 3. Regional performance
if {"Region", "Sales", "Profit"}.issubset(df.columns):
    region = df.groupby("Region").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    ).sort_values("Total_Sales", ascending=False)

    print("\n===== REGIONAL PERFORMANCE =====")
    print(region.round(2))

    region.to_csv("reports/regional_performance.csv")

# 4. Monthly sales trends
date_col = next(
    (col for col in df.columns if col.lower() == "order date"),
    None
)

if date_col and "Sales" in df.columns:
    monthly = (
        df.dropna(subset=[date_col])
        .set_index(date_col)["Sales"]
        .resample("MS")
        .sum()
    )

    print("\n===== MONTHLY SALES =====")
    print(monthly.to_string())

    monthly.to_csv("reports/monthly_sales.csv")

    monthly.plot(
        kind="line", title="Monthly Sales Trend",
        ylabel="Sales", xlabel="Month"
    )
    plt.tight_layout()
    plt.savefig("reports/monthly_sales_trend.png")
    plt.close()

# 5. Top subcategories
if {"Sub-Category", "Sales", "Profit"}.issubset(df.columns):
    subcategory = df.groupby("Sub-Category").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    ).sort_values("Total_Sales", ascending=False)

    print("\n===== TOP 10 SUBCATEGORIES BY SALES =====")
    print(subcategory.head(10).round(2))

    subcategory.to_csv("reports/subcategory_performance.csv")

print("\nEDA complete. Check the reports folder.")
