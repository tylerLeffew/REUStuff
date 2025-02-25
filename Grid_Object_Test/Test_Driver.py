from Grid import Grid
from context_tools import *
import cairo, clip, cv2, random, os
import numpy as np

# This is the example driver for the Grid object class

# There will be multiple methods to demo individual parts of the Grid object class

nx,ny = 225,225
big_array = np.zeros((nx,ny))
wx = nx//10 + 1
wy = ny//10 + 1
big_array[int(.3*nx):int(.3*nx)+wx,int(.1*ny):int(.1*ny)+wy] = 1 
big_array[int(.1*nx):int(.1*nx)+wx,int(.5*ny):int(.5*ny)+wy] = 1 
big_array[int(.6*nx):int(.6*nx)+wx,int(.6*ny):int(.6*ny)+wy] = 1

# ^^This is the main array that will serve as the object environment

def add_robot(position, context):
       
       """
       Draws a blue circle representing a robot at the given position in the given context
       
       Parameters:
       position (tuple of two floats): The x and y coordinates of the position of the robot
       context (cairo.Context): The context in which to draw the robot
       """
       context.set_source_rgb(0, 0, 1)
       context.arc(position[0],position[1],(.25),0,2*math.pi)
       context.fill()

def represent_simple_environment():
       """
       Represents a simple environment using a grid and draws it to a PNG file.

       This function creates a grid object using a predefined occupancy array
       to represent an environment. It then draws this environment into a PNG
       file with the help of a mapped PNG context. Additionally, it draws a 
       robot at a fixed position within this environment.

       The resulting image will be saved as 'simple_environment.png'."""

       with mapped_png_context("Images/simple_environment.png",((0,0),(10,10)),(1000,1000)) as context:
              RSE_Grid = Grid(.05,big_array)
              context.set_source_rgb(0,0,0)
              RSE_Grid.draw(context)
              add_robot((5,5),context)

def draw_shadows_on_simple_env():
       """
       Represents a simple environment using a grid and draws it to a PNG file.
       Additionally, it draws the shadows of a robot at a fixed position within this
       environment.

       The resulting image will be saved as 'simple_shadow_environment.png'.
       """
       with mapped_png_context("Images/simple_shadow_environment.png",((0,0),(10,10)),(1000,1000)) as context:
              SRSE_Grid = Grid(.05,big_array)
              Shadows = SRSE_Grid.get_all_shadows((5,5))
              context.set_source_rgb(1,0,0)
              Shadows.draw(context)
              context.set_source_rgb(0,0,0)
              SRSE_Grid.draw(context)
              add_robot((5,5),context)

def separate_discrete_shadows():
       """
       Represents a simple environment using a grid and draws it to a PNG file.
       Additionally, it draws the shadows of a robot at a fixed position within this
       environment, and then separates and draws these shadows discretely.

       The resulting image will be saved as 'discrete_shadows.png'.
       """
       with mapped_png_context("Images/discrete_shadows.png",((0,0),(10,10)),(1000,1000)) as context:
              SRSE_Grid = Grid(.05,big_array)
              Shadows = SRSE_Grid.get_all_shadows((5,5))
              Shadows.occupancy_array = Shadows.occupancy_array - SRSE_Grid.occupancy_array
              list_of_shadows = Shadows.compute_separate_shadows()
              for shadow in list_of_shadows:
                     context.set_source_rgb(random.random(),random.random(),.1)
                     shadow.draw(context)
              context.set_source_rgb(0,0,0)
              SRSE_Grid.draw(context)
              add_robot((5,5),context)

def moving_shadows_discrete(): #### Work in progress
       ENV_Grid = Grid(.05,big_array)
       first_path = ((5,4),(1,9))
       second_path = ((1,9),(8,9))
       list_of_paths = [first_path,second_path]
       name = "Images/Video/VideoFrames/discrete_shadows"
       for i in range (len(list_of_paths)):
              current_path = list_of_paths[i]
              list_of_shadowlists = []
              list_of_grid_objects = ENV_Grid.get_movement_shadows(current_path[0],current_path[1])
              print("current path = "+ str(current_path[0]) + " to " + str(current_path[1]))
              for grid in list_of_grid_objects:
                     grid.occupancy_array = grid.occupancy_array - ENV_Grid.occupancy_array
                     shadow_list = grid.compute_separate_shadows()
                     list_of_shadowlists.append(shadow_list)
              for j in range(len(list_of_shadowlists)):       
                     file_name = f"{name + str(i)}{j+1:04d}.png"
                     current_shadowlist = list_of_shadowlists[j]
                     with mapped_png_context(file_name,((0,0),(10,10)),(1000,1000)) as context:
                            print(file_name + " being created")
                            for shadow in current_shadowlist:
                                   context.set_source_rgb(random.random(),random.random(),random.random())
                                   shadow.draw(context)
                            context.set_source_rgb(0,0,0)
                            ENV_Grid.draw(context)

def compile_video():
       """
       Compile a video from a folder of PNG images in the Images/Video/VideoFrames
       folder. The video is saved as Images/Video/test_video.mp4 with a frame rate
       of 30.
       """
       print("\nAttempting to compile video\n")
       vid = clip.image_glob('Images/Video/VideoFrames/*.png', frame_rate=30)
       vid = clip.background(vid,(255,255,255))
       clip.save_mp4(vid,"Images/Video/test_video.mp4",30)

def make_folder_stack():
       """
       Ensures that the directory structure for storing video frames exists.

       This function checks whether a specific directory path exists for storing
       video frames. If the directory does not exist, it creates the directory
       and prints a message indicating the creation. If the directory already
       exists, it prints a message indicating that the directory is already
       present.
       """
       path = './Images/Video/VideoFrames'
       if not os.path.exists(path):
              print("\nCreating folder directory for images\n")
              os.makedirs(path)
       else:
              print("\nFolder directory for images already exists\n")
              
def main():
       make_folder_stack()
       # moving_shadows_discrete()
       compile_video()
main()