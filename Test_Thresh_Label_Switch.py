import cv2
from Grid import Grid
import numpy as np
from context_tools import mapped_png_context
from color_loader import get_color_list

def edge_points(array):
    contours, heirarchy = cv2.findContours(array, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours



if __name__ == "__main__":
    colors = get_color_list()
    image = cv2.imread("test_shapes/blob_indi.jpeg",0)
    image = image/255
    cv2.imshow("raw image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    grid = Grid(image,resolution=.1)

    points = edge_points(grid.occupancy_array)

    with mapped_png_context("test_shapes/blob_indi_output.png",grid.calc_aabb(),(1000,1000)) as context:
        grid.draw(context,colors["teal"])
