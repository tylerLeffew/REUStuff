import Grid, cv2, math
import numpy as np
import cairo

"""
This reads an image using cv2 and toggles the bits, prints both to show cv2 reading and the toggle function.

 - gold_master image is 5x5 pixels in checkerboard pattern, first row is white black white black white

"""

float_array = np.array([[11,255,12,190,15],
                        [240,4,255,24,200],
                        [3,220,22,230,20],
                        [210,20,230,6,225],
                        [19,230,0,190,3]],dtype=np.float32)

gold_master = np.array([[0,1,0,1,0],
                        [1,0,1,0,1],
                        [0,1,0,1,0],
                        [1,0,1,0,1],
                        [0,1,0,1,0]],dtype=np.float32)

gold_master_invert = np.array([
                        [1,0,1,0,1],
                        [0,1,0,1,0],
                        [1,0,1,0,1],
                        [0,1,0,1,0],
                        [1,0,1,0,1]],dtype=np.float32)

def toggle_bits(orig):
    return 1 - orig

def load_to_all_binary(array, threshold = 0.1):
    shape = array.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if array[i,j] > threshold: 
                array[i,j] = 1
            else:
                array[i,j] = 0




def test_perfect_image_cv2():
    """
    Test loading a perfect image using OpenCV and verify its correctness.

    This function reads a 5x5 checkerboard image in grayscale, normalizes it to
    a binary form using floor division, and checks if the resulting array matches
    the expected inverted gold master pattern. Prints the loaded array and a message
    indicating whether the loaded image matches the expected pattern.
    """
    image_test = cv2.imread("5x5_checkerboard.png",0)
    image_test = np.floor(image_test/255)
    print(f"original form cv2 :\n{image_test}\n")

    if np.array_equal(image_test, gold_master_invert):
        print("The image loaded as expected")
    else:
        print("Something went wrong :(")
    
def test_np_floor():
    """
    Test loading a fuzzy image using numpy's floor division and verify its correctness.

    This function reads a 5x5 grayscale image, normalizes it to a binary form using numpy's floor division,
    and checks if the resulting array matches the expected gold master pattern. Prints the loaded array
    and a message indicating whether the loaded image matches the expected pattern.
    """
    threshold = .10
    new_instance = np.copy(float_array/255)
    load_to_all_binary(new_instance, threshold)
    print(f"original:\n{float_array}\n")
    print(f"new after np_floor (threshold={threshold*255}):\n{new_instance}\n")

    if np.array_equal(new_instance, gold_master):
        print("The image loaded as expected")
    else:
        print("Something went wrong :(")

def test_toggle_bits_cv2():
    """
    Test toggling bits of a checkerboard image using OpenCV.

    This function reads a 5x5 checkerboard image in grayscale, normalizes it to
    a binary form using floor division, toggles its bits, and checks if the
    resulting array matches the expected gold master pattern. Prints the original
    and toggled arrays along with a message indicating whether the toggled image
    matches the expected pattern.
    """
    image_test = cv2.imread("5x5_checkerboard.png",0)
    image_test = np.floor(image_test/255)
    print(f"original form cv2 :\n{image_test}\n")
    image_test2 = toggle_bits(image_test)
    print(f"toggled image: \n{image_test2}")

    if np.array_equal(image_test2, gold_master):
        print("The image loaded as expected")
    else:
        print("Something went wrong :(")

if __name__ == "__main__":
    print(f"-------------------")
    print("Running Test for reading a perfect image:")
    test_perfect_image_cv2()

    print(f"-------------------")
    print("Running Test for a fuzzy image:")
    test_np_floor()

    print(f"-------------------")
    print("Running Test for toggling bits (white = 0, black = 1):")
    test_toggle_bits_cv2()

