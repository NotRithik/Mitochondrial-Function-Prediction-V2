import pandas as pd
import io 
# Load the data
import re
import ast
import numpy as np

csv_file_path = 'All_Groups.csv'
buffer = io.StringIO()

# Open and process the CSV file, to strip entries so that numbers aren't read as strings by read_csv and column names have no leading/trailing whitespaces
with open(csv_file_path, 'r') as file:
    for line in file:
        cleaned_line = ','.join(cell.strip() for cell in line.split(','))
        buffer.write(cleaned_line + '\n')

# Move the buffer cursor to the start
buffer.seek(0)

# Read the cleaned data into pandas
data = pd.read_csv(buffer)
edge_columns = [col for col in data.columns if col.startswith('edge_') and col.split('_')[-1].isdigit()]
# Replace empty entries with 0 in these columns
data[edge_columns] = data[edge_columns].fillna(0)

# Not sure if these folder names are required for segregating the dataset, so for now dropping them
# data = data.drop(columns=['folder_name_x', 'folder_name_x.1', 'folder_name_y'])
data = data.drop(columns=['folder_name_x.1']) # 'folder_name_x' not dropping here, dropping in sample_data

# Make each string in folder_name_y correspond to an integer instead
unique_strings = data['folder_name_y'].unique()
string_to_int_mapping = {string: i+1 for i, string in enumerate(unique_strings)}

data['folder_name_y'] = data['folder_name_y'].replace(string_to_int_mapping)

# For now, we aren't using the 555 channel either
data = data.drop(columns=['element_pixel_intensity_555'])

# These fields seem to be not implemented either:
data = data.drop(columns=["Unnamed: 0_x", "x", "y" ,"z" ,"node_x" ,"degree_x" ,"vol_cc_x" ,"avg_PK_Of_element_x" ,"element_connectivity_x" ,"Unnamed: 0_y"])

# The next few lines of code are to convert the degree_distribution column to columns labelled node_degree_0, node_degree_1, etc. till node_degree_MAX
def str_to_dict(s):
    try:
        return ast.literal_eval(s)
    except ValueError:
        return {}
# Apply the function to the 'degree_distribution' column
data['degree_distribution'] = data['degree_distribution'].apply(str_to_dict)

# Find the highest node degree in the DataFrame
max_degree = max(degree for row in data['degree_distribution'] for degree in row.keys())

# Create a DataFrame for new columns
new_columns = pd.DataFrame({f'node_degree_{i}': 0 for i in range(1, max_degree + 1)}, index=data.index)

# Concatenate with the original DataFrame
data = pd.concat([data, new_columns], axis=1)

# Function to update the degree columns for a row
def update_degrees(row):
    for degree, count in row['degree_distribution'].items():
        row[f'node_degree_{degree}'] = count
    return row

# Apply the function to each row
data = data.apply(update_degrees, axis=1)
data = data.drop(columns=['degree_distribution'])
# Now we should have columns labelled node_degree_0, node_degree_1, etc. till node_degree_MAX and dropped the degree_distribution column

data['cc_average_connectivity'] = data['cc_average_connectivity'].replace([np.inf, -np.inf], 0)

data['cc_pixel_intensity_488'] = data['cc_pixel_intensity_488'].replace(0, np.nan)
data = data.dropna(subset=['cc_pixel_intensity_488'])

data['cc_pixel_intensity_405_488_ratio'] = ((np.array(data['cc_pixel_intensity_405']) / np.array(data['cc_pixel_intensity_488']))*1000).copy()
# data['cc_pixel_intensity_ratio'] = (np.array(data['cc_pixel_intensity_ratio']) * 1000).copy()
# Add feature vectors from CNN obtained image vectors

# data.drop('image_name', axis=1, inplace=True)
data['image_name'] = data['folder_name_x'] + '_' + data['cc_x'].astype(str)
data['file_name'] = data['image_name'] + '.tif'



data = pd.read_csv('All_Groups.csv')

data['cell_group'] = data['cc_pixel_intensity_ratio']
data['image_name'] = data['folder_name_x'] + '_' + data['cc_x'].astype(str)
data['file_name'] = data['image_name'] + '.tif'


# Create the new column based on the condition
data['cell_group'] = data['cell_group'].apply(lambda x: 1 if x > 0.1 else 0)

# Write the modified data back to the same file
data.to_csv('All_Groups.csv', index=False)
