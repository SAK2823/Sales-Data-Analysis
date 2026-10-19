
import pandas as pd

# Load the dataset
df = pd.read_csv("superstore_sales.csv", encoding="cp1252")

# 1. Display the first five rows
print("\n--- FIRST 5 ROWS ---")
print(df.head())

# 2. Display the last five rows
print("\n--- LAST 5 ROWS ---")
print(df.tail())

# 3. Check the number of rows and columns
print("\n--- DATASET SHAPE ---")
print(df.shape)

# 4. Display column names
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

# 5. Check data types and non-null values
print("\n--- DATASET INFORMATION ---")
df.info()

# 6. Generate summary statistics
print("\n--- SUMMARY STATISTICS ---")
print(df.describe(include="all").T)

# 7. Count missing values in each column
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# 8. Count duplicate rows
print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())
