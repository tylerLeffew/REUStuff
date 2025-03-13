import numpy as np
import triangle
import matplotlib.pyplot as plt

# Function to compute the circumcenter of a triangle
def circumcenter(triangle_points):
    A, B, C = np.array(triangle_points)
    D = 2 * (A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]))

    Ux = ((A[0]**2 + A[1]**2) * (B[1] - C[1]) +
          (B[0]**2 + B[1]**2) * (C[1] - A[1]) +
          (C[0]**2 + C[1]**2) * (A[1] - B[1])) / D

    Uy = ((A[0]**2 + A[1]**2) * (C[0] - B[0]) +
          (B[0]**2 + B[1]**2) * (A[0] - C[0]) +
          (C[0]**2 + C[1]**2) * (B[0] - A[0])) / D

    return np.array([Ux, Uy])

# Function to compute the area of a triangle
def triangle_area(triangle_points):
    A, B, C = np.array(triangle_points)
    return 0.5 * abs(A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]))

# Function to compute the incenter by finding the largest empty circumcircle
def compute_incenter(triangulated, vertices):
    circumcenters = np.array([circumcenter(triangulated['vertices'][tri]) for tri in triangulated['triangles']])
    return max(circumcenters, key=lambda c: min(np.linalg.norm(c - np.array(vertices), axis=1)))

# Function to compute the weighted circumcenter, averaging circumcenters based on triangle area
def compute_weighted_circumcenter(triangulated):
    total_area = 0
    weighted_center = np.array([0.0, 0.0])
    for tri in triangulated['triangles']:
        points = triangulated['vertices'][tri]
        area = triangle_area(points)
        total_area += area
        weighted_center += area * circumcenter(points)
    return weighted_center / total_area if total_area != 0 else weighted_center

# Function to find a label point using the selected method
def find_label_point(vertices, method="incenter"):
    # Generate segments from the list of vertices to define the polygon
    segments = [[i, i + 1] for i in range(len(vertices) - 1)] + [[len(vertices) - 1, 0]]
    polygon = {"vertices": vertices, "segments": segments}
    triangulated = triangle.triangulate(polygon, 'pD')
    
    # Compute the label point using the specified method
    if method == "incenter":
        return compute_incenter(triangulated, vertices)
    elif method == "weighted_circumcenter":
        return compute_weighted_circumcenter(triangulated)
    else:
        raise ValueError("Invalid method. Choose 'incenter' or 'weighted_circumcenter'.")

# Example usage:
vertices = [[0, 0], [4, 0], [4, 3], [2, 5], [0, 3]]
label_point = find_label_point(vertices, method="incenter")
print("Label Point (Incenter):", label_point)

