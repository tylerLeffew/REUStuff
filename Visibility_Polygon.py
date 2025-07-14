import math
import matplotlib.pyplot as plt

# --------------------------------------
# Core Visibility Polygon Functionality
# --------------------------------------

def ray_segment_intersection(origin, direction, segment):
    x0, y0 = origin
    dx, dy = direction
    (x1, y1), (x2, y2) = segment

    sx, sy = x2 - x1, y2 - y1
    denominator = dx * sy - dy * sx

    if abs(denominator) < 1e-10:
        return None

    t = ((x1 - x0) * sy - (y1 - y0) * sx) / denominator
    u = ((x1 - x0) * dy - (y1 - y0) * dx) / denominator

    if t < 0 or not (0 <= u <= 1):
        return None

    return (x0 + t * dx, y0 + t * dy)

def compute_visibility_polygon(origin, segments):
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

    # Output the floating-point polygon
    visibility_polygon_float = [pt for angle, pt in sorted(intersection_points)]

    # ------------------------------
    # Convert to integer coordinates
    # ------------------------------
    visibility_polygon_int = [(int(round(x)), int(round(y))) for x, y in visibility_polygon_float]

    # Remove duplicates while preserving order
    visibility_polygon_int_unique = []
    seen = set()
    for pt in visibility_polygon_int:
        if pt not in seen:
            visibility_polygon_int_unique.append(pt)
            seen.add(pt)

    return visibility_polygon_int_unique

# --------------------------------------
# Visualization (Optional Testing)
# --------------------------------------

def plot_visibility_polygon(origin, polygon_int, segments):
    """Visualize environment, obstacles, and integer visibility polygon."""
    plt.figure(figsize=(7, 7))

    for seg in segments:
        plt.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]], 'k-', lw=1.5)

    if polygon_int:
        xs, ys = zip(*polygon_int)
        plt.fill(xs, ys, color='lightblue', alpha=0.4, label='Visibility Polygon')
        plt.plot(xs + (xs[0],), ys + (ys[0],), 'b-', lw=1)

    plt.plot(origin[0], origin[1], 'ro', label='Observer')
    plt.gca().set_aspect('equal')
    plt.title("Integer Output Visibility Polygon")
    plt.legend()
    plt.show()

# --------------------------------------
# Example Usage for Testing
# --------------------------------------

if __name__ == "__main__":
    # Example environment with multiple holes
    outer_square = [
        ((0,0),(10,0)), ((10,0),(10,10)), ((10,10),(0,10)), ((0,10),(0,0))
    ]

    hole1 = [((3,3),(5,3)), ((5,3),(5,5)), ((5,5),(3,5)), ((3,5),(3,3))]
    hole2 = [((6,6),(8,6)), ((8,6),(8,8)), ((8,8),(6,8)), ((6,8),(6,6))]
    hole3 = [((2,7),(4,7)), ((4,7),(4,9)), ((4,9),(2,9)), ((2,9),(2,7))]

    segments = outer_square + hole1 + hole2 + hole3

    # Observer position
    origin = (5, 2)

    # Compute integer visibility polygon
    polygon_int = compute_visibility_polygon(origin, segments)

    # Optional visualization for validation
    plot_visibility_polygon(origin, polygon_int, segments)

    # polygon_int now ready for:
    # - Overlay as a mask on your occupancy grid
    # - Coverage and exploration planning
    # - Efficient further processing
