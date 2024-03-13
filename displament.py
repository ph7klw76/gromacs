# Corrected Python code to adjust specified columns in a PDB file

def process_line_corrected(line, subtract_values):
    if line.startswith("HETATM"):
        parts = line.split()
        parts[4] = f"{float(parts[4]) - subtract_values[0]:.3f}"  # Adjusting the 4th column
        parts[5] = f"{float(parts[5]) - subtract_values[1]:.3f}"  # Adjusting the 5th column
        parts[6] = f"{float(parts[6]) - subtract_values[2]:.3f}"  # Adjusting the 6th column
        print(parts[4])
        # Reconstruct the line with updated values, maintaining the original format
        new_line = f"{parts[0]:<6}{parts[1]:>5} {parts[2]:>2} {parts[3]:>11} {parts[4]:>11} {parts[5]:>7}  {parts[6]:<5}   {parts[7]:>21}"
    else:
        new_line = line.rstrip()  # No modification for lines not starting with "HETATM"
    return new_line

# Replace 'pdb_file_path' and 'output_file_path' with the actual paths
pdb_file_path = 'E:/Pz10chain2.pdb'
output_file_path = 'E:/Pz10chain2_modified_v2.pdb'

subtract_values_corrected = (14.419, 0.36, 2.886)

with open(pdb_file_path, 'r') as file, open(output_file_path, 'w') as outfile:
    for line in file:
        modified_line = process_line_corrected(line, subtract_values_corrected)
        outfile.write(modified_line + '\n')

print(f"Modified file saved to: {output_file_path}")
