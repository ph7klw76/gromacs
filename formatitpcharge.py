# Path to the original and target format files
original_file_path = 'path/to/charge2.txt'
target_format_file_path = 'path/to/charge1.txt'
new_file_path = 'path/to/charge2_reformatted.txt'

# Function to read the content of a file
def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# Function to reformat lines based on the target format
def reformat_lines(original_lines):
    reformatted_lines = []
    for line in original_lines:
        parts = line.split()
        formatted_line = f"{parts[0]:>5} {parts[1]:>5} {parts[2]:>4} {parts[3]:>6} {parts[4]:>5} {parts[5]:>5} {float(parts[6]):>7.3f} {float(parts[7]):>7.4f}\n"
        reformatted_lines.append(formatted_line)
    return reformatted_lines

# Function to write reformatted lines to a new file
def write_reformatted_lines(reformatted_lines, new_file_path):
    with open(new_file_path, 'w') as file:
        file.writelines(reformatted_lines)

# Main process
def reformat_file(original_file_path, new_file_path):
    original_lines = read_file_content(original_file_path)
    reformatted_lines = reformat_lines(original_lines)
    write_reformatted_lines(reformatted_lines, new_file_path)

# Run the reformatting process
reformat_file(original_file_path, new_file_path)

print(f"The content of {original_file_path} has been reformatted and saved to {new_file_path}.")
