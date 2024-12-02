import numpy as np
import cv2
from Grid import Grid
import cairo
import time
from context_tools import mapped_svg_context

small_array = np.array([[1,1,0,0,0],
                        [1,0,0,0,1],
                        [0,0,0,0,0],
                        [0,1,0,0,0],
                        [0,0,1,0,1],
                        [0,0,0,1,1]])

gold_master = np.array([[0,1,0,1,0],
                        [1,0,1,0,1],
                        [0,1,0,1,0],
                        [1,0,1,0,1],
                        [0,1,0,1,0]],dtype=np.float32)

grid1 = Grid(1,gold_master)

def flip_arrayX(array):
    new_array = np.copy(array)
    for i in range(array.shape[0]):
        new_array[i] = array[((array.shape[0]-1)-i)]
    print("old")
    print(array)
    print("new")
    print(new_array)



if __name__ == '__main__':
    with mapped_svg_context('movingtest.svg',grid1.calc_aabb(),(100,100)) as context:
        context.set_source_rgb(1,1,0)
        grid1.draw(context)