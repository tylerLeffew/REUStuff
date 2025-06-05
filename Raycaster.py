import numpy as np

class Raycaster():

    class Stop(Exception): pass
    def __init__(self, array):
        self.master_array = array
        self.working_array = np.copy(array)
        self.rays_only = np.zeros(array.shape)
        self.check_bit = 0 # 1 = stop on intersection
        
    def visit(self, x, y, array, count):
        if self.check_bit == 1:
            if array[x][y] == 1:
                if self.rays_only[x][y] == 1:
                    raise self.Stop("Collision")
            if x < 0 or x >= array.shape[0] or y < 0 or y >= array.shape[1]:
                raise self.Stop("Out of bounds")
        array[x][y] = 1


    def _raytrace(self, x0, y0, x1, y1, visit, array):
        working_array = np.copy(array)
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
                visit(x, y, working_array,i)
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
            print("out of bounds stopage at ",x, y)
            pass
        finally:
            self.working_array += working_array
            self.rays_only += working_array - self.master_array

    def raycast(self, x0, y0, x1, y1, stop_on_intersection=False):
        if stop_on_intersection:
            self.check_bit = 1
            self._raytrace(x0, y0, x1, y1, self.visit, self.working_array)
        else:    
            self.check_bit = 0
            self._raytrace(x0, y0, x1, y1, self.visit, self.master_array)
        