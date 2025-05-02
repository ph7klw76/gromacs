import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm    # ← new: progress bars

def read_gro_file_with_masses(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[2:]  # Skip the first two header lines

    molecules = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            molecule_number = int(line[0:5])
            atom_type = line[10:15].strip()
            x, y, z = map(float, [
                line[20:28].strip(),
                line[28:36].strip(),
                line[36:44].strip()
            ])
            molecules.setdefault(molecule_number, []).append((x, y, z, atom_type))
        except ValueError:
            continue
    return molecules

def extract_specific_carbon_atoms(atoms, carbon_labels):
    return [atom for atom in atoms
            if any(lbl in atom[3] for lbl in carbon_labels)]

def calculate_nearest_avg_specific_carbon_distances_and_neighbors(molecules, carbon_labels):
    carbon_coords = {
        mol_id: np.array([atom[:3]
                          for atom in extract_specific_carbon_atoms(atoms, carbon_labels)])
        for mol_id, atoms in molecules.items()
    }

    mol_ids = list(carbon_coords.keys())
    nearest = {}

    # Outer loop with tqdm
    for mol_i in tqdm(mol_ids, desc="Processing molecules"):
        coords_i = carbon_coords[mol_i]
        if coords_i.size == 0:
            continue

        best_j = None
        best_avg = None

        # Inner loop also wrapped (optional)
        for mol_j in mol_ids:
            if mol_j == mol_i:
                continue
            coords_j = carbon_coords[mol_j]
            if coords_j.size == 0:
                continue

            avg_dist = cdist(coords_i, coords_j).mean()
            if (best_avg is None) or (avg_dist < best_avg):
                best_avg = avg_dist
                best_j = mol_j

        if best_j is not None:
            nearest[mol_i] = (best_j, best_avg)

    return nearest

def plot_probability_density(values, title, xlabel):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(values, fill=True)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Probability Density')
    plt.show()

if __name__ == "__main__":
    file_path = 'C:/Users/User/Documents/HK/HK5-output_whole.gro'
    specific_carbon_labels = ['C41','C39','C36','C35','C45','C53','C48','C50']

    molecules = read_gro_file_with_masses(file_path)

    # This will now show a progress bar as it works through each molecule.
    nearest_map = calculate_nearest_avg_specific_carbon_distances_and_neighbors(
        molecules, specific_carbon_labels
    )

    avg_distances = [dist for (_, dist) in nearest_map.values()]

    plot_probability_density(
        avg_distances,
        'Probability Density of Nearest-Molecule Avg Specific-Carbon Distances',
        'Average Specific-Carbon Distance (nm)'
    )

    out_fname = 'nearest_molecule_distances.txt'
    with open(out_fname, 'w') as fout:
        fout.write("Mol_i\tMol_j_nearest\tAvgDist(nm)\n")
        for mol_i, (mol_j, avg_dist) in sorted(nearest_map.items()):
            fout.write(f"{mol_i}\t{mol_j}\t{avg_dist:.6f}\n")

    print(f"Done! Results saved to {out_fname}")
