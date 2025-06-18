import numpy as np

class Raycaster():

    class Stop(Exception): pass
    def __init__(self, array):
        self.master_array = array # just the environment
        self.working_array = np.copy(array) # contains the rays as they are shot in the environment
        self.rays_only = np.zeros(array.shape) # contains just rays not the environment
        self.check_bit = 0 # 1 = stop on intersection
        self.ray_dict = {} # dictionary that holds individual rays (no environments) with keys representing their source coordinates

    def remove_rays_from_source(self, key, array):
        if key in self.ray_dict:
            list_of_individual_rays = self.ray_dict[key]
            for ray in list_of_individual_rays:
                array-=ray
        return array
        
    def add_rays_to_source(self, key, array):
        if key in self.ray_dict:
            list_of_individual_rays = self.ray_dict[key]
            for ray in list_of_individual_rays:
                array+=ray
        return array

    def add_rays_except_key(self, exclude_key, array):
        for key, list_of_individual_rays in self.ray_dict.items():
            if key == exclude_key:
                continue
            for ray in list_of_individual_rays:
                print("ray added in add_rays_except_key")
                array += ray
        return array
    def visit(self, x, y, array, ray_only_array):
        if self.check_bit == 1:
            if array[x][y] == 1:
                if self.rays_only[x][y] == 1:
                    raise self.Stop("Collision")
            if x < 0 or x >= array.shape[0] or y < 0 or y >= array.shape[1]:
                raise self.Stop("Out of bounds")
        else:
            if array[x][y] == 1:
                raise self.Stop("Collision")
            if x < 0 or x >= array.shape[0] or y < 0 or y >= array.shape[1]:
                raise self.Stop("Out of bounds")
        array[x][y] = 1
        ray_only_array[x][y] = 1


    def _raytrace(self, x0, y0, x1, y1, visit, array):
        key = (x0,y0)
        ray_list = []
        working_array = np.copy(array)
        if key in self.ray_dict:
            ray_list = self.ray_dict[key]
            print(len(ray_list))
            self.remove_rays_from_source(key, working_array)
            self.add_rays_except_key(key, working_array)
        single_ray = np.zeros(array.shape) 
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x = x0
        y = y0
        n = 1000000 + dx + dy
        x_inc = 1 if x1 > x0 else -1
        y_inc = 1 if y1 > y0 else -1
        error = dx - dy
        dx *= 2
        dy *= 2
        try:
            for i in range(n):
                visit(x, y, working_array, single_ray)
                if error > 0:
                    x += x_inc
                    error -= dy
                else:
                    y += y_inc
                    error += dx
        except self.Stop as e:
            print(e, x, y)
            pass
        except IndexError:
            print("out of bounds stoppage at ",x, y)
            pass
        finally:
            if key in self.ray_dict:
                ray_list.append(single_ray)
                self.ray_dict[key] = ray_list
                self.add_rays_to_source(key, working_array)
                print('mad it')
            else:
                print('mad it 2')
                
                self.ray_dict[key] = [single_ray]
            # self.ray_dict[x0,y0] = single_ray
            self.working_array += working_array
            self.rays_only += working_array - self.master_array
            print(self.ray_dict.keys())

    def raycast(self, x0, y0, x1, y1, stop_on_intersection=False):
        if stop_on_intersection:
            self.check_bit = 1
            self._raytrace(x0, y0, x1, y1, self.visit, self.working_array)
        else:    
            self.check_bit = 0
            self._raytrace(x0, y0, x1, y1, self.visit, self.master_array)
        