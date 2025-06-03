import numpy as np
import Array_Toolkit as atk

class Stop(Exception): pass
def visit(x,y,array):
    print(x,y)
    if array[x][y] == 1:
        raise Stop()
    if x < 0 or x >= array.shape[0] or y < 0 or y >= array.shape[1]:
        raise Stop()
    array[x][y] = 1
    

def raytrace(x0, y0, x1, y1, visit, array):
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
            visit(x, y, array)
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
    except Stop:
        pass
    except IndexError:
        pass

if __name__ == "__main__":
    array = np.zeros((100, 100))
    raytrace(10, 10, 12, 11, visit, array)
    atk.write_array_to_image(array=array, filepath="raytrace.png")


