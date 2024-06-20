import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# Function to calculate centroid (average) of a set of points
def calculate_centroid(points):
    return np.mean(points, axis=0)

# Function to calculate normal vector of a plane defined by three points
def calculate_normal_vector(points):
    vector1 = points[1] - points[0]
    vector2 = points[2] - points[0]
    return np.cross(vector1, vector2)

# Function to calculate angle between two vectors
def calculate_angle(vector1, vector2):
    cos_theta = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    return np.arccos(cos_theta) * (180.0 / np.pi)  # Convert to degrees

# Function to extract points based on atom ids
def get_points(data, ids):
    return data[np.isin(data[:, 2], ids), 3:].astype(float)

def calculate_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return np.linalg.norm(point1 - point2)

def find_shortest_distances(molecule_centroids, molecule_centroids2):
    """Find the shortest distance for each molecule in molecule_centroids2 to any molecule in molecule_centroids."""
    shortest_distances = {}  # Dictionary to hold shortest distances for each molecule in molecule_centroids2

    # Iterate over each molecule in molecule_centroids2
    for molecule2, centroids2 in molecule_centroids2.items():
        min_distance = float('inf')  # Initialize with a large number
        closest_molecule = None
        closest_centroid_pair = None
        
        # Check distance to every centroid in molecule_centroids
        for molecule1, centroids1 in molecule_centroids.items():
            for centroid1 in centroids1:
                for centroid2 in centroids2:
                    distance = calculate_distance(centroid1, centroid2)
                    if distance < min_distance:
                        min_distance = distance
                        closest_molecule = molecule1
                        closest_centroid_pair = (centroid1, centroid2)

        # Store the results for this molecule from molecule_centroids2
        shortest_distances[molecule2] = (min_distance, closest_molecule, closest_centroid_pair)
    return shortest_distances

# Function to get normal vectors for given ids_list and data
def get_normal_vectors(data, ids_list):
    normal_vectors = []
    for ids in ids_list:
        points = get_points(data, ids)
        normal_vector = calculate_normal_vector(points)
        normal_vectors.append(normal_vector)
    return normal_vectors


# Number of atoms in each monomer unit
a = 2142

# Define the atom ids for centroid calculations
ids_list = [
    [14, 15], [52, 53], [74, 88], [122, 123], [157, 158], [194, 195],
    [216, 230], [217, 272], [300, 299], [333, 319], [376, 377], [402, 403],
    [437, 438], [468, 469], [505, 506], [540, 541], [574, 573], [613, 599],
    [644, 643], [680, 681]
]


# New ids_list_planes for defining planes for the poymer
ids_list_planes = [
    [1, 8, 24], [40, 46, 59], [80, 77, 94], [110, 116, 129],
    [145, 151, 164], [198, 201, 183], [233, 236, 220], [250, 256, 264],
    [303, 306, 288], [325, 322, 339], [355, 361, 369], [390, 396, 409],
    [425, 431, 444], [460, 466, 475], [509, 515, 498], [544, 550, 533],
    [565, 571, 580], [605, 602, 619], [635, 641, 650], [684, 690, 673]
] #monomer unit center

# Number of atoms in dopant
a2 = 41
m=77112
# Define the atom ids for centroid calculations
ids_list2 = [[20+m,22+m,37+m,27+m,36+m,28+m,30+m,32+m,34+m]]  # DOPANT


base_path = 'C:/Users/Woon/Documents/DICC/suhao/straight/'
num_files = 2  # Number of file pairs


# Initialize lists to store all distances and angles
all_distances = []
all_angles = []
data_DistancevsAngle=[]
# Loop through each file pair
for i in range(1, num_files + 1):
    file1 = f'{base_path}frame_{i}.gro'
    output_file_path = f'{base_path}frame_{i}-modified.gro'
    # Read the data from the file
    input_file_path = file1
    # Read the entire file into a list of lines
    with open(input_file_path, 'r') as file:
        lines = file.readlines()  
    lines = lines[2:-1]
    
    with open(output_file_path, 'w') as outfile:
        for line in lines:
                # Extract and modify data from each line
                col1 = line[:4].strip()
                col2 = col1 + line[4:10].strip()
                col3 = line[10:15].strip()
                col4 = line[15:20].strip()
                col5 = float(line[20:28].strip())
                col6 = float(line[28:36].strip())
                col7 = float(line[36:44].strip())
                # Prepare the string to write to the output file
                output_line = f"{col2}\t{col3}\t{col4}\t{col5:.3f}\t{col6:.3f}\t{col7:.3f}\n"
                outfile.write(output_line)

    filename = output_file_path   #polymer

    data = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 6:
                molecule_name = parts[0]
                residue = parts[1]
                atom_id = int(parts[2])
                x, y, z = map(float, parts[3:6])
                data.append([molecule_name, residue, atom_id, x, y, z])
    
    data = np.array(data, dtype=object)
    # Initialize dictionary to store centroids for each molecule name
    molecule_centroids = {}
    
    # Calculate centroids for each monomer unit in the polymer
    for n in range(36):
        start_id = n * a
        
        for ids in ids_list:
            ids = [id_ + start_id for id_ in ids]
            points = get_points(data, ids)
            centroid = calculate_centroid(points)
            
            # Get molecule name for current monomer unit
            molecule_name = data[np.isin(data[:, 2], ids)][0, 0]
            
            if molecule_name not in molecule_centroids:
                molecule_centroids[molecule_name] = []
            molecule_centroids[molecule_name].append(centroid)
    
    # Initialize dictionary to store centroids for each molecule name
    molecule_centroids2 = {}
    
    # Calculate centroids for each monomer unit in the polymer
    for n in range(180):  #there are 180 dopant molecules
        start_id = n * a2
    
        for ids in ids_list2:
            ids = [id_ + start_id for id_ in ids]
            points = get_points(data, ids)
            centroid = calculate_centroid(points)
            
            # Get molecule name for current monomer unit
            molecule_name = data[np.isin(data[:, 2], ids)][0, 0]
            
            if molecule_name not in molecule_centroids:
                molecule_centroids2[molecule_name] = []
            molecule_centroids2[molecule_name].append(centroid)
    
    #Avoid edge effect
    filtered_molecule_centroids2 = {}
    for molecule_name, centroids in molecule_centroids2.items():
        filtered_centroids = [centroid for centroid in centroids if (0.5 <= centroid[0] <= 16.43 and 0.5 <= centroid[1] <= 9.32 and 0.5 <= centroid[2] <= 4.25)]
        if filtered_centroids:
            filtered_molecule_centroids2[molecule_name] = filtered_centroids
            
    shortest_distances = find_shortest_distances(molecule_centroids, filtered_molecule_centroids2)
    
    distances = [details[0] for details in shortest_distances.values()]
    
    
    # Get normal vectors for ids_list_planes and ids_list2
    normal_vectors_planes = get_normal_vectors(data, ids_list_planes)
    normal_vectors_ids2 = get_normal_vectors(data, ids_list2)
    
    # Calculate the angle between normal vectors for each pair of shortest distances
    shortest_distances_with_angles = []
    
    for molecule2, details in shortest_distances.items():
        # details[2] contains the closest centroid pair (centroid1, centroid2)
        closest_centroid1 = details[2][0]
        closest_centroid2 = details[2][1]
        
        # Find the corresponding planes' normal vectors
        plane_index1 = [i for i, centroid in enumerate(molecule_centroids[details[1]]) if np.array_equal(centroid, closest_centroid1)][0]
        plane_index2 = [i for i, centroid in enumerate(filtered_molecule_centroids2[molecule2]) if np.array_equal(centroid, closest_centroid2)][0]
    
        normal_vector1 = normal_vectors_planes[plane_index1]
        normal_vector2 = normal_vectors_ids2[plane_index2]
    
        # Calculate the angle between the normal vectors
        angle = calculate_angle(normal_vector1, normal_vector2)
        shortest_distances_with_angles.append((details[0], details[1], molecule2, angle, closest_centroid1, closest_centroid2))
    
    # Assuming shortest_distances_with_angles is already populated
    distances = [details[0] for details in shortest_distances_with_angles]
    angles = [details[3] if details[3] <= 90 else 180 - details[3] for details in shortest_distances_with_angles]
    # Adjust angles and create the list of adjusted angles
    
    if i==1:
        data_DistancevsAngle = pd.DataFrame({'Shortest Distance': distances, 'Angle': angles})
    else: 
        to_append= pd.DataFrame({'Shortest Distance': distances, 'Angle': angles})
        data_DistancevsAngle=pd.concat([data_DistancevsAngle, to_append], ignore_index=True)

## Create a jointplot with KDE and marginal histograms
sns.set(style="whitegrid", palette="muted")

# Create the joint plot
j = sns.jointplot(
    x='Shortest Distance', 
    y='Angle', 
    data=data_DistancevsAngle, 
    kind='kde', 
    fill=True, 
    height=8, 
    space=0,
    cmap="viridis"
)

# Add marginal histograms
j.plot_marginals(sns.histplot, kde=True, color='skyblue', bins=30, edgecolor='k')

# Customize the appearance
j.ax_joint.collections[0].set_alpha(0)  # Remove the solid fill
sns.kdeplot(
    data=data_DistancevsAngle, 
    x="Shortest Distance", 
    y="Angle", 
    fill=True, 
    ax=j.ax_joint, 
    levels=100, 
    cmap="viridis",
    alpha=0.6
)

# Adjust titles and labels
j.set_axis_labels('Shortest Distance', 'Angle (degrees)', fontsize=12)
plt.suptitle('Kernel Density Estimation with Marginal Histograms\nfor Shortest Distances and Corresponding Angles', y=1.02, fontsize=16)

# Customize the plot appearance
j.ax_joint.tick_params(labelsize=10)
j.ax_marg_x.tick_params(labelsize=10)
j.ax_marg_y.tick_params(labelsize=10)
j.ax_joint.grid(True, linestyle='--', alpha=0.7)

# Add grid and set style
sns.despine(trim=True)
plt.show()
