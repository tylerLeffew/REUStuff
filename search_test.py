import cv2
import numpy as np
from Grid import Grid
from context_tools import mapped_png_context
import math

def add_robot(position, context):
    
    """
    Draws a blue circle representing a robot at the given position in the given context
    
    Parameters:
    position (tuple of two floats): The x and y coordinates of the position of the robot
    context (cairo.Context): The context in which to draw the robot
    """
    context.set_source_rgb(0, 0, 1)
    context.arc(position[0],position[1],(1.5),0,2*math.pi)
    context.fill()

image = cv2.imread("Images/object_envs/small_custom_env.png",0)
image = image/255

grid = Grid(image, resolution=1)

print(grid.calc_aabb())

grid2 = grid.get_all_shadows((40,50))

for i in range(grid2.occupancy_array.shape[0]):
    out = ""
    for j in range(grid2.occupancy_array.shape[1]):
        out += str(grid2.occupancy_array[i][j])
    print(out)


with mapped_png_context("Images/Output_Images/test_example_output1.png",grid.calc_aabb(),svg_size=(grid.occupancy_array.shape[1],grid.occupancy_array.shape[0])) as context:
    context.set_source_rgb(0,0,1)
    grid2.draw(context)
    add_robot((40,50),context)

