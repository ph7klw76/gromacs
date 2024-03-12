import numpy as np
from scipy.spatial import KDTree

def parse_gro_file(file_path):
    atoms, molecules_with_f = [], {}
    molecule_info = {}  # Tracks whether each molecule contains 'F'

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines[2:-1]:
        residue_number = int(line[:5].strip())
        residue_name = line[0:10].strip()
        atom_name = line[10:15].strip()
        x, y, z = map(float, line[20:44].strip().split())

        atoms.append((residue_number, residue_name, atom_name, np.array([x, y, z])))
        if 'F' in atom_name:
            molecules_with_f[residue_number] = True
        molecule_info[residue_number] = molecule_info.get(residue_number, False) or 'F' in atom_name

    # Separate atoms based on whether they're in molecules containing 'F'
    target_atoms = [atom for atom in atoms if molecule_info[atom[0]]]
    return target_atoms, molecules_with_f

def find_shortest_distances(target_atoms, molecules_with_f):
    # Build KDTree for target atoms
    kd_tree = KDTree([atom[3] for atom in target_atoms if atom[2].startswith('F') and atom[0] in molecules_with_f])

    results = []
    for atom in target_atoms:
        residue_number, residue_name, atom_name, coordinates = atom
        if atom_name.startswith('F') and residue_number in molecules_with_f:
            # Perform the query with k=2 to find the nearest non-self neighbor
            distances, index = kd_tree.query(coordinates, k=2)
            # Ensure we're accessing the second closest distance since the first is the point itself
            # Convert the second closest distance to float for safety
            if len(distances) > 1 and len(index) > 1:  # Check if we have a second distance
                distance = float(distances[1])  # The actual nearest neighbor distance
                nearest_atom = target_atoms[index[1]]  # Adjust index access as needed
                # Ensure the nearest atom is from a different molecule
                if nearest_atom[0] != residue_number:
                    results.append({
                        'from_atom': atom_name,
                        'from_residue': residue_name,
                        'to_atom': nearest_atom[2],
                        'to_residue': nearest_atom[1],
                        'distance': distance
                    })

    return results
