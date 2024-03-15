import pandas as pd

# Load the Excel file
file_path = 'D:/dihedral-3.xlsx'  # Replace with your file path
df = pd.read_excel(file_path)
# Initialize the 'ai1' column to ensure it's ready for data insertion

# Identifying the first occurrence of each unique 'ref' value
#first_occurrences_ref = df.drop_duplicates(subset='ref', keep='first').set_index('ref')['Long'].to_dict()

df['ref_occurrence'] = df.groupby('ref').cumcount() + 1
second_occurrences_ref = df[df['ref_occurrence'] == 3].set_index('ref')['Long'].to_dict()  # 2==second, 3==third
# Updating 'ai2', 'aj2', 'ak2', 'al2' based on the first occurrence matches
#df['ai2'] = df['ai'].map(first_occurrences_ref)
#df['aj2'] = df['aj'].map(first_occurrences_ref)
#df['ak2'] = df['ak'].map(first_occurrences_ref)
#df['al2'] = df['al'].map(first_occurrences_ref)

df['ai4'] = df['ai'].map(second_occurrences_ref)
df['aj4'] = df['aj'].map(second_occurrences_ref)
df['ak4'] = df['ak'].map(second_occurrences_ref)
df['al4'] = df['al'].map(second_occurrences_ref)

modified_file_path_improper2 = 'D:/dihedral-4.xlsx'
df.to_excel(modified_file_path_improper2, index=False)
