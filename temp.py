# Since we don't have access to the actual files, this code will outline the approach without executing it.
import pandas as pd

# Step 1: Load both CSV files
df_stripped_cleaned = pd.read_csv('full_Table_STRIPPED_CLEANED.csv')
df_high_qual = pd.read_csv('full_Table_HIGH_QUAL.csv')

# Step 2: Get the columns from both DataFrames
stripped_cleaned_columns = set(df_stripped_cleaned.columns)
high_qual_columns = set(df_high_qual.columns)

# Step 3: Find the differences
columns_in_high_qual_not_in_stripped_cleaned = high_qual_columns - stripped_cleaned_columns
columns_in_stripped_cleaned_not_in_high_qual = stripped_cleaned_columns - high_qual_columns

# Step 4: Display the results
print("Columns in HIGH_QUAL but not in STRIPPED_CLEANED:", columns_in_high_qual_not_in_stripped_cleaned)
print("Columns in STRIPPED_CLEANED but not in HIGH_QUAL:", columns_in_stripped_cleaned_not_in_high_qual)

# This code won't run here due to the lack of access to the CSV files, but it can be used in an environment where the files are accessible.
