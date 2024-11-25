from Grid import Grid
from context_tools import *
import cairo, clip, cv2, random, os
import numpy as np
import time


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
      
def draw_list_of_shadows(image_name,list_of_shadows,original_env,point=[0,0]):
    with mapped_png_context(f"Test_Shadow_Tracking_Images/vid/{image_name}.png",(list_of_shadows[0].calc_aabb()),(1000,1000)) as context:
        for shadow in list_of_shadows:
                print(f"This is my label: {shadow.label}")
                if shadow.label == True:
                    context.set_source_rgb(1,0,0)
                else:
                        context.set_source_rgb(0,1,0)
                shadow.draw(context)
        context.set_source_rgb(0,0,0)
        original_env.draw(context)
        draw_vis_point(point,context)

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
                  else: array[i,j] = 0

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

def draw_vis_point(point,context):
    context.set_source_rgb(0, 0, 1)
    context.arc(point[0],point[1],(.3),0,2*math.pi)
    context.fill()

def build_triangulation(polygon,*, tsettings='qpa1.0', verbose=False):
    def centroid(poly):
        """
        Compute the centroid of a polygon.

        Args:
            poly: A polygon object or a list of vertices where each vertex is a (x, y) point.

        Returns:
            A Point object representing the centroid of the polygon.
        """
        # Get the vertices of the polygon
        pts = np.array([point.to_numpy() for point in poly.vertices])

        # Add the first point at the end to close the polygon
        pts = np.vstack([pts, pts[0]])

        # Compute the signed area of the polygon using the shoelace formula
        x = pts[:, 0]
        y = pts[:, 1]
        area = 0.5 * np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])

        # Compute the centroid using the weighted average formula
        Cx = (1 / (6 * area)) * np.sum((x[:-1] + x[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1]))
        Cy = (1 / (6 * area)) * np.sum((y[:-1] + y[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1]))

        # Return the centroid as a point (you can replace this with your Point object)
        return np.array([Cx, Cy])
    

    def _tri_helper(poly, *, compute_hole=False) -> {'type': tuple[np.ndarray, np.ndarray, []], 'docstring': "Given a polygon boundary, return the pts, segs, and representative hole (if applicable)"}:
        i = np.arange(len(poly)) # How many points
        pts = np.array( [ point.to_numpy() for point in poly.vertices]) # list of points
        seg = np.stack([i, i + 1], axis=1) % len(poly) # A ndarray with shape (N, 2) corresponding to vertex indices of our segments
        if compute_hole:
            cent = centroid(poly)
            return pts, seg, cent.to_numpy()
        else:
            return pts, seg, None

    if verbose:
        print(f"----------------------------------\n\tBuilding Triangulation\n----------------------------------")

    gp_pts = []   # list of np.arrays for  vertices
    gp_seg = []   # list of np.array's for contours (segments0
    gp_holes = [] # holes represented as a point in the hole
    idx = 0 # where does the next contour start
    for p in self.polygons:
        # p should be a polygon_with_holes (meaning an outer boundary and 0 or more holes)
        bpts, bsegs, bhole = _tri_helper(p.outer_boundary())
        gp_pts.append(bpts)
        gp_seg.append(bsegs)
        idx += bsegs.shape[0] # update idx
        for h in p.holes:
            hpts, hsegs, hhole = _tri_helper(h, compute_hole=True)
            gp_pts.append(hpts)
            gp_seg.append(hsegs + idx)
            gp_holes.append(hhole)
            idx += hsegs.shape[0] # update idx

    # Stacks (may not need)
    stack_pts = np.vstack(gp_pts)
    stack_seg = np.vstack(gp_seg)

    if gp_holes:
        stack_holes = np.vstack(gp_holes)
        A = dict(vertices=stack_pts, segments=stack_seg, holes=stack_holes)
    else:
        A = dict(vertices=stack_pts, segments=stack_seg)


    self.triangulation = tr.triangulate(A, tsettings) # this builds the triangulation ... save it

    # extra bookkeeping to grab the triangles and turn it into something we can use
    vlist = self.triangulation['vertices'].tolist()
    tlist = self.triangulation['triangles'].tolist()

    self._triangles = [Triangle2(vlist[t[0]], vlist[t[1]], vlist[t[2]]) for t in tlist]
    # https://stackoverflow.com/questions/46539431/np-random-choice-probabilities-do-not-sum-to-1
    initial_weights = np.asarray([t.area for t in self._triangles]).astype('float64')
    self._tri_weights = initial_weights / np.sum(initial_weights)
      
    
if __name__=='__main__':

    # keyframe_nondiscrete_shadows = generate_keyframe_grid()
    # nothing_shadows = generate_nothing_grid()
    # label_status(keyframe_nondiscrete_shadows, nothing_shadows)
    # draw_list_of_shadows("keyframe_representation",keyframe_nondiscrete_shadows)

    #                        [0,0,0,0,0]],dtype=np.float64)
    # small_grid = Grid(1,test_array)
    # print(small_grid.occupancy_array)
    # small_grid2 = small_grid.get_all_shadows((1,0))
    # print(small_grid2.occupancy_array)
    # print("\n")
    # print((small_grid.occupancy_array + small_grid2.occupancy_array))
    # draw_list_of_shadows("small_array_test",[small_grid])
    # draw_list_of_shadows("small_array_test2",[small_grid2])

    #get the list of lists,set all shadows to contaminated for first list, get list of points for bot, loop draw list comparing current draw list to i-1 then drawing, draw list then bot


    time1 = time.time()
    image_array = cv2.imread('object_envs/splitmerge.png',0)
    image_array=image_array/255
    load_to_all_binary(image_array)
    grid_sm = Grid(.1,image_array)
    # grid_sm2 = grid_sm.get_all_shadows([8.5,18])
    # grid_sm3 = grid_sm.get_all_shadows([8.5,17])
    # list1 = grid_sm3.compute_separate_shadows()
    # list2 = grid_sm2.compute_separate_shadows()
    # list1[1].label = True
    # draw_list_of_shadows("sm_test1",list1, grid_sm,[8.5,17])
    # label_status(list1,list2)
    # draw_list_of_shadows("sm_test2",list2,grid_sm,[8.5,18])

    list_of_non_discreet_grids1 = grid_sm.get_movement_shadows([8.5,17],[8.5,18])
    print("length of list_of_non_discreet_grids1: ",len(list_of_non_discreet_grids1))
    list_of_shadowlists = []
    for grid in list_of_non_discreet_grids1:
                     grid.occupancy_array = grid.occupancy_array - grid_sm.occupancy_array
                     shadow_list = grid.compute_separate_shadows()
                     list_of_shadowlists.append(shadow_list)
    print('length of list of shdowlists: ',len(list_of_shadowlists))
    first_frame_list = list_of_shadowlists[0]
    first_frame_list[2].label = True
    robo_points_list1 = grid_sm.points_along_line(8.5,8.5,17,18)
    name = 'split_merge_moving'

    for i in range(len(list_of_shadowlists)):
         file_name = f"{name}{i+1:04d}.png"
         if i == 0:
               draw_list_of_shadows(file_name,list_of_shadowlists[i],grid_sm,robo_points_list1[i])
         else:
               label_status(list_of_shadowlists[i-1],list_of_shadowlists[i])
               draw_list_of_shadows(file_name,list_of_shadowlists[i],grid_sm,robo_points_list1[i])
    print(f'Time elapsed: {time.time()-time1:.2f} seconds')
    

