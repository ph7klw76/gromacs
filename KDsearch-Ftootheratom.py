import numpy as np
from scipy.spatial import KDTree
def parse_gro_file_all_atoms(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Data structure to hold all atom information
    atoms = []

    for line in lines[2:-1]:
        residue_number = int(line[:5].strip())
        residue_name = line[0:10].strip()
        atom_name = line[10:15].strip()
        atom_number = int(line[15:20].strip())
        x = float(line[20:28].strip())
        y = float(line[28:36].strip())
        z = float(line[36:44].strip())
        
        atoms.append(((residue_number, residue_name, atom_name, atom_number), np.array([x, y, z])))

    return atoms
file_path='D:/shafiq/7/nvt4.gro'
# Parse the file to get all atom data
all_atom_data = parse_gro_file_all_atoms(file_path)

# KDTree for all atoms
all_coordinates = np.array([data[1] for data in all_atom_data])
all_kd_tree = KDTree(all_coordinates)

# Now find the shortest distances from 'F' atoms to any other atom in different molecules
def find_shortest_distances_all_atoms(f_atom_data, all_atom_data, all_kd_tree):
    shortest_distances_all = []

    for i, ((residue_number_i, residue_name_i, atom_name_i, atom_number_i), coord_i) in enumerate(f_atom_data):
        if 'F' not in atom_name_i:  # Skip atoms that don't contain 'F'
            continue

        # Query the KDTree for the nearest neighbor, excluding the atom itself
        distance, index = all_kd_tree.query(coord_i, k=2)  # k=2 because the closest (first one) is the atom itself
        # Ensure the nearest is from a different molecule by checking residue number
        if all_atom_data[index[1]][0][0] != residue_number_i:
            nearest_atom = all_atom_data[index[1]][0]
            shortest_distances_all.append({
                'from_atom': atom_name_i,
                'from_residue': residue_name_i,
                'to_atom': nearest_atom[2],
                'to_residue': nearest_atom[1],
                'distance': distance[1]  # distance[0] is the distance to itself, which is 0
            })

    return shortest_distances_all

# Find the shortest distances for each 'F' atom to any other atom in a different molecule
shortest_distances_all_atoms = find_shortest_distances_all_atoms(all_atom_data, all_atom_data, all_kd_tree)

# Save the output to a text file
output_file_path_all_atoms = 'D:/shafiq/7/shortest_distances_F_to_all_atoms.txt'

with open(output_file_path_all_atoms, 'w') as file:
    for distance_info in shortest_distances_all_atoms:
        file.write(f"From Atom: {distance_info['from_atom']} ({distance_info['from_residue']}), "
                   f"To Atom: {distance_info['to_atom']} ({distance_info['to_residue']}), "
                   f"Distance: {distance_info['distance']:.3f}\n")

output_file_path_all_atoms
