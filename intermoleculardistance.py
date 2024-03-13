from scipy.spatial import distance_matrix
import numpy as np
import pandas as pd

def extract_geometric_center(file_path, residue_name, molecule_numbers):
    molecule_atoms = {number: [] for number in molecule_numbers}  # Prepare a dict to hold atom coordinates
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[2:-1]:  # Skip the header and footer
            res_num = int(line[:5].strip())  # Residue number
            res_name = line[5:10].strip()  # Residue name
            
            if res_name == residue_name and res_num in molecule_numbers:
                x = float(line[20:28].strip())
                y = float(line[28:36].strip())
                z = float(line[36:44].strip())
                molecule_atoms[res_num].append((x, y, z))
    
    # Calculate geometric centers
    geometric_centers = {}
    for num, atoms in molecule_atoms.items():
        if atoms:  # Ensure there are atoms to avoid division by zero
            x_avg = sum(atom[0] for atom in atoms) / len(atoms)
            y_avg = sum(atom[1] for atom in atoms) / len(atoms)
            z_avg = sum(atom[2] for atom in atoms) / len(atoms)
            geometric_centers[num] = (x_avg, y_avg, z_avg)
    
    return geometric_centers

gro_file_path="E:/7/3/nvt4.gro"
# Extract geometric centers for all JJP5 molecules
jjp5_geometric_centers = extract_geometric_center(gro_file_path, "NUIE", range(1, 1000))  # Assuming a broad range

# Convert the geometric centers to a DataFrame for easier manipulation
df_centers = pd.DataFrame.from_dict(jjp5_geometric_centers, orient='index', columns=['x', 'y', 'z'])

# Calculate the distance matrix
dist_matrix = distance_matrix(df_centers.values, df_centers.values)

# Set the diagonal to np.inf to exclude self-distances
np.fill_diagonal(dist_matrix, np.inf)

# Find the minimum distance (nearest neighbor) for each molecule
min_distances = np.min(dist_matrix, axis=1)

# Plotting and statistics
import matplotlib.pyplot as plt
import seaborn as sns

mean_distance = np.mean(min_distances)
std_distance = np.std(min_distances)

# Plot the probability density of the nearest neighbor distances
sns.histplot(min_distances, stat="density", kde=True)
plt.xlabel('Distance (nm)')
plt.ylabel('Density')
plt.title('Probability Density of Nearest Neighbor Distances for NUIE Molecules')
plt.axvline(mean_distance, color='r', linestyle='--', label=f'Mean: {mean_distance:.3f} nm')
plt.legend()

print(mean_distance, std_distance)
