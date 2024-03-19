import numpy as np

# Define the three points on the plane
A = np.array([3.387995702, -9.832380299, -2.834124368])
B = np.array([4.70658381, -6.672760226, 2.043031367])
C = np.array([-4.304081681, 5.411956058, -1.172071549])

# Calculate vectors in the plane and the normal vector
AB = B - A
AC = C - A
N = np.cross(AB, AC)
N_normalized = N / np.linalg.norm(N)  # Normalize the vector

# Calculate the rotation axis (cross product of N and Y-axis unit vector)
Y = np.array([0, 1, 0])
rotation_axis = np.cross(N_normalized, Y)
rotation_axis_normalized = rotation_axis / np.linalg.norm(rotation_axis)

# Calculate the angle of rotation
angle_of_rotation = np.arccos(np.dot(N_normalized, Y))

# Construct the skew-symmetric matrix for the rotation axis
K = np.array([[0, -rotation_axis_normalized[2], rotation_axis_normalized[1]], 
              [rotation_axis_normalized[2], 0, -rotation_axis_normalized[0]], 
              [-rotation_axis_normalized[1], rotation_axis_normalized[0], 0]])

# Identity matrix
I = np.identity(3)

# Construct the rotation matrix using Rodrigues' rotation formula
R = I + np.sin(angle_of_rotation) * K + (1 - np.cos(angle_of_rotation)) * np.dot(K, K)

# Load points from the file
file_path = 'path_to_your_file.txt'  # Update this path
points = np.loadtxt(file_path, delimiter='\t')

# Apply the rotation matrix to each point
rotated_points = np.dot(points, R.T)

# Save the rotated points to a new file
rotated_file_path = 'path_to_save_aligned_points.txt'  # Update this path
np.savetxt(rotated_file_path, rotated_points, delimiter='\t')

print(f"Rotated points saved to {rotated_file_path}")

import numpy as np

# Define the two given points
P1 = np.array([-8.438852928710071311, 0.002439994260466085349, 8.910274330186290115])
P2 = np.array([8.055622267038486939, 0.5746337521623806621, -7.506408912596087113])

# Calculate the vector connecting the two points
vector = P2 - P1

# Calculate the rotation axis as the cross product of the vector and the x-axis unit vector
x_axis = np.array([1, 0, 0])
rotation_axis = np.cross(vector, x_axis)
rotation_axis_normalized = rotation_axis / np.linalg.norm(rotation_axis)

# Calculate the angle of rotation
angle_of_rotation = np.arccos(np.dot(vector / np.linalg.norm(vector), x_axis))

# Construct the skew-symmetric matrix for the rotation axis
K = np.array([[0, -rotation_axis_normalized[2], rotation_axis_normalized[1]], 
              [rotation_axis_normalized[2], 0, -rotation_axis_normalized[0]], 
              [-rotation_axis_normalized[1], rotation_axis_normalized[0], 0]])

# Identity matrix
I = np.identity(3)

# Construct the rotation matrix using Rodrigues' rotation formula
R = I + np.sin(angle_of_rotation) * K + (1 - np.cos(angle_of_rotation)) * np.dot(K, K)

# Load points from the provided file
file_path = 'path_to_your_file.txt'  # Update this path
points = np.loadtxt(file_path, delimiter='\t')

# Apply the rotation matrix to each point
rotated_points = np.dot(points, R.T)

# Save the rotated points to a new file
output_file_path = 'path_to_save_rotated_points.txt'  # Update this path
np.savetxt(output_file_path, rotated_points, delimiter='\t')

print(f"Rotated points saved to {output_file_path}")

