from Grid import Grid
from context_tools import *
import cairo, clip, cv2, random, os
import numpy as np


nx,ny = 225,225
big_array = np.zeros((nx,ny))
wx = nx//10 + 1
wy = ny//10 + 1
big_array[int(.3*nx):int(.3*nx)+wx,int(.1*ny):int(.1*ny)+wy] = 1 
big_array[int(.1*nx):int(.1*nx)+wx,int(.5*ny):int(.5*ny)+wy] = 1 
big_array[int(.6*nx):int(.6*nx)+wx,int(.6*ny):int(.6*ny)+wy] = 1

# ^^This is the main array that will serve as the object environment
def generate_keyframe_grid():
    SRSE_Grid = Grid(.05,big_array)
    Shadows = SRSE_Grid.get_all_shadows((5,5))
    Shadows.occupancy_array = Shadows.occupancy_array - SRSE_Grid.occupancy_array
    list_of_shadows = Shadows.compute_separate_shadows()

    list_of_shadows[1].label = True
    list_of_shadows[2].label = True
    with mapped_png_context("Images/keyframe_representation.png",((0,0),(10,10)),(1000,1000)) as context:
            for shadow in list_of_shadows:
                    print(f"This is my label: {shadow.label}")
                    if shadow.label == True:
                        context.set_source_rgb(1,0,0)
                    else:
                          context.set_source_rgb(0,1,0)
                    shadow.draw(context)
            context.set_source_rgb(0,0,0)
            SRSE_Grid.draw(context)


def main():
    keyframe_shadowlist = generate_keyframe_grid()
main()