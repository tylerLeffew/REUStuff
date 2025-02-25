import numpy as np
import triangle
import matplotlib.pyplot as plt
import json


def load_polygon_from_json(file_path):
    """Load polygon data from a JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Extract vertices from JSON
    vertices = [[v["x"], v["y"]] for v in data["vertices"]]
    
    # Generate segments automatically
    segments = [[i, i + 1] for i in range(len(vertices) - 1)] + [[len(vertices) - 1, 0]]
    
    return {"vertices": vertices, "segments": segments}


def circumcenter(triangle_points):
    """Compute the circumcenter of a triangle given its vertices."""
    A, B, C = np.array(triangle_points)
    D = 2 * (A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]))

    Ux = ((A[0]**2 + A[1]**2) * (B[1] - C[1]) +
          (B[0]**2 + B[1]**2) * (C[1] - A[1]) +
          (C[0]**2 + C[1]**2) * (A[1] - B[1])) / D

    Uy = ((A[0]**2 + A[1]**2) * (C[0] - B[0]) +
          (B[0]**2 + B[1]**2) * (A[0] - C[0]) +
          (C[0]**2 + C[1]**2) * (B[0] - A[0])) / D

    return np.array([Ux, Uy])


def triangle_area(triangle_points):
    """Compute the area of a triangle given its vertices."""
    A, B, C = np.array(triangle_points)
    return 0.5 * abs(A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]))

def find_incenter(triangulated, polygon_vertices):
    """Find the incenter of the polygon by locating the largest empty circle."""
    circumcenters = np.array([circumcenter(triangulated['vertices'][tri]) for tri in triangulated['triangles']])

    # Find the circumcenter farthest from polygon edges
    return max(circumcenters, key=lambda c: min(np.linalg.norm(c - np.array(polygon_vertices), axis=1)))



def is_point_inside_polygon(point, polygon_vertices):
    """Check if a point is inside a polygon using the Ray-Casting Algorithm."""
    x, y = point
    inside = False
    n = len(polygon_vertices)
    p1x, p1y = polygon_vertices[0]
    for i in range(n + 1):
        p2x, p2y = polygon_vertices[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def project_point_onto_polygon(point, polygon_vertices):
    """Project a point onto the nearest polygon boundary if it's outside."""
    closest_point = None
    min_distance = float('inf')

    for i in range(len(polygon_vertices)):
        A = np.array(polygon_vertices[i])
        B = np.array(polygon_vertices[(i + 1) % len(polygon_vertices)])

        # Compute projection of `point` onto segment AB
        AP = point - A
        AB = B - A
        t = np.clip(np.dot(AP, AB) / np.dot(AB, AB), 0, 1)
        projection = A + t * AB

        # Find the closest projection
        distance = np.linalg.norm(point - projection)
        if distance < min_distance:
            min_distance = distance
            closest_point = projection

    return closest_point


def find_weighted_circumcenter(triangulated, polygon_vertices):
    """Find the weighted circumcenter by averaging circumcenters based on triangle area,
    ensuring it remains inside the polygon."""
    total_area = 0
    weighted_center = np.array([0.0, 0.0])

    for tri in triangulated['triangles']:
        points = triangulated['vertices'][tri]
        area = triangle_area(points)
        total_area += area
        weighted_center += area * circumcenter(points)

    if total_area == 0:
        return weighted_center  # Edge case: Return early if no valid area

    weighted_center /= total_area  # Compute final position

    # Ensure the center is inside the polygon
    if not is_point_inside_polygon(weighted_center, polygon_vertices):
        weighted_center = project_point_onto_polygon(weighted_center, polygon_vertices)

    return weighted_center


def plot_triangulation(triangulated, polygon, center=None, center_label=""):
    """Plot the triangulated polygon and optionally mark a center point."""
    plt.triplot(triangulated['vertices'][:, 0], triangulated['vertices'][:, 1], triangulated['triangles'], 'go-')
    plt.plot(triangulated['vertices'][:, 0], triangulated['vertices'][:, 1], 'ro', label="Vertices")

    if center is not None:
        plt.plot(center[0], center[1], 'bo', markersize=10, label=center_label)

    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title(f"{center_label} of Polygon")
    plt.legend()
    plt.show()


def main():
    """Main function to execute triangulation and center calculations."""
    # Load polygon from JSON file
    polygon = load_polygon_from_json("L.json")

    # Compute Delaunay triangulation
    triangulated = triangle.triangulate(polygon, 'pD')

    # Compute centers
    incenter = find_incenter(triangulated, polygon['vertices'])
    weighted_circumcenter = find_weighted_circumcenter(triangulated, polygon['vertices'])

    # Plot results
    plot_triangulation(triangulated, polygon, incenter, "Incenter")
    plot_triangulation(triangulated, polygon, weighted_circumcenter, "Weighted Circumcenter")


if __name__ == "__main__":
    main()
