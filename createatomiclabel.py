""" for this code to work, dfirst row empty, then put the atomic label and then second colum atom type"""
import pandas as pd

# Load the Excel file
file_path = 'C:/Users/User/Downloads/Book3.xlsx'
df = pd.read_excel(file_path)

# Extract the first letter from the second column
df['FirstLetter'] = df.iloc[:, 1].astype(str).str[0]

# Calculate the cumulative count of each letter up to each row
df['Count'] = df.groupby('FirstLetter').cumcount() + 1

# Combine the letter and its count
df['Combined'] = df['FirstLetter'] + df['Count'].astype(str)

# Update the first column with the combined value where it's missing
df.iloc[:, 0] = df.iloc[:, 0].combine_first(df['Combined'])

# Save the updated DataFrame back to Excel
output_path = 'C:/Users/User/Downloads/Updated_Book3_Combined.xlsx'
df.to_excel(output_path, index=False)
