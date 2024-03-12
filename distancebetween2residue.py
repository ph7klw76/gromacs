# Let's start by reading the contents of the provided GROMACS file to understand its structure and extract the relevant information.

file_path = 'D:/shafiq/5/nvt4.gro'

# Define a function to parse the .gro file
def parse_gro_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Skip the header and the last line which contains the box vectors
    atom_lines = lines[2:-1]
    
    molecules = {}
    for line in atom_lines:
        residue_number = int(line[:5].strip())
        residue_name = line[5:10].strip()
        atom_name = line[10:15].strip()
        atom_number = int(line[15:20].strip())
        x = float(line[20:28].strip())
        y = float(line[28:36].strip())
        z = float(line[36:44].strip())
        
        if residue_name not in molecules:
            molecules[residue_name] = []
        molecules[residue_name].append({'residue_number': residue_number, 'atom_name': atom_name, 'atom_number': atom_number, 'coordinates': (x, y, z)})
    
    return molecules

# Parse the file
molecules = parse_gro_file(file_path)
molecules.keys()  # Display the molecule types

from scipy.spatial.distance import cdist
import numpy as np

# Extract coordinates for each molecule type and group them by residue number
def extract_coordinates_by_residue(molecules_dict, molecule_name):
    coordinates = {}
    for molecule in molecules_dict[molecule_name]:
        residue_number = molecule['residue_number']
        if residue_number not in coordinates:
            coordinates[residue_number] = []
        coordinates[residue_number].append(molecule['coordinates'])
    return coordinates

# Calculate the average position of each molecule (assuming molecules are not split across periodic boundaries)
def calculate_center_of_mass(coordinates_dict):
    center_of_masses = {}
    for residue, coords in coordinates_dict.items():
        center_of_masses[residue] = np.mean(coords, axis=0)
    return center_of_masses

# Calculate nearest neighbors
def find_nearest_neighbors(coms1, coms2):
    residues1 = list(coms1.keys())
    residues2 = list(coms2.keys())
    coords1 = np.array(list(coms1.values()))
    coords2 = np.array(list(coms2.values()))

    distances = cdist(coords1, coords2, 'euclidean')
    nearest_indices = distances.argmin(axis=1)
    nearest_distances = distances.min(axis=1)
    
    neighbors = []
    for i, index in enumerate(nearest_indices):
        neighbors.append((residues1[i], residues2[index], nearest_distances[i]))
    
    return neighbors

# Extract coordinates
coordinates_ZMYH = extract_coordinates_by_residue(molecules, 'ZMYH')
coordinates_HJMA = extract_coordinates_by_residue(molecules, 'HJMA')

# Calculate center of masses
com_ZMYH = calculate_center_of_mass(coordinates_ZMYH)
com_HJMA = calculate_center_of_mass(coordinates_HJMA)

# Find nearest neighbors for each molecule type
neighbors_ZMYH = find_nearest_neighbors(com_ZMYH, com_HJMA)
neighbors_HJMA = find_nearest_neighbors(com_HJMA, com_ZMYH)

# Combine both lists of nearest neighbors for saving to a text file
combined_neighbors = neighbors_ZMYH + neighbors_HJMA

# Define the file path for saving the results
output_file_path = 'D:/shafiq/5/nearest_neighbors_results.txt'

# Save the results to a text file
with open(output_file_path, 'w') as file:
    file.write("Residue ZMYH, Residue HJMA, Distance (nm)\n")  # Header
    for zmyh_residue, hjma_residue, distance in combined_neighbors:
        file.write(f"{zmyh_residue}, {hjma_residue}, {distance:.6f}\n")

# Provide the path for the user to download the file
output_file_path
