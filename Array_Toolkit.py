import cv2
import numpy as np
def write_array_to_image(array, filepath):
        print("hit")
        array = array.astype(np.uint8)
        array = array * 255 
        cv2.imwrite(filepath, array)
        array = array / 255
        array = array.astype(np.float64)