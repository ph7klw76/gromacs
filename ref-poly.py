import pandas as pd

# Load the Excel file
file_path = 'D:/dihedral-1.xlsx'  # Replace with your file path
df = pd.read_excel(file_path)
# Initialize the 'ai1' column to ensure it's ready for data insertion

# Identifying the first occurrence of each unique 'ref' value
first_occurrences_ref = df.drop_duplicates(subset='ref', keep='first').set_index('ref')['Long'].to_dict()

# Updating 'ai2', 'aj2', 'ak2', 'al2' based on the first occurrence matches
df['ai2'] = df['ai'].map(first_occurrences_ref)
df['aj2'] = df['aj'].map(first_occurrences_ref)
df['ak2'] = df['ak'].map(first_occurrences_ref)
df['al2'] = df['al'].map(first_occurrences_ref)

modified_file_path_improper2 = 'D:/dihedral-2.xlsx'
df.to_excel(modified_file_path_improper2, index=False)
