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

# Function 1: Perform Delaunay Triangulation
def compute_delaunay_triangulation(vertices):
    """
    Computes the Delaunay triangulation for a set of vertices.
    Returns the triangles formed by the triangulation.
    """
    # Define the boundary segments (closing the polygon)
    boundary = np.column_stack((vertices, np.roll(vertices, -1, axis=0)))
    
    # Triangle input format
    input_dict = {'vertices': vertices, 'segments': boundary}
    output_dict = triangle.triangulate(input_dict, 'p')  # 'p' means to produce a standard Delaunay triangulation
    
    return output_dict['triangles']

# Function 2: Calculate Circumcenter of a Triangle
def circumcenter(A, B, C):
    """
    Computes the circumcenter of a triangle given its three vertices.
    The circumcenter is the center of the circumscribed circle around the triangle.
    """
    D = 2 * (A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]))
    
    Ux = ((A[0]**2 + A[1]**2) * (B[1] - C[1]) +
          (B[0]**2 + B[1]**2) * (C[1] - A[1]) +
          (C[0]**2 + C[1]**2) * (A[1] - B[1])) / D
    
    Uy = ((A[0]**2 + A[1]**2) * (C[0] - B[0]) +
          (B[0]**2 + B[1]**2) * (A[0] - C[0]) +
          (C[0]**2 + C[1]**2) * (B[0] - A[0])) / D
    
    return np.array([Ux, Uy])

# Function 3: Compute Circumcenters and Radii for Delaunay Triangles
def compute_circumcenters_and_radii(triangles, vertices):
    """
    Given a set of triangles (by vertex indices) and the original vertices,
    compute the circumcenter and the radius for each triangle.
    """
    circumcenters = []
    radii = []
    
    for triangle_indices in triangles:
        # Get the vertices for each triangle
        A = vertices[triangle_indices[0]]
        B = vertices[triangle_indices[1]]
        C = vertices[triangle_indices[2]]
        
        # Calculate circumcenter
        center = circumcenter(A, B, C)
        circumcenters.append(center)
        
        # Calculate radius (distance from circumcenter to any vertex)
        radius = np.linalg.norm(center - A)
        radii.append(radius)
    
    return np.array(circumcenters), np.array(radii)

# Function 4: Find the Circumcenter with the Largest Radius
def find_center_of_fattest_part(circumcenters, radii):
    """
    Given the circumcenters and their corresponding radii,
    find the circumcenter with the largest radius (the fattest part of the polygon).
    """
    # Find the index of the largest radius
    ind = np.argmax(radii)
    return circumcenters[ind]

# Main Function: Given Vertices, Compute the Center of the Fattest Part of a Non-Convex Shape
def compute_center_of_non_convex_shape(vertices):
    """
    Given the vertices of a non-convex polygon, compute the center of the fattest part (largest circumcenter).
    This will calculate Delaunay triangulation, circumcenters, and find the one with the largest radius.
    """
    # Step 1: Compute the Delaunay triangulation
    triangles = compute_delaunay_triangulation(vertices)
    
    # Step 2: Compute the circumcenters and their radii
    circumcenters, radii = compute_circumcenters_and_radii(triangles, vertices)
    
    # Step 3: Find the center with the largest radius
    center = find_center_of_fattest_part(circumcenters, radii)
    
    return center


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