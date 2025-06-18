import numpy as np
class Raycaster:

    class Stop(Exception): pass

    def __init__(self, array):
        self.master_array = array # just the environment
        self.working_array = np.copy(array) # contains the rays as they are shot in the environment
        self.ray_dict = {} # dictionary that holds individual rays (no environments) with keys representing their source coordinates

    def add_rays_except_key(self, exclude_key, array):
        for key, list_of_individual_rays in self.ray_dict.items():
            if exclude_key in self.ray_dict: 
                if key == exclude_key: continue
            for ray in list_of_individual_rays:
                array += ray
        return array
    
        
    def visit(self, x, y, array, ray_only_array):
        if array[x][y] == 1: raise self.Stop("Collision")
        if x < 0 or x >= array.shape[0] or y < 0 or y >= array.shape[1]: raise self.Stop("Out of bounds")
        array[x][y] = 1
        ray_only_array[x][y] = 1

    def _raytrace(self, x0, y0, x1, y1, visit, stop_on_intersection=True):
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
            pass
        except IndexError as e:
            pass
        finally:
            if key in self.ray_dict:
                ray_list.append(single_ray)
                self.ray_dict[key] = ray_list
            else:
                self.ray_dict[key] = [single_ray]
            self.working_array += single_ray

    def raycast(self, x0, y0, x1, y1, stop_on_intersection=True):
        self._raytrace(x0, y0, x1, y1, self.visit, stop_on_intersection)