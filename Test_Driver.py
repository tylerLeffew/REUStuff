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
       context.set_source_rgb(0, 0, 1)
       context.arc(position[0],position[1],(.25),0,2*math.pi)
       context.fill()

def represent_simple_environment():
       with mapped_png_context("Images/simple_environment.png",((0,0),(10,10)),(1000,1000)) as context:
              RSE_Grid = Grid(.05,big_array)
              context.set_source_rgb(0,0,0)
              RSE_Grid.draw(context)
              add_robot((5,5),context)

def draw_shadows_on_simple_env():
       with mapped_png_context("Images/simple_shadow_environment.png",((0,0),(10,10)),(1000,1000)) as context:
              SRSE_Grid = Grid(.05,big_array)
              Shadows = SRSE_Grid.get_all_shadows((5,5))
              context.set_source_rgb(1,0,0)
              Shadows.draw(context)
              context.set_source_rgb(0,0,0)
              SRSE_Grid.draw(context)
              add_robot((5,5),context)

def separate_discrete_shadows():
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
              file_name = f"{name}{i+1:04d}.png"
              list_of_grid_objects = ENV_Grid.get_movement_shadows(first_path[0],first_path[1])
              with mapped_png_context(file_name,((0,0),(10,10)),(1000,1000)) as context:
                     print(file_name)

def make_folder_stack():
       path = './Images/Video/VideoFrames'
       if not os.path.exists(path):
              print("\nCreating folder directory for images\n")
              os.makedirs(path)
       else:
              print("\nFolder directory for images already exists\n")
              
def main():
       make_folder_stack()
       moving_shadows_discrete()
main()