import pandas as pd

# Load the data
data = pd.read_csv('full_Table_HIGH_QUAL.csv')

# Create the new column based on the condition
data['cell_group'] = data['cell_group'].apply(lambda x: 1 if x > 0 else 0)

# Write the modified data back to the same file
data.to_csv('full_Table_HIGH_QUAL.csv', index=False)
