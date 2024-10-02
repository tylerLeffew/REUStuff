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

    list_of_shadows = Shadows.compute_separate_shadows()

    list_of_shadows[1].label = True
    # list_of_shadows[2].label = True
    # with mapped_png_context("Test_Shadow_Tracking_Images/keyframe_representation.png",((0,0),(10,10)),(1000,1000)) as context:
    #         for shadow in list_of_shadows:
    #                 print(f"This is my label: {shadow.label}")
    #                 if shadow.label == True:
    #                     context.set_source_rgb(1,0,0)
    #                 else:
    #                       context.set_source_rgb(0,1,0)
    #                 shadow.draw(context)
    #         context.set_source_rgb(0,0,0)
            # SRSE_Grid.draw(context)
    return list_of_shadows

def generate_nothing_grid():
    SRSE_Grid = Grid(.05,big_array)
    Shadows = SRSE_Grid.get_all_shadows((6,6))
    list_of_shadows = Shadows.compute_separate_shadows()

    # with mapped_png_context("Test_Shadow_Tracking_Images/nothing_representation.png",((0,0),(10,10)),(1000,1000)) as context:
    #         for shadow in list_of_shadows:
    #                 print(f"This is my label: {shadow.label}")
    #                 if shadow.label == True:
    #                     context.set_source_rgb(1,0,0)
    #                 else:
    #                       context.set_source_rgb(0,1,0)
    #                 shadow.draw(context)
    #         context.set_source_rgb(0,0,0)
    #         SRSE_Grid.draw(context)
    return list_of_shadows


def label_status(previous_grid, current_grid):
      for shadow in current_grid:
            shadow.label = False
            for old_shadow in previous_grid:
                  temp_array = shadow.occupancy_array + old_shadow.occupancy_array
                  if np.max(temp_array) == 2 and old_shadow.label == True:
                        shadow.label = True
                        break
      
def draw_list_of_shadows(imagename,list_of_shadows):
    with mapped_png_context(f"Test_Shadow_Tracking_Images/{imagename}.png",((0,0),(10,10)),(1000,1000)) as context:
        for shadow in list_of_shadows:
                print(f"This is my label: {shadow.label}")
                if shadow.label == True:
                    context.set_source_rgb(1,0,0)
                else:
                        context.set_source_rgb(0,1,0)
                shadow.draw(context)

def create_cup_grid():
        image = cv2.imread('cup_piece.png',0)
        print("'image' data type: ",image.dtype)
        image = image/255
        image = image.astype(np.float32)
        print(image.dtype)
        load_to_all_binary(image)
        image_grid = Grid(0.035,image)
        print("claculated aabb = ", image_grid.calc_aabb())
        return image_grid

def load_to_all_binary(array):
      shape = array.shape
      for i in range(shape[0]):
            for j in range(shape[1]):
                  if array[i,j] >0.07: array[i,j] = 1

def appear_dis_example_cup_env():
    cup_grid = create_cup_grid()
    print(cup_grid.calc_aabb)
    first_position = cup_grid.get_all_shadows((3,5))
    list_first = first_position.compute_separate_shadows()
    list_first[1].label = True
    list_first[0].label = True
    draw_list_of_shadows("cup_first_position",list_first)
    second_position = cup_grid.get_all_shadows((5,5))
    list_second = second_position.compute_separate_shadows()
    label_status(list_first,list_second)
    draw_list_of_shadows("cup_second_position",list_second)
    third_position = cup_grid.get_all_shadows((8,5))
    list_third = third_position.compute_separate_shadows()
    label_status(list_second,list_third)
    draw_list_of_shadows("cup_third_position",list_third)
    
def main():
    # keyframe_nondiscrete_shadows = generate_keyframe_grid()
    # nothing_shadows = generate_nothing_grid()
    # label_status(keyframe_nondiscrete_shadows, nothing_shadows)
    # draw_list_of_shadows("keyframe_representation",keyframe_nondiscrete_shadows)

    # cup_grid = create_cup_grid()

    # ## Human-readable cup

    # print(cup_grid.calc_aabb)
    # first_position = cup_grid.get_all_shadows((3,5))
    # list_first = first_position.compute_separate_shadows()
    # list_first[1].label = True
    # list_first[0].label = True
    # draw_list_of_shadows("cup_first_position",list_first)
    # second_position = cup_grid.get_all_shadows((5,5))
    # list_second = second_position.compute_separate_shadows()
    # label_status(list_first,list_second)
    # draw_list_of_shadows("cup_second_position",list_second)
    # third_position = cup_grid.get_all_shadows((8,5))
    # list_third = third_position.compute_separate_shadows()
    # label_status(list_second,list_third)
    # draw_list_of_shadows("cup_third_position",list_third)

    # test_array = np.array([[0,0,0,0,1],
    #                        [0,0,0,0,0],
    #                        [0,1,0,0,0],
    #                        [0,0,0,0,0],
    #                        [0,0,0,0,0]],dtype=np.float64)
    # small_grid = Grid(1,test_array)
    # print(small_grid.occupancy_array)
    # small_grid2 = small_grid.get_all_shadows((1,0))
    # print(small_grid2.occupancy_array)
    # print("\n")
    # print((small_grid.occupancy_array + small_grid2.occupancy_array))
    # draw_list_of_shadows("small_array_test",[small_grid])
    # draw_list_of_shadows("small_array_test2",[small_grid2])
    pass

main()