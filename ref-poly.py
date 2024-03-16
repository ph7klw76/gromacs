import pandas as pd

# # Load the Excel file
file_path = 'C:/Users/User/Downloads/dihedral.xlsx'  # Replace with your file path
df = pd.read_excel(file_path)
# # Initialize the 'ai1' column to ensure it's ready for data insertion

for index, row in df.iterrows():
    # Find rows where 'A1' matches 'ref' and update 'A2' with 'Long2' accordingly
    df.loc[df['ai'] == row['monomer'], 'ai1'] = row['Long']
for index, row in df.iterrows():
    df.loc[df['aj'] == row['monomer'], 'aj1'] = row['Long']
for index, row in df.iterrows():
    df.loc[df['ak'] == row['monomer'], 'ak1'] = row['Long']
for index, row in df.iterrows():
     df.loc[df['al'] == row['monomer'], 'al1'] = row['Long']
# # Save the modified DataFrame to a new Excel file
# # Replace 'modified_file_path.xlsx' with your desired output file path
# df.to_excel('C:/Users/User/Downloads/final_updated_bond-1.xlsx', index=False)


# Load the Excel file
# file_path = 'C:/Users/User/Downloads/final_updated_bond-4.xlsx'  # Replace with your file path
# df = pd.read_excel(file_path)
# Initialize the 'ai1' column to ensure it's ready for data insertion

# Identifying the first occurrence of each unique 'ref' value
first_occurrences_ref = df.drop_duplicates(subset='ref', keep='first').set_index('ref')['Long2'].to_dict()
df['ai2'] = df['ai1'].map(first_occurrences_ref)
df['aj2'] = df['aj1'].map(first_occurrences_ref)
df['ak2'] = df['ak1'].map(first_occurrences_ref)
df['al2'] = df['al1'].map(first_occurrences_ref)

df['ref_occurrence'] = df.groupby('ref').cumcount() + 1
second_occurrences_ref = df[df['ref_occurrence'] == 2].set_index('ref')['Long2'].to_dict()  # 2==second, 3==third
df['ai3'] = df['ai1'].map(second_occurrences_ref)
df['aj3'] = df['aj1'].map(second_occurrences_ref)
df['ak3'] = df['ak1'].map(second_occurrences_ref)
df['al3'] = df['al1'].map(second_occurrences_ref)

second_occurrences_ref = df[df['ref_occurrence'] == 3].set_index('ref')['Long2'].to_dict()  # 2==second, 3==third
df['ai4'] = df['ai1'].map(second_occurrences_ref)
df['aj4'] = df['aj1'].map(second_occurrences_ref)
df['ak4'] = df['ak1'].map(second_occurrences_ref)
df['al4'] = df['al1'].map(second_occurrences_ref)

second_occurrences_ref = df[df['ref_occurrence'] == 4].set_index('ref')['Long2'].to_dict()  # 2==second, 3==third
df['ai5'] = df['ai1'].map(second_occurrences_ref)
df['aj5'] = df['aj1'].map(second_occurrences_ref)
df['ak5'] = df['ak1'].map(second_occurrences_ref)
df['al5'] = df['al1'].map(second_occurrences_ref)

modified_file_path_improper2 = 'C:/Users/User/Downloads/dihedral-done.xlsx'
df.to_excel(modified_file_path_improper2, index=False)
