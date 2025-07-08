import cv2
import numpy as np
def write_array_to_image(array, filepath):
	array = array.astype(np.uint8)
	array = array * 255 
	cv2.imwrite(filepath, array)
	array = array / 255
	array = array.astype(np.float64)

def rc_to_xy(point_rc, grid_shape):
    """
    Convert (row, col) -> (x, y) for Cartesian usage in visibility tools.
    Flips the y-axis to match y increasing upward.
    """
    row, col = point_rc
    x = col
    y = grid_shape[0] - row
    return (x, y)

def grid_to_segments(grid, grid_shape):
    """
    Given a binary occupancy grid and its shape, extract obstacle contours
    and convert them to segments suitable for the visibility polygon tool.
    """
    segments = []

    # Convert grid to uint8 for OpenCV
    grid_uint8 = (grid * 255).astype(np.uint8)

    # Find contours
    contours, _ = cv2.findContours(grid_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        contour = contour.squeeze()
        if len(contour.shape) == 1:
            # Single point
            continue
        for i in range(len(contour)):
            p1_rc = (contour[i][1], contour[i][0])  # (row, col)
            p2_rc = (contour[(i + 1) % len(contour)][1], contour[(i + 1) % len(contour)][0])
            p1_xy = rc_to_xy(p1_rc, grid_shape)
            p2_xy = rc_to_xy(p2_rc, grid_shape)
            segments.append((p1_xy, p2_xy))

    # Add outer boundary
    w, h = grid_shape[1], grid_shape[0]
    outer_boundary = [
        ((0,0),(w,0)), ((w,0),(w,h)),
        ((w,h),(0,h)), ((0,h),(0,0))
    ]
    segments.extend(outer_boundary)

    return segments

def cartesian_to_grid_coords(polygon_cartesian, grid_shape):
    """
    Converts a list of (x, y) Cartesian coordinates (x right, y up)
    to a list of (row, col) grid coordinates (row down, col right).

    Parameters:
        polygon_cartesian (list of tuples): List of (x, y) points.
        grid_shape (tuple): (rows, cols) of the grid.

    Returns:
        list of (row, col) points.
    """
    converted = [(grid_shape[0] - y, x) for (x, y) in polygon_cartesian]
    converted.append(converted[0])
    return converted

def draw_polygon_on_array(array, vertices, color=(255, 0, 0), thickness=1, is_closed=True):
    """
    Draws a polygon on the given array using OpenCV.

    Parameters:
        array (np.ndarray): The array to draw on (grayscale or BGR).
        vertices (list of tuples): List of (row, col) coordinates defining the polygon vertices.
        color (tuple or int): Color for the polygon.
            - For grayscale: int (e.g., 255).
            - For BGR: tuple (B, G, R). Default is blue (255, 0, 0).
        thickness (int): Line thickness. Use -1 to fill the polygon.
        is_closed (bool): Whether to close the polygon. Default True.

    Returns:
        np.ndarray: The array with the polygon drawn.
    """
    # Convert (row, col) to (col, row) for OpenCV (x, y)
    pts = np.array([[ (col, row) for (row, col) in vertices ]], dtype=np.int32)
    
    if thickness == -1:
        cv2.fillPoly(array, pts, color)
    else:
        cv2.polylines(array, pts, isClosed=is_closed, color=color, thickness=thickness)

    return array