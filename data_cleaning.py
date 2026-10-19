
import pandas as pd
from pathlib import Path

# 1. Load the original dataset
df = pd.read_csv("superstore_sales.csv", encoding="cp1252")

print("Original dataset shape:", df.shape)

# 2. Clean column names
df.columns = df.columns.str.strip()

# 3. Remove leading/trailing spaces from text columns
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].apply(
        lambda value: value.strip() if isinstance(value, str) else value
    )

# 4. Convert empty strings into missing values
df = df.replace(r"^\s*$", pd.NA, regex=True)

# 5. Remove exact duplicate rows
duplicate_count = df.duplicated().sum()
df = df.drop_duplicates()

print("Exact duplicate rows removed:", duplicate_count)

# 6. Convert date columns where applicable
for col in df.columns:
    if "date" in col.lower():
        converted = pd.to_datetime(
            df[col],
            errors="coerce",
            format="mixed"
        )

        invalid_count = (df[col].notna() & converted.isna()).sum()

        print(f"{col} - invalid dates:", invalid_count)

        df[col] = converted

# 7. Convert common numeric columns where applicable
numeric_columns = [
    "Sales", "Quantity", "Discount", "Profit"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 8. Report missing values after conversion
print("\nMissing values after cleaning:")
print(df.isnull().sum())

# 9. Validate important numeric fields
for col in ["Sales", "Quantity", "Discount", "Profit"]:
    if col in df.columns:
        print(f"\n{col} summary:")
        print(df[col].describe())

# 10. Save cleaned data
output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "superstore_sales_cleaned.csv"
df.to_csv(output_file, index=False)

print("\nCleaned dataset saved to:", output_file)
print("Cleaned dataset shape:", df.shape)
