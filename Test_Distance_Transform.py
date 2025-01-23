import Grid
import numpy as np
import cv2, math, random


def read_image(filename):
    image = cv2.imread(filename,0)
    print(np.info(image))
    ret , thresh = cv2.threshold(image,50,255,cv2.THRESH_BINARY_INV)
    for i in range(image.shape[0]):
        print(thresh[i])
    print(ret)
    thresh_inv = cv2.bitwise_not(thresh)
    cv2.imshow("thresh", thresh)
    cv2.imshow("thresh_inv", thresh_inv)
    cv2.waitKey(0)
    # cv2.imshow("thresh_inv", thresh_inv)
    cv2.destroyAllWindows()
    # exit()
    
    distance = cv2.distanceTransform(thresh_inv, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    cv2.imshow("distance", distance)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    _, max_val, _, centre = cv2.minMaxLoc(distance)
    circle = cv2.circle(img =image,center= centre, radius = int(max_val), color=(0, 255, 0), lineType=2,thickness=2)
    cv2.imshow("OG with circle", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(centre)
    exit()



if __name__ == "__main__":
    # read_image("object_envs/cup_piece.png")
    # read_image("Test_Shadow_Tracking_Images/test.png")
    # read_image("Test_Label_Images/simple_centroid.png")
    # read_image("Test_Shadow_Tracking_Images/test_small_corner.png")
    read_image("Test_Shadow_Tracking_Images/cup_second_position.png")


#Test_Shadow_Tracking_Images/test.png
#object_envs/5x5_checkerboard.png