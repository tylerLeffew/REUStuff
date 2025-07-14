import numpy as np
import cv2
import math
import matplotlib.pyplot as plt

def rc_to_xy(point_rc, grid_shape):
    row, col = point_rc
    x = col
    y = grid_shape[0] - row
    return (x, y)

def extract_segments_from_grid(grid, grid_shape):
    segments = []
    grid_for_cv = (grid * 255).astype(np.uint8)
    contours, _ = cv2.findContours(grid_for_cv, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        contour = contour.squeeze()
        if contour.ndim == 1:
            continue
        for i in range(len(contour)):
            p1_rc = (contour[i][1], contour[i][0])
            p2_rc = (contour[(i+1)%len(contour)][1], contour[(i+1)%len(contour)][0])
            p1_xy = rc_to_xy(p1_rc, grid_shape)
            p2_xy = rc_to_xy(p2_rc, grid_shape)
            segments.append((p1_xy, p2_xy))
    w, h = grid_shape[1], grid_shape[0]
    segments += [((0,0),(w,0)), ((w,0),(w,h)), ((w,h),(0,h)), ((0,h),(0,0))]
    return segments

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
    visibility_polygon_float = [pt for angle, pt in sorted(intersection_points)]
    visibility_polygon_int = [(int(round(x)), int(round(y))) for x, y in visibility_polygon_float]
    visibility_polygon_int_unique = []
    seen = set()
    for pt in visibility_polygon_int:
        if pt not in seen:
            visibility_polygon_int_unique.append(pt)
            seen.add(pt)
    return visibility_polygon_int_unique

def polygon_to_mask(polygon_int, grid_shape):
    mask = np.zeros(grid_shape, dtype=np.uint8)
    # Corrected conversion to (col, row) for cv2.fillPoly
    pts = np.array([[[x, grid_shape[0] - y] for (x, y) in polygon_int]], dtype=np.int32)
    cv2.fillPoly(mask, pts, 1)
    return mask

def plot_mask_and_polygon(grid, mask, polygon_int, observer_rc):
    plt.figure(figsize=(10, 10))
    combined = grid.copy().astype(float)
    combined[mask == 1] = 0.5
    plt.imshow(combined, cmap='gray', origin='upper')

    if polygon_int:
        xs, ys = zip(*polygon_int)
        xs = list(xs)  # convert to list for concatenation
        ys_flipped = [grid.shape[0] - y for y in ys]
        plt.plot(xs + [xs[0]], ys_flipped + [ys_flipped[0]], 'r-', lw=1)

    plt.plot(observer_rc[1], observer_rc[0], 'bo', label='Observer')
    plt.title("Visibility Polygon Overlay on Grid")
    plt.legend()
    plt.show()

def get_visibility_polygon(grid, observer_rc):
    grid_shape = grid.shape
    observer_xy = rc_to_xy(observer_rc, grid_shape)
    segments = extract_segments_from_grid(grid, grid_shape)
    polygon_int = compute_visibility_polygon(observer_xy, segments)
    return polygon_int

if __name__ == "__main__":
    grid_shape = (1000, 1000)
    grid = np.zeros(grid_shape, dtype=np.uint8)
    # Add test boxes:
    grid[100:200, 100:200] = 1
    grid[400:500, 600:700] = 1
    grid[800:900, 300:400] = 1
    observer_rc = (500, 500)
    observer_xy = rc_to_xy(observer_rc, grid_shape)
    segments = extract_segments_from_grid(grid, grid_shape)
    polygon_int = compute_visibility_polygon(observer_xy, segments)
    visibility_mask = polygon_to_mask(polygon_int, grid_shape)
    print("Visibility Polygon:", polygon_int)
    plot_mask_and_polygon(grid, visibility_mask, polygon_int, observer_rc)
