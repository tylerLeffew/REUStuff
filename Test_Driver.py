from Grid import Grid
from context_tools import *
import cairo, clip, cv2
import numpy as np

# This is the test driver for the Grid object class

# There will be multiple methods to demo individual parts of the Grid object class

nx,ny = 225
big_array = np.zeros((nx,ny))
wx = nx//10 + 1
wy = ny//10 + 1
big_array[int(.3*nx):int(.3*nx)+wx,int(.1*ny):int(.1*ny)+wy] = 1 
big_array[int(.1*nx):int(.1*nx)+wx,int(.5*ny):int(.5*ny)+wy] = 1 
big_array[int(.6*nx):int(.6*nx)+wx,int(.6*ny):int(.6*ny)+wy] = 1

big_grid = Grid(.05,big_array) # This is the main Grid object that is demonstrated by the methods in this file

def add_robot(position, context):
       context.set_source_rgba(0, 0, 255, 1)
       context.arc(position[0],position[1],(.25),0,2*math.pi)
       context.fill()






