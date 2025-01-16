import Grid
import numpy as np
import cv2, math, random


def read_image(filename):
    image = cv2.imread(filename,0)
    print(np.info(image))
    ret , thresh = cv2.threshold(image,127,1,cv2.THRESH_BINARY_INV)
    for i in range(image.shape[0]):
        print(thresh[i])
    print(ret)

if __name__ == "__main__":
    read_image("object_envs/5x5_checkerboard.png")


#Test_Shadow_Tracking_Images/test.png