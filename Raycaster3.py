import numpy as np
import math
class Raycaster:

    class Stop(Exception): pass

    def __init__(self, array):
        self.master_array = array # just the environment
        self.working_array = np.copy(array) # contains the rays as they are shot in the environment
        self.ray_dict = {} # dictionary that holds individual rays (no environments) with keys representing their source coordinates
        self.coordinate_list = []
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

    def add_to_sorted_list(self, list, item):
        for i in range(len(list)):
            if list[i][2] >= item[2]:
                list.insert(i, item)
                return
        list.append(item)

    def ordered_coordinate_list(self, key):
        items = self.ray_dict[key]
        list_out = []
        for item in items:
            list_out.append(item[1])
        self.coordinate_list = list_out
        return list_out

                
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
        if x < 0 or x >= array.shape[0] or y < 0 or y >= array.shape[1]: 
            raise self.Stop("Out of bounds")
        array[x][y] = 1
        ray_only_array[x][y] = 1                                                                                                                                                                                                                                                                              

    def _raytrace(self, x0, y0, x1, y1, visit, stop_on_intersection=True):
        self.current_target = (x1, y1)
        self.hit_target = False
        key = (x0,y0)
        ray_list = []
        working_temporary_array = np.copy(self.master_array)
        single_ray = np.zeros(self.master_array.shape)
        if key in self.ray_dict: ray_list = self.ray_dict[key]
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
        current_coordinate = ()
        try:
            for i in range(n):
                current_coordinate = (x, y)
                visit(x, y, working_temporary_array, single_ray)  # visit may raise a Stop
                if error > 0:
                    x += x_inc
                    error -= dy
                else:
                    y += y_inc
                    error += dx
        except self.Stop as e:
            pass
        except IndexError as e:
            pass
        finally:
            if self.hit_target:
                adjusted_coordinate = (current_coordinate[1],self.master_array.shape[0] - current_coordinate[0])
                offset_coordinate = (adjusted_coordinate[0] - x0, adjusted_coordinate[1] - y0)
                angle = math.atan2(offset_coordinate[1], offset_coordinate[0])
                if angle < 0: angle += 2 * math.pi
                if key in self.ray_dict:
                    print("here")
                    self.add_to_sorted_list(ray_list,[single_ray, current_coordinate, angle])
                    self.ray_dict[key] = ray_list
                    list_out = self.ordered_coordinate_list(key)
                    print(list_out)
                    for item in ray_list:
                        print(item[2])
                else:
                    print("there")
                    self.ray_dict[key] = [[single_ray, current_coordinate, angle]]
                self.working_array += single_ray

            else:
                print("No path found to target")

    def get_ray_endpoints(self, x, y, theta, sa, resolution):
        """
        For a given origin (x, y), return `resolution` endpoints at angles
        evenly spaced across `sa` radians centered at `theta`.
        Uses step-wise float marching until ray exits bounds.
        """
        height, width = self.master_array.shape
        endpoints = []

        if resolution < 1:
            raise ValueError("Resolution must be >= 1")

        # Handle resolution = 1 as a special case
        if resolution == 1:
            angles = [theta]
        else:
            start_angle = theta - sa / 2
            angle_step = sa / (resolution - 1)
            angles = [start_angle + i * angle_step for i in range(resolution)]

        for angle in angles:
            dx = math.cos(angle)
            dy = math.sin(angle)

            fx, fy = x + 0.5, y + 0.5  # Start at center of cell for better coverage
            last_valid = (x, y)

            # March forward in small steps until out of bounds
            for _ in range(max(width, height) * 2):  # Safety max steps
                fx += dx * 0.5
                fy += dy * 0.5
                ix, iy = int(fx), int(fy)

                if 0 <= ix < width and 0 <= iy < height:
                    last_valid = (ix, iy)
                else:
                    break

            endpoints.append(last_valid)

        return endpoints


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
            