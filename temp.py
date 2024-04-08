import pandas as pd

# Load the CSV files
file_name_stripped_cleaned = 'full_Table_STRIPPED_CLEANED.csv'
file_name_high_qual = 'full_Table_HIGH_QUAL.csv'

df_stripped_cleaned = pd.read_csv(file_name_stripped_cleaned)
df_high_qual = pd.read_csv(file_name_high_qual)

# Filter out columns with '1hot' in the name
columns_stripped_cleaned = set(df_stripped_cleaned.columns) - set(df_stripped_cleaned.filter(regex='1hot').columns)
columns_high_qual = set(df_high_qual.columns) - set(df_high_qual.filter(regex='1hot').columns)

# Determine the differences in columns
columns_only_in_stripped_cleaned = columns_stripped_cleaned - columns_high_qual
columns_only_in_high_qual = columns_high_qual - columns_stripped_cleaned

print(columns_only_in_stripped_cleaned, columns_only_in_high_qual)
