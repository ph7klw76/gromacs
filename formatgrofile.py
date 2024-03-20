# Define the path to the input file
file_path = 'D:/Peking/align.txt'

# Read the content of the input file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Define the Python format string corresponding to the C format string
format_str = "{:>4}{:<6}{:>5}{:>5}{:>8.3f}{:>8.3f}{:>8.3f}\n"

# Process each line according to the given format and collect the formatted lines
formatted_lines = []
for line in lines:
    parts = line.split()
    if len(parts) == 6:
        # Unpack the parts and convert numerical values to float
        res_name, atom_name, atom_num, x, y, z = parts
        atom_num = int(atom_num)
        x, y, z = float(x), float(y), float(z)
        # Format the line according to the specified format string
        formatted_line = format_str.format("",res_name, atom_name, atom_num, x, y, z)
        formatted_lines.append(formatted_line)

# Specify the path where the formatted file will be saved
formatted_file_path = 'D:/Peking/align-1.txt'

# Save the formatted lines to the new file
with open(formatted_file_path, 'w') as file:
    file.writelines(formatted_lines)

print(f"Formatted file saved as {formatted_file_path}")
