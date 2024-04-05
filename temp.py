import pandas as pd

# Load the data
import re

def process_csv(file_path, file_path_new):
    output_lines = []
    with open(file_path, 'r') as file:
        current_line = ''
        inside_quotes = False

        for line in file:
            # Count the number of quotes in this line
            num_quotes = line.count('"')

            # Toggle the inside_quotes flag if there's an odd number of quotes
            if num_quotes % 2 != 0:
                inside_quotes = not inside_quotes

            # If we're inside quotes, replace newlines with tabs
            if inside_quotes:
                current_line += line.replace('\n', '\t')
            else:
                # Append the current line to output_lines
                current_line += line
                output_lines.append(current_line)
                current_line = ''  # Reset for the next record

    # Write to the same file or a new file
    with open(file_path_new, 'w') as file:
        file.writelines(output_lines)

# Replace 'your_file.csv' with the path to your CSV file
process_csv('All_Groups.csv', 'All_Groups.csv')

data = pd.read_csv('All_Groups.csv')

data['cell_group'] = data['cc_pixel_intensity_ratio']
data['image_name'] = data['folder_name_x'] + '_' + data['cc_x'].astype(str)
data['file_name'] = data['image_name'] + '.tif'


# Create the new column based on the condition
data['cell_group'] = data['cell_group'].apply(lambda x: 1 if x > 0.1 else 0)

# Write the modified data back to the same file
data.to_csv('All_Groups.csv', index=False)
