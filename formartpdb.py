# Define the path to the input file
file_path = '/mnt/data/align.txt'

# Path to the output file
output_file_path = '/mnt/data/align_formatted.txt'

# Process and format each line of the input file
with open(file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
    for line in infile:
        record_type = line[0:6].strip()
        atom_serial_number = int(line[6:11].strip())
        atom_name = line[12:16].strip()
        alt_loc = line[16:17].strip()
        residue_name = line[17:20].strip()
        chain_id = line[21:22].strip()
        residue_seq_num = int(line[22:26].strip())
        insert_code = line[26:27].strip()
        x = float(line[30:38].strip())
        y = float(line[38:46].strip())
        z = float(line[46:54].strip())
        occupancy = float(line[54:60].strip())
        temp_factor = float(line[60:66].strip())
        element_symbol = line[76:78].strip()
        
        # Format the line according to the specified format string
        formatted_line = "{:6s}{:5d} {:^4s}{:1s}{:3s} {:1s}{:4d}{:1s} {:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f} {:>2s}{:2s}\n".format(
            record_type, atom_serial_number, atom_name, alt_loc, residue_name,
            chain_id, residue_seq_num, insert_code, x, y, z, occupancy, temp_factor,
            element_symbol, "")
        outfile.write(formatted_line)

print(f"Formatted file saved to: {output_file_path}")
