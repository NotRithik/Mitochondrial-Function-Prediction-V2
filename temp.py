import pandas as pd
import re

# Load the CSV file into a DataFrame
df = pd.read_csv('full_Table_STRIPPED_CLEANED.csv')

# Function to clean the file_name
def clean_file_name(file_name):
    # Remove "_Subset_x.tif" where x is any integer
    cleaned_name = re.sub(r'_Subset_\d+\.tif$', '', file_name)
    # Remove "_S_x.tif" where x is any integer
    cleaned_name = re.sub(r'_S_\d+\.tif$', '', cleaned_name)
    return cleaned_name

# Apply the cleaning function to the file_name column
df['cleaned_file_name'] = df['file_name'].apply(clean_file_name)

# Get unique cleaned file names and sort them alphabetically
unique_names = sorted(df['cleaned_file_name'].unique())

# Create a mapping from unique names to folder IDs starting from 1
folder_id_mapping = {name: i+1 for i, name in enumerate(unique_names)}

# Map the cleaned file names to folder IDs
df['folder_id'] = df['cleaned_file_name'].map(folder_id_mapping)

# Drop the temporary cleaned_file_name column
df.drop(columns=['cleaned_file_name'], inplace=True)

# Save the updated DataFrame to a new CSV file
df.to_csv('full_Table_STRIPPED_CLEANED_with_folder_id.csv', index=False)

# Print the unique names and their corresponding folder IDs (for reference)
for name, folder_id in folder_id_mapping.items():
    print(f"{name}: {folder_id}")

# Print the total number of unique names
print(f"Total number of unique names: {len(unique_names)}")
