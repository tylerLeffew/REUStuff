import numpy as np
import math
class Raycaster:

    class Stop(Exception): pass

    class Ray:
        TERMINUS_AT_TARGET = 0
        TERMINUS_AT_EDGE = 1
        PASS_THRU_TARGET = 2
        TERMINUS_WITHIN_BOUNDS = 3
        def __init__(self, array, origin, terminus, type):
            self.array = array
            self.origin = origin
            self.terminus = terminus
            self.type = type
            self.angle = self.find_angle()

        def find_angle(self):
            adj_term = (self.terminus[1], self.array.shape[1] - self.terminus[1])
            adj_origin = (self.origin[1], self.array.shape[1] - self.origin[1])
            offset = (adj_term[0] - adj_origin[0], adj_term[1] - adj_origin[1])
            angle = math.atan2(offset[1], offset[0])
            return angle

    def __init__(self, array):
        self.master_array = array # just the environment
        self.working_array = np.copy(array) # contains the rays as they are shot in the environment
        self.ray_dict = {} # dictionary that holds individual rays (no environments) with keys representing their source coordinates
        self.coordinate_list = []

    def custom_sort(self, list):
        for i,ray in enumerate(list):
            
            

    def is_within_4_connected_neighbors(self, candidate_coord, center_coord):
        """
        Check if candidate_coord is within the 4-connected neighbors of center_coord.
        
        4-connected neighbors include cells directly above, below, left, or right
        of the center cell, but not diagonal cells or the center itself.

        Args:
            candidate_coord (tuple): (x, y) of the candidate cell.
            center_coord (tuple): (x, y) of the center cell.

        Returns:
            bool: True if candidate_coord is within the 4-connected neighbors, False otherwise.
        """
        x_candidate, y_candidate = candidate_coord
        x_center, y_center = center_coord

        return (
            (x_candidate == x_center and abs(y_candidate - y_center) == 1) or
            (y_candidate == y_center and abs(x_candidate - x_center) == 1)
        )
    def visit2(self,x, y):
        try:
            self.working_array[x][y] = 1
        except IndexError:
            pass
    def point_in_triangle(self,p, a, b, c):
        # Barycentric coordinate method
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - \
                (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        d1 = sign(p, a, b)
        d2 = sign(p, b, c)
        d3 = sign(p, c, a)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def iterate_triangle(self, origin, point1, point2, visit):
        x_coords = [origin[0], point1[0], point2[0]]
        y_coords = [origin[1], point1[1], point2[1]]

        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if self.point_in_triangle((x, y), origin, point1, point2):
                    visit(x, y)


                
    def add_rays_except_key(self, exclude_key, array):
        for key, list_of_individual_rays in self.ray_dict.items():
            if exclude_key in self.ray_dict: 
                if key == exclude_key: continue
            for ray in list_of_individual_rays:
                array += ray
        return array
      
    def visit(self, x, y, array, ray_only_array):
        if x == self.current_target[0] and y == self.current_target[1]:
            self.hit_target = True
        if array[x][y] == 1 and x != self.current_target[0] and y != self.current_target[1]: 
            raise self.Stop("Collision")
        if x <= 0 or x >= array.shape[0] or y <= 0 or y >= array.shape[1]: 
            raise self.Stop("Out of bounds")
        array[x][y] = 1
        ray_only_array[x][y] = 1
        self.current_coordinate = (x, y)


    def _raytrace(self, x0, y0, x1, y1, visit, stop_on_intersection=True):
        self.current_target = (x1, y1)
        self.hit_target = False
        key = (x0,y0)
        ray_list = []
        working_temporary_array = np.copy(self.master_array)
        single_ray = np.zeros(self.master_array.shape)
        if key in self.ray_dict: 
            ray_list = self.ray_dict[key]
        else:
            self.ray_dict[key] = ray_list
        if stop_on_intersection: working_temporary_array = self.add_rays_except_key(key, working_temporary_array)
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x = x0
        y = y0
        n = 100000 + dx + dy
        x_inc = 1 if x1 > x0 else -1
        y_inc = 1 if y1 > y0 else -1
        error = dx - dy
        dx *= 2
        dy *= 2
        self.current_coordinate = ()
        try:
            for i in range(n):
                visit(x, y, working_temporary_array, single_ray)  # visit may raise a Stop
                if error > 0:
                    x += x_inc
                    error -= dy
                else:
                    y += y_inc
                    error += dx  
        except self.Stop as e:
            print("Stop stop",e, x, y, self.current_coordinate)
        except IndexError as e:
            print("IndexError stop",e, x, y, self.current_coordinate)
        finally:
            if self.hit_target:
                if self.is_within_4_connected_neighbors(self.current_coordinate, self.current_target):
                    print('----Appending Ray type: TERMINUS_AT_TARGET----\n')
                    ray_list.append(self.Ray(single_ray, key, self.current_target, self.Ray.TERMINUS_AT_TARGET))
                elif ((0,self.master_array.shape[0]-1) in self.current_coordinate[0]) or ((0,self.master_array.shape[1]-1) in self.current_coordinate[1]):
                    print('----Appending Ray type: PASS_THRU_TARGET and TERMINUS_AT_EDGE----\n')
                    ray_list.append(self.Ray(single_ray, key, self.current_target, self.Ray.PASS_THRU_TARGET))
                    ray_list.append(self.Ray(single_ray, key, self.current_coordinate, self.Ray.TERMINUS_AT_EDGE))
                else:
                    print('----Appending Ray type: PASS_THRU_TARGET and TERMINUS_WITHIN_BOUNDS----\n')
                    ray_list.append(self.Ray(single_ray, key, self.current_target, self.Ray.PASS_THRU_TARGET))
                    ray_list.append(self.Ray(single_ray, key, self.current_coordinate, self.Ray.TERMINUS_WITHIN_BOUNDS))
                print("--------------here----------------")
                self.working_array += single_ray
                self.ray_dict[key] = ray_list

            else:
                print("No path found to target")



    def raycast(self, x0, y0, x1, y1, stop_on_intersection=True):
        self._raytrace(x0, y0, x1, y1, self.visit, stop_on_intersection)
    
    def fill_visibility_cone(self, origin):
        for i in range(len(self.coordinate_list)):
            if i >= 1:
                pass
            if i == len(self.coordinate_list) - 1:
                self.iterate_triangle(origin, self.coordinate_list[i], self.coordinate_list[0], self.visit2)
            else:
                self.iterate_triangle(origin, self.coordinate_list[i], self.coordinate_list[i+1], self.visit2)
            