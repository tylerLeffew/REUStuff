import numpy as np
from Grid import Grid
from context_tools import *
import cairo, clip, cv2, random, os
import time
import triangle

def load_to_all_binary(array):
      shape = array.shape
      for i in range(shape[0]):
            for j in range(shape[1]):
                  if array[i,j] >0.07: array[i,j] = 1
                  else: array[i,j] = 0

def index_to_unit(resolution,index):
     print(index)
     x_point = (index[0]*resolution)
     y_point = (index[1]*resolution)
     return [x_point,y_point]

def draw_vis_point(point,context,color = 0):
    context.set_source_rgb(0, color, 1)
    context.arc(point[0],point[1],(.3),0,2*math.pi)
    context.fill()
    
def centroid(vertices):
    x, y = 0, 0
    n = len(vertices)
    signed_area = 0
    for i in range(len(vertices)):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % n]
        # shoelace formula
        area = (x0 * y1) - (x1 * y0)
        signed_area += area
        x += (x0 + x1) * area
        y += (y0 + y1) * area
    signed_area *= 0.5
    x /= 6 * signed_area
    y /= 6 * signed_area
    out = [x,y]
    return out

  

if __name__ == '__main__':                
    time1 = time.time()
    image_array = cv2.imread('object_envs/cup_piece.png',0)
    ret,thresh = cv2.threshold(image_array,100,1,cv2.THRESH_BINARY)
    image_env = thresh.astype(np.float64)
    print(np.info(thresh))

    contours,heir = cv2.findContours(thresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(contours)
    print('length of contours ',len(contours[0]))
    list_of_contours = []
    for i in range(len(contours[0])):
      list_of_contours.append(contours[0][i][0])
    grid1 = Grid(.1,image_env)


    print(f"These are the verticies: {list_of_contours}\n")
    # Convert the list of numpy arrays to a 2D numpy array (Nx2)
    vertices = np.array(list_of_contours)
    
    # Compute the center of the fattest part of the shape
    center = compute_center_of_non_convex_shape(vertices)

    print(f"This is the center: {center}\n")





#     print(grid1.calc_aabb())
#     print(grid1.occupancy_array.shape)
#     print(np.info(grid1.occupancy_array))
#     print(np.max(grid1.occupancy_array))
#     center_point = centroid(list_of_contours)
#     center_point = index_to_unit(grid1.resolution,center_point)
    center = index_to_unit(grid1.resolution,center)
    with mapped_png_context('Test_Label_Images/simple_centroid4.png',grid1.calc_aabb(),(1000,1000)) as context:
         context.set_source_rgb(1,0,1)
         grid1.draw(context)
         for i in range(len(list_of_contours)):
              point = index_to_unit(grid1.resolution,list_of_contours[i])
              print('index to unit = ',point)
              draw_vis_point(point,context)
         draw_vis_point(center,context=context,color=1)
            
          
    




























    print(center_point)
    print('\n\n',time.time()-time1," seconds")