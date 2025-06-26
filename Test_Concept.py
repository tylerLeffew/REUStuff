from Image_Modifier import ImageModifier
import numpy as np
import Raycaster3 as rc
import Array_Toolkit as atk
import math, time
import cv2
from Dynamic_Visualization import thresh_and_show


def unpack_contours(image, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE):
    """
    Runs cv2.findContours() on the given binary image and unpacks all contours
    into a flat list of (x, y) integer coordinate tuples.

    Parameters:
    - image: binary (thresholded) image
    - mode: contour retrieval mode (default: RETR_EXTERNAL)
    - method: contour approximation method (default: CHAIN_APPROX_SIMPLE)

    Returns
    - coords: list of (x, y) points from all contours
    """
    image = np.copy(image).astype(np.uint8)
    contours, _ = cv2.findContours(image, mode, method)
    coords = []
    print(contours)

    for contour in contours:
        for point in contour:
            x, y = point[0]  # contour has shape (N, 1, 2)
            coords.append((x, y))

    return coords

def draw_circles_on_grid(array, coordinates, circle_radius=2, circle_color=(0, 0, 255)):
    """
    Convert binary grid to color and draw circles on given coordinates.

    Parameters:
        array (np.ndarray): 2D array with values 0 or 1
        coordinates (list of (x, y)): List of cell coordinates (x=col, y=row)
        circle_radius (int): Radius of each circle (default: 2)
        circle_color (tuple): BGR color for circles (default: red)

    Returns:
        np.ndarray: Color image with circles
    """
    # Scale from 0/1 to 0/255
    grayscale = (array * 255).astype(np.uint8)

    # Convert to BGR color
    color_image = cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR)

    # Draw circles
    for x, y in coordinates:
        cv2.circle(color_image, (y, x), radius=circle_radius, color=circle_color, thickness=-1)

    return color_image

def draw_circles_with_gradient(array, coordinates, circle_radius=2):
    """
    Draws circles with a color gradient and overlays point indices as labels.

    Parameters:
        array (np.ndarray): 2D binary array (0 or 1)
        coordinates (list of (x, y)): List of coordinates (x=col, y=row)
        circle_radius (int): Radius of the circles

    Returns:
        np.ndarray: Color BGR image with drawn circles and labels
    """
    # Scale binary array to 0–255 grayscale
    grayscale = (array * 255).astype(np.uint8)
    color_image = cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR)

    n = len(coordinates)
    for idx, (x, y) in enumerate(coordinates):
        # Gradient color: blue (first) to red (last)
        r = int(255 * (idx / (n - 1))) if n > 1 else 255
        b = 255 - r
        color = (b, 0, r)  # BGR

        # Draw filled circle
        cv2.circle(color_image, (y, x), radius=circle_radius, color=color, thickness=-1)

        # Draw index label (white text slightly offset)
        cv2.putText(
            color_image, str(idx), (y + 3, x - 3),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.3,
            color=(255, 255, 255),
            thickness=1,
            lineType=cv2.LINE_AA
        )

    return color_image

def draw_circles_with_lines(array, coordinates, circle_radius=2, line_color=(0, 0, 255)):
    """
    Draws a sequence of circles with gradient color, labels, and connecting lines.

    Parameters:
        array (np.ndarray): 2D binary array (0 or 1)
        coordinates (list of (x, y)): List of coordinates (x=col, y=row)
        circle_radius (int): Radius of the circles
        line_color (tuple): BGR color for connecting lines (default red)

    Returns:
        np.ndarray: Color BGR image with gradient circles, labels, and connecting lines
    """
    # Scale binary grid to 0–255 grayscale
    grayscale = (array * 255).astype(np.uint8)
    color_image = cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR)

    n = len(coordinates)
    for idx, (x, y) in enumerate(coordinates):
        # Gradient color from blue (first) to red (last)
        r = int(255 * (idx / (n - 1))) if n > 1 else 255
        b = 255 - r
        circle_color = (b, 0, r)

        # Draw filled circle
        cv2.circle(color_image, (y, x), radius=circle_radius, color=circle_color, thickness=-1)

        # Draw index label
        cv2.putText(
            color_image, str(idx), (y + 3, x - 3),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.3,
            color=(255, 255, 255),
            thickness=1,
            lineType=cv2.LINE_AA
        )

        # Draw line from previous point
        if idx > 0:
            x_prev, y_prev = coordinates[idx - 1]
            cv2.line(color_image, (y_prev, x_prev), (y, x), color=line_color, thickness=2)

    return color_image

if __name__ == "__main__":
    array = np.zeros((1000, 1000))
    image = cv2.imread("Images/object_envs/9roomgrid.png",0)
    image = image/255
    image = 1 - image
    array = image
    # array = array.astype(np.uint8)
    # array[(array.shape[0]//2)-10:(array.shape[0]//2)+20, (array.shape[1]//2)-10:(array.shape[1]//2)+5] = 1
    ray = rc.Raycaster(array)
    ray2 = rc.Raycaster(array)
    ray3 = rc.Raycaster(array)
    # array[600:750, 600:700] = 1
    # array[650:680, 570:600] = 1
    # array[220:450, 590:800] = 1
    # array[50:150, 600:690] = 1
    # array[700:800, 10:110] = 1
    # array[10:40, 10:40] = 1
    # Initialize empty occupancy grid
    # array = np.zeros((1000, 1000))

    # x, y = 300, 500
    # theta = math.pi          # Facing right (0 radians)
    # sa = math.pi  *2  # 180° field of view
    # resolution = 1000 # 9 evenly spaced rays

    # targets = ray.get_ray_endpoints(x, y, theta, sa, resolution)

    # print(targets)

    # for target in targets:
    #     ray.raycast(x, y, target[0], target[1], stop_on_intersection=True)

    coords = unpack_contours(array)
    print(coords)
    for coord in coords:
        ray.raycast(array.shape[0]//2, array.shape[1]//2, coord[1], coord[0], stop_on_intersection=False)
        ray2.raycast((array.shape[0]//4)-75, (array.shape[1]//4) - 100, coord[1], coord[0], stop_on_intersection=False)
        ray3.raycast(array.shape[0]-275, (array.shape[1]) - 300, coord[1], coord[0], stop_on_intersection=False)
        # printer = array + ray.working_array
        # atk.write_array_to_image(array=printer, filepath="raytrace3.png")
        # time.sleep(2)

    # ray.iterate_triangle((300,500), (ray.coordinate_list[0]), (ray.coordinate_list[2]), ray.visit2)
    # ray.iterate_triangle((300,500), (ray.coordinate_list[2]), (ray.coordinate_list[5]), ray.visit2)
    # ray.iterate_triangle((300,500), (ray.coordinate_list[3]), (ray.coordinate_list[4]), ray.visit2)
    # ray.iterate_triangle((300,500), (ray.coordinate_list[4]), (ray.coordinate_list[5]), ray.visit2)
    # print(ray.coordinate_list[0], ray.coordinate_list[1], ray.coordinate_list[2])
    printer = array + ray.working_array + ray2.working_array + ray3.working_array
    printer = 1 - printer
    # color = draw_circles_with_lines(printer, ray.coordinate_list, circle_radius=10)
    # cv2.imwrite("raytrace5.png", color)
    atk.write_array_to_image(array=printer, filepath="raytrace5.png")
    print(array.shape)
    print("fin")