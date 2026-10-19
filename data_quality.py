
import pandas as pd

df = pd.read_csv("superstore_sales.csv", encoding="cp1252")

# Remove accidental spaces from column names for inspection
df.columns = df.columns.str.strip()

print("========== DATA QUALITY REPORT ==========")

# 1. Dataset dimensions
print("\n1. Dataset dimensions:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# 2. Missing values
print("\n2. Missing values:")
missing = df.isnull().sum()
missing_report = pd.DataFrame({
    "Missing_Count": missing,
    "Missing_Percentage": (
        missing / len(df) * 100 if len(df) > 0 else 0
    )
})
print(missing_report[missing_report["Missing_Count"] > 0])

# 3. Exact duplicate rows
print("\n3. Exact duplicate rows:")
print(df.duplicated().sum())

# 4. Duplicate column names
print("\n4. Duplicate column names:")
print(df.columns[df.columns.duplicated()].tolist())

# 5. Data types
print("\n5. Data types:")
print(df.dtypes)

# 6. Blank text values
print("\n6. Blank text values:")
text_columns = df.select_dtypes(include=["object", "string"]).columns

for col in text_columns:
    blank_count = (
        df[col].astype("string").str.strip().eq("").sum()
    )
    if blank_count > 0:
        print(f"{col}: {blank_count} blank values")

# 7. Check numeric fields for suspicious values
print("\n7. Numeric summary:")
print(df.select_dtypes(include="number").describe().T)

# 8. Inspect possible date columns
print("\n8. Date column checks:")
date_columns = [
    col for col in df.columns
    if "date" in col.lower()
]

for col in date_columns:
    parsed = pd.to_datetime(df[col], errors="coerce")
    invalid = df[col].notna() & parsed.isna()

    print(f"\n{col}")
    print("Invalid date values:", invalid.sum())
    print("Earliest valid date:", parsed.min())
    print("Latest valid date:", parsed.max())

# 9. Check negative values in important numeric fields
print("\n9. Negative values:")
for col in ["Sales", "Quantity", "Discount", "Profit"]:
    if col in df.columns:
        print(f"{col}: {(df[col] < 0).sum()}")

print("\n========== REPORT COMPLETE ==========")


from pathlib import Path

Path("reports").mkdir(exist_ok=True)

quality_report = pd.DataFrame({
    "Column": df.columns,
    "Data_Type": [str(dtype) for dtype in df.dtypes],
    "Missing_Count": df.isnull().sum().values,
    "Missing_Percentage": (
        df.isnull().mean().values * 100
    )
})

quality_report.to_csv(
    "reports/data_quality_report.csv",
    index=False
)

print("Quality report saved to reports/data_quality_report.csv")

