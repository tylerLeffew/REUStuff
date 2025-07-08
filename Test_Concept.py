from Image_Modifier import ImageModifier
import numpy as np
import Raycaster4 as rc
import Array_Toolkit as atk
import Visibility_Polygon2 as vp
import math, time
import cv2
import Dynamic_Visualization as dv


def unpack_contours(image, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE):
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

def draw_circles_with_lines(array, coordinates, circle_radius=2, line_color=(0, 0, 255), circles = True):
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

        if circles:
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

def test1():

    image = cv2.imread("Images/object_envs/9roomgrid.png",0)
    image = image/255
    image = 1-image
    array = image
    obs = (array.shape[0]//2, array.shape[1]//2)
    print(array.dtype)
    polygon = vp.get_visibility_polygon(grid=array, observer_rc=obs)
    polygon = atk.cartesian_to_grid_coords(polygon, array.shape)

    polygon2 = vp.get_visibility_polygon(grid=array, observer_rc=(1160,1200))
    polygon2 = atk.cartesian_to_grid_coords(polygon2, array.shape)

    polygon3 = vp.get_visibility_polygon(grid=array, observer_rc=(400,350))
    polygon3 = atk.cartesian_to_grid_coords(polygon3, array.shape)

    color = draw_circles_with_lines(array, polygon, circle_radius=10,line_color=(0,255,0),circles=False)
    color += draw_circles_with_lines(array, polygon2, circle_radius=10,circles=False)
    color += draw_circles_with_lines(array, polygon3, circle_radius=10,line_color=(255,0,0),circles=False)
    cv2.circle(color, (obs[1],obs[0]), radius=20, color=(0, 255, 0), thickness=-1)
    cv2.circle(color, (1200,1160), radius=20, color=(0, 0, 255), thickness=-1)
    cv2.circle(color, (350,400), radius=20, color=(255, 0, 0), thickness=-1)
    cv2.imwrite("raytrace10.png", color)
    print("fin")

if __name__ == "__main__":
    # threshold, image = dv.thresh_and_show("Images/object_envs/rsz_custom_env.png")
    image = cv2.imread("Images/object_envs/rsz_custom_env.png",0)
    image = image/255
    image = 1-image
    ret,image= cv2.threshold(image,0.8,1,cv2.THRESH_BINARY)
    obs = (image.shape[0]//2, image.shape[1]//2)
    color = image
    polygon = vp.get_visibility_polygon(grid=image, observer_rc=obs)
    polygon = atk.cartesian_to_grid_coords(polygon, image.shape)
    print("polygon 1 created")
    polygon2 = vp.get_visibility_polygon(grid=image, observer_rc=(290,350))
    polygon2 = atk.cartesian_to_grid_coords(polygon2, image.shape)
    print("polygon 2 created")
    polygon3 = vp.get_visibility_polygon(grid=image, observer_rc=(66,70))
    polygon3 = atk.cartesian_to_grid_coords(polygon3, image.shape)
    print("polygon 3 created")
    color = draw_circles_with_lines(image, polygon, circle_radius=10,line_color=(0,255,0),circles=False)
    color += draw_circles_with_lines(image, polygon2, circle_radius=10,line_color=(0,0,255),circles=False)
    color += draw_circles_with_lines(image, polygon3, circle_radius=10,line_color=(255,0,0),circles=False)
    # image = (image * 255).astype(np.uint8)
    # color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.circle(color, (obs[1],obs[0]), radius=5, color=(0, 255, 0), thickness=-1)
    cv2.circle(color, (350,290), radius=5, color=(0, 0, 255), thickness=-1)
    cv2.circle(color, (70,66), radius=5, color=(255, 0, 0), thickness=-1)
    print(color.dtype, color.shape)
    print("eh")
    cv2.imwrite("raytrace11.png", color)
    print("fin")