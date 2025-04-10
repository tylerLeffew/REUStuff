import cv2,math
import numpy as np
from Grid import Grid
from context_tools import mapped_png_context, vflip_font
import matplotlib.pyplot as plt

if __name__ == "__main__":

    def show_array(array):
        plt.imshow(array, cmap='gray')
        plt.axis('off')
        plt.show()

    def add_robot(position, context):
       
       """
       Draws a blue circle representing a robot at the given position in the given context
       
       Parameters:
       position (tuple of two floats): The x and y coordinates of the position of the robot
       context (cairo.Context): The context in which to draw the robot
       """
       context.set_source_rgb(0, 0, 1)
       context.arc(position[0],position[1],(2.3),0,2*math.pi)
       context.fill()

    image = cv2.imread("Images/object_envs/9roomgrid50.png",0)
    image = image/255
    image = 1- image
    ret, thresh = cv2.threshold(image,.4,1,cv2.THRESH_BINARY)
    cv2.imshow("image",thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(thresh.dtype)
    grid = Grid(thresh,.1)
    print(grid.calc_aabb())
    grid2 = grid.get_all_shadows((44,35))
    # print(grid2.occupancy_array[0,0])
    print(grid2.occupancy_array.shape)
    with mapped_png_context("test_example_output4.png",grid.calc_aabb(),svg_size=(grid.occupancy_array.shape[1],grid.occupancy_array.shape[0])) as context:
        grid.occupancy_array = grid.occupancy_array[::-1, :]
        context.set_source_rgb(0,0,0)
        grid.draw(context=context)
        context.set_source_rgb(.84,.6,.94)
        grid2.occupancy_array = grid2.occupancy_array[::-1, :]
        grid2.draw(context=context)
        add_robot([44,35],context)
    #     add_robot([0,0],context)
    #     add_robot([0,142],context)
    #     add_robot([176,142],context)
    #     add_robot([176,0],context)
    # print('done')


    # show_array(grid.occupancy_array)
    show_array(grid2.occupancy_array[::-1, :])



def main():
    main()