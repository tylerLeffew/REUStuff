import numpy as np
import Array_Toolkit as atk

class Stop(Exception): pass
def visit(x,y,array, count):
    if array[x][y] == 1 and count > 3:
        raise Stop()
    if x < 0 or x >= array.shape[0] or y < 0 or y >= array.shape[1]:
        raise Stop()
    array[x][y] = 1
    
    

def raytrace(x0, y0, x1, y1, visit, array):
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
            visit(x, y, array, i)
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
    except Stop:
        print("collision stopage at ",x, y)
        pass
    except IndexError:
        print("out of bounds stopage at ",x, y)
        pass

if __name__ == "__main__":
    array = np.zeros((100, 100))
    array[(array.shape[0]//2)-10:(array.shape[0]//2)+10, (array.shape[1]//2)-10:(array.shape[1]//2)+5] = 1
    raytrace(x0=10, y0=10, x1=35, y1=90, visit=visit, array=array)
    raytrace(10,10,11,11,visit, array)
    raytrace(10,10,13,11,visit, array)
    raytrace(90,90,89,90,visit, array)
    raytrace(90,90,90,89,visit, array)
    atk.write_array_to_image(array=array, filepath="raytrace.png")


