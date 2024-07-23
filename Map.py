import numpy as np
from Grid import Grid
import cairo
import math
from context_tools import *
import random
import clip
import cv2

# find method to scale image cv2.resize
user_aabb = ((0,0),(10,10))
svg_size =  (1000,1000)
resolution = 5

def load_to_all_binary(array):
      shape = array.shape
      for i in range(shape[0]):
            for j in range(shape[1]):
                  if array[i,j] >0.07: array[i,j] = 1      

def outline_of_ones(array):
      shape = array.shape
      for i in range(shape[0]):
            for j in range(shape[1]):
                  if i == 0 or j == 0 or i == shape[0]-1 or j == shape[1]-1:
                        array[i,j] = 1


def points_along_line(from_x, to_x, from_y, to_y):
        distance = math.sqrt(math.pow((to_x-from_x),2)+math.pow((to_y-from_y),2))
        point_amount = int(distance/0.5)
        list_x = np.linspace(from_x,to_x,point_amount)
        list_y = np.linspace(from_y,to_y,point_amount)
        list_out = list(zip(list_x,list_y))
        return list_out


def make_square(x,y,color,context,reso):
        color = 1-color
        context.set_line_width(4)
        context.set_source_rgba(100, 0, 0, color)
        context.rectangle(x,y,reso,reso)
        context.fill()
        context.stroke_preserve()

def add_robot(array,context):
    #    array[0] = array[0]*50
    #    array[1] = 1000 - (array[1]*50)
       context.set_source_rgba(0, 0, 255, 1)
       context.arc(array[0],array[1],(.15),0,2*math.pi)
       context.fill()
       context.stroke_preserve()

def draw( context, robot_position, occupancy_grid,reso):
       position_y = 0
       for i in occupancy_grid:
            position_x=0
            for x in i:
                 make_square(position_x,position_y,x,context,reso)
                # print(x)
                 position_x+=resolution
            position_y+=resolution
       add_robot(robot_position,context,resolution)

def main(): #with resolution 2, 11 squares can fit across
    #  with mapped_svg_context("outfile.svg",user_aabb,svg_size) as context:
        robot_position = np.array([10,5])
        vis_grid = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #after visibility alg
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
                             [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
                             [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                             [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                             [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0]],dtype= np.float32)
        
        occgrid = np.array     ([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #before the one above
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],np.float64)
        
        
        occupancy_grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#building layout example
                                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
                                [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        
        small_array = np.array([[1,1,0,0],
                                [0,0,0,0],
                                [0,0,0,0],
                                [0,0,0,0],
                                [0,0,0,0],
                                [0,0,1,1]])
        nx = 225
        ny = 225

        # Create map
        big_array = np.zeros((nx,ny))
        wx = nx//10 + 1
        wy = ny//10 + 1
        big_array[int(.3*nx):int(.3*nx)+wx,int(.1*ny):int(.1*ny)+wy] = 1 #1 #2
        big_array[int(.1*nx):int(.1*nx)+wx,int(.5*ny):int(.5*ny)+wy] = 1 #1 #3
        big_array[int(.6*nx):int(.6*nx)+wx,int(.6*ny):int(.6*ny)+wy] = 1








        test_array1 = np.zeros((nx,ny))
        test_array1[int(.3*nx):int(.3*nx)+wx,int(.1*ny):int(.1*ny)+wy] = 1
        test_array1[int(.1*nx):int(.1*nx)+wx,int(.5*ny):int(.5*ny)+wy] = 1

        test_array2 = np.zeros((nx,ny))
        test_array2[int(.3*nx):int(.3*nx)+wx,int(.1*ny):int(.1*ny)+wy] = 1

        test_array3 = np.zeros((nx,ny))
        test_array3[int(.1*nx):int(.1*nx)+wx,int(.5*ny):int(.5*ny)+wy] = 1

        test_grid1 = Grid(resolution,test_array1)
        test_grid2 = Grid(resolution,test_array2)
        test_grid3 = Grid(resolution,test_array3)

        # print(test_grid1.overlaps(test_grid2))
        # print(test_grid2.overlaps(test_grid3))


        image = cv2.imread('all_black_environment_resized.png',0)
        print("'image' data type: ",image.dtype)
        image = image/255
        print(image)
        image = image.astype(np.float32)

        print(image.dtype)
        # outline_of_ones(image)
        load_to_all_binary(image)
        image_grid = Grid(0.035,image)
        print("claculated aabb = ", image_grid.calc_aabb())


      #   list_of_grid_objects = image_grid.get_movement_shadows((0.5,0.5),(9,0.5))
      #   list_of_robot_locations = points_along_line(0.5,9,0.5,0.5)
      #   list_of_shadowlists = []
      #   count = 1
      #   for grid in list_of_grid_objects:
      #         grid.occupancy_array = grid.occupancy_array - image_grid.occupancy_array
      #         list_out = grid.compute_separate_shadows()
      #         list_of_shadowlists.append(list_out)
      #   pathname = "test_with_shape"
      #   for i in range(len(list_of_shadowlists)):
      #       file_name = f"{pathname}{i+1:04d}.png"
      #       with mapped_png_context(file_name,image_grid.calc_aabb(),svg_size) as context:
      #             current_list = list_of_shadowlists[i]
      #             print("amount of shadows in current list: ", len(current_list))
      #             color = 1
      #             for shadow in current_list:
      #                   context.set_source_rgb(0.5,0,0)
      #                   shadow.draw(context)
      #                   color = random.random()
      #             add_robot(list_of_robot_locations[i],context)
      #             context.set_source_rgb(0,0,0)
      #             image_grid.draw(context)


        
        # with mapped_png_context("image_test.png",image_grid.calc_aabb(),svg_size) as context:
        #     image_grid.draw(context)
        #     image_grid.add_robot((9,9),context)
        #     image_grid.add_robot((10.5,0),context)
        #     image_grid.add_robot((0,9.1),context)
        #     image_grid.add_robot((0,0),context)
        # print(image_grid.occupancy_array.shape)
        # print(test_grid1.occupancy_array.shape)
               




        



        # draw(context,robot_position,occgrid,resolution)   
        index = np.array([7,9])
        grid1 = Grid(resolution,big_array)
        small_grid = Grid(1,small_array)
        # grid1.slice_visibility_array_from_index(robot_position)
        # grid1.print_grid()
        # outgrid = grid1.get_visibility_grid()
        # draw(context,robot_position,outgrid,resolution)
        # point_from1 = [9,5]
        # point_to1 = [5,5]
        # point_from2 = [5,5]
        # point_to2 = [5,9]
        # grid1.draw1(point_from1,point_to1,"firstpath")
        # grid1.draw1(point_from2,point_to2,"secondpath")




        # list_of_grid_objects = grid1.get_movement_shadows((0.5,0.5),(9,0.5))
        # list_of_robot_locations = points_along_line(0.5,9,0.5,0.5)
        # list_of_shadowlists = []
        # count = 1
        # for grid in list_of_grid_objects:
        #       list_out = grid.compute_separate_shadows()
        #       list_of_shadowlists.append(list_out)
        # pathname = "movementfile4"
        # for i in range(len(list_of_shadowlists)):
        #     file_name = f"{pathname}{i+1:04d}.png"
        #     with mapped_png_context(file_name,user_aabb,svg_size) as context:
        #           current_list = list_of_shadowlists[i]
        #           color = 1
        #           for shadow in current_list:
        #                 context.set_source_rgb(random.random(),random.random(),random.random())
        #                 shadow.draw(context)
        #                 color = random.random()
        #           add_robot(list_of_robot_locations[i],context)
        #           context.set_source_rgb(0,0,0)
        #           grid1.draw(context)


        y = clip.image_glob('*.png', frame_rate=30)
        y = clip.background(y,(255,255,255))
        clip.save_mp4(y,"test_with_shape3.mp4",30)










            # #     # context.set_source_rgb(100,0,0)
            # #     # grid2 = grid1.get_shadow((5,5))
            # #     # grid2.draw(context)
            # #     # context.set_source_rgb(0,0,100)
            # #     # grid1.draw(context)
            #     list1 = grid1.get_movement_shadows((5,5),(5,6))
            #     context.set_source_rgb(100,0,0)
            #     # list1[3].draw(context)
            #     # context.set_source_rgb(0,0,100)
            #     # grid1.draw(context)
            #     grid3 = grid1.compute_separate_shadows()
            #     grid3.draw(context)
                
                # add_robot(index,context)
                # color = 1
                # for shadow in shadow_list:
                #     context.set_source_rgb(color,1-color,color)
                #     shadow.draw(context)
                #     color = random.random()
                #     color = random.random()
                # context.set_source_rgb(0,0,0)
                # grid1.draw(context)

         
        
        
        
         


main()





# def draw ( surface robot_position occupancy_grid  )











# with cairo.SVGSurface("outfile.svg", 700, 700) as surface:
#     context = cairo.Context(surface)
#     # setting color of the context
#     context.set_source_rgba(0, 0, 0, 1)
 
#     # setting of line width
#     context.set_line_width(4)
 
#     # setting of line pattern
#     # context.set_dash([10])
 
#     # move the context to x,y position
#     context.move_to(600, 600)
 
#     # creating a rectangle(square)
#     context.rectangle(100, 100, 100, 100)
 
#     # stroke out the color and width property
#     context.stroke_preserve()
#     context.move_to(10,10)
#     context.rectangle(50, 50, 100, 100)
#     # context.stroke()
#     context.stroke_preserve()
    

    # create class Grid
        # occ grid array 
        # resolution
        # draw method(self, context)
        # visibility
        # aabb method(self) - figure out size 
        # getvisiblecells(self, robo position, reso ) -> array