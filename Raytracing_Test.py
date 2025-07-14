import math
import matplotlib.pyplot as plt

# ------------------------
# Intersection Utilities
# ------------------------

def ray_segment_intersection(origin, direction, segment):
    """Compute intersection point of a ray and a segment if it exists."""
    x0, y0 = origin
    dx, dy = direction
    (x1, y1), (x2, y2) = segment

    sx, sy = x2 - x1, y2 - y1
    denominator = dx * sy - dy * sx

    if abs(denominator) < 1e-10:
        return None  # Parallel

    t = ((x1 - x0) * sy - (y1 - y0) * sx) / denominator
    u = ((x1 - x0) * dy - (y1 - y0) * dx) / denominator

    if t < 0 or not (0 <= u <= 1):
        return None

    return (x0 + t * dx, y0 + t * dy)

# ------------------------
# Visibility Polygon Core
# ------------------------

def compute_visibility_polygon(origin, segments):
    """Compute visibility polygon from an origin given environment segments."""
    x0, y0 = origin
    epsilon = 1e-8
    angles = []

    for seg in segments:
        for p in seg:
            angle = math.atan2(p[1] - y0, p[0] - x0)
            angles.extend([angle - epsilon, angle, angle + epsilon])

    intersection_points = []

    for angle in sorted(angles):
        dx, dy = math.cos(angle), math.sin(angle)
        closest_intersection = None
        min_dist = float('inf')

        for seg in segments:
            intersection = ray_segment_intersection(origin, (dx, dy), seg)
            if intersection:
                dist = (intersection[0] - x0)**2 + (intersection[1] - y0)**2
                if dist < min_dist:
                    min_dist = dist
                    closest_intersection = intersection

        if closest_intersection:
            intersection_points.append((angle, closest_intersection))

    visibility_polygon = [pt for angle, pt in sorted(intersection_points)]
    return visibility_polygon

# ------------------------
# Visualization
# ------------------------

def plot_visibility_polygon(origin, polygon, segments):
    """Visualize environment, holes, and visibility polygon."""
    plt.figure(figsize=(8, 8))

    # Draw environment segments
    for seg in segments:
        plt.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]], 'k-', lw=1.5)

    # Draw visibility polygon
    if polygon:
        xs, ys = zip(*polygon)
        plt.fill(xs, ys, color='lightblue', alpha=0.4, label='Visibility Polygon')
        plt.plot(xs + (xs[0],), ys + (ys[0],), 'b-', lw=1)

    # Draw observer
    plt.plot(origin[0], origin[1], 'ro', label='Observer')

    plt.xlim(-1, 11)
    plt.ylim(-1, 11)
    plt.gca().set_aspect('equal')
    plt.title("Visibility Polygon with Multiple Holes")
    plt.legend()
    plt.show()

# ------------------------
# Environment with Multiple Holes
# ------------------------

# Outer boundary (10x10)
outer_square = [
    ((0,0),(10,0)), ((10,0),(10,10)), ((10,10),(0,10)), ((0,10),(0,0))
]

# Hole 1: lower left
hole1 = [
    ((2,2),(4,2)), ((4,2),(4,4)), ((4,4),(2,4)), ((2,4),(2,2))
]

# Hole 2: upper right
hole2 = [
    ((6,6),(8,6)), ((8,6),(8,8)), ((8,8),(6,8)), ((6,8),(6,6))
]

# Hole 3: upper left
hole3 = [
    ((1,7),(3,7)), ((3,7),(3,9)), ((3,9),(1,9)), ((1,9),(1,7))
]

# Combine all segments
segments = outer_square + hole1 + hole2 + hole3

# Observer position (can be moved for testing)
origin = (7, 1.1)

# ------------------------
# Execute
# ------------------------

polygon = compute_visibility_polygon(origin, segments)
print("Visibility Polygon:", polygon)
plot_visibility_polygon(origin, polygon, segments)
