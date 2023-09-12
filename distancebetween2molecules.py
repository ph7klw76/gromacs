import math
inside=['72','78','71','39','40','45','41','44','43','47','50','48','49','62','63','65','67','69','61','52','51','59','57','55','53']
inside2=['182','188','181','149','150','155','151','154','153','157','160','158','159','172','173','175','177','179','171','162','161','169','167','165','163']
def read_coordinates_from_gro(gro_lines,inside):
    coordinates = []
    for line in gro_lines:
        # Skip the header or empty lines
        if len(line.split()) != 6:
            continue
        if line.split()[2] in inside:
            x, y, z = map(float, line.split()[3:6])
            coordinates.append((x, y, z))
    return coordinates

def distance(coord1, coord2):
    """Calculate the Euclidean distance between two points in 3D space."""
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2 + (coord1[2] - coord2[2])**2)

def find_min_distance(molecule1, molecule2):
    """Find the minimum distance between any two atoms from two different molecules."""
    min_distance = float('inf')  # Initialize with a very large number
    for coord1 in molecule1:
        for coord2 in molecule2:
            current_distance = distance(coord1, coord2)
            min_distance = min(min_distance, current_distance)
    return min_distance

if __name__ == "__main__":
    with open("D:/B16/double/729DJYB_128DJYB.gro",'r') as f:
        gro_data =f.readlines()
    gro_lines = gro_data
    molecule1 = read_coordinates_from_gro(gro_lines, inside)
    molecule2 = read_coordinates_from_gro(gro_lines, inside2)
    min_distance = find_min_distance(molecule1, molecule2)
    print(f"The minimum distance between any two atoms is {min_distance:.4f} units.")
