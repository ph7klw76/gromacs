import pandas as pd

# Load the Excel file
file_path = 'D:/dihedral-1.xlsx'  # Replace with your file path
df = pd.read_excel(file_path)
# Initialize the 'ai1' column to ensure it's ready for data insertion

for index, row in df.iterrows():
    # Find rows where 'A1' matches 'ref' and update 'A2' with 'Long2' accordingly
    df.loc[df['ai'] == row['monomer'], 'ai1'] = row['Long']
for index, row in df.iterrows():
    df.loc[df['aj'] == row['monomer'], 'aj1'] = row['Long']
for index, row in df.iterrows():
    df.loc[df['ak'] == row['monomer'], 'ak1'] = row['Long']
for index, row in df.iterrows():
    df.loc[df['al'] == row['monomer'], 'al1'] = row['Long']
# Save the modified DataFrame to a new Excel file
# Replace 'modified_file_path.xlsx' with your desired output file path
df.to_excel('D:/dihedral-2.xlsx', index=False)
