from Image_Modifier import ImageModifier
import numpy as np
import Raycaster3 as rc
import Array_Toolkit as atk
import math, time
import cv2


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
if __name__ == "__main__":
    array = np.zeros((1000, 1000))
    # array[(array.shape[0]//2)-10:(array.shape[0]//2)+20, (array.shape[1]//2)-10:(array.shape[1]//2)+5] = 1
    ray = rc.Raycaster(array)
    array[600:750, 600:700] = 1
    array[650:680, 570:600] = 1
    array[220:450, 590:800] = 1
    array[50:150, 600:710] = 1
    array[700:800, 10:110] = 1
    array[10:40, 10:40] = 1

    # x, y = 300, 500
    # theta = math.pi          # Facing right (0 radians)
    # sa = math.pi  *2  # 180° field of view
    # resolution = 1000 # 9 evenly spaced rays

    # targets = ray.get_ray_endpoints(x, y, theta, sa, resolution)

    # print(targets)

    # for target in targets:
    #     ray.raycast(x, y, target[0], target[1], stop_on_intersection=True)

    coords = unpack_contours(array)
    for coord in coords:
        print(coord[0],",", coord[1])
        ray.raycast(300, 500, coord[1], coord[0], stop_on_intersection=False)
        # printer = array + ray.working_array
        # atk.write_array_to_image(array=printer, filepath="raytrace3.png")
        # time.sleep(2)


    ray.iterate_triangle((300,500), (ray.coordinate_list[0]), (ray.coordinate_list[1]), ray.visit2)
    # ray.iterate_triangle((300,500), (ray.coordinate_list[1]), (ray.coordinate_list[2]), ray.visit2)
    printer = array + ray.working_array
    atk.write_array_to_image(array=printer, filepath="raytrace4.png")
    print("fin")