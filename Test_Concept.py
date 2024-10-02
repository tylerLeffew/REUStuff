import numpy as np
import cv2

small_array = np.array([[1,1,0,0,0],
                        [1,0,0,0,1],
                        [0,0,0,0,0],
                        [0,1,0,0,0],
                        [0,0,1,0,1],
                        [0,0,0,1,1]])

def flip_arrayX(array):
    new_array = np.copy(array)
    for i in range(array.shape[0]):
        new_array[i] = array[((array.shape[0]-1)-i)]
    print("old")
    print(array)
    print("new")
    print(new_array)


flip_arrayX(small_array)