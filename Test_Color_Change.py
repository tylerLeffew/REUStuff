import json
from Grid import Grid
import cv2
import numpy as np
from context_tools import mapped_png_context

def get_color_list():
    with open("colors.json", "r") as file:
        data = json.load(file)
        color_tuples = {key: tuple(value) for key, value in data["colors"].items()}
        return color_tuples

def main():
    image = cv2.imread("weird_shapes.jpeg",0)
    

    np.info(image)

    cv2.imshow("hellO",image)
    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(0)

    # closing all open windows
    cv2.destroyAllWindows()

    test_grid = Grid(image,resolution=.5)
    cv2.imshow("hello",test_grid.occupancy_array)
    cv2.waitKey(0)

    # closing all open windows
    cv2.destroyAllWindows()
    colors = get_color_list()
    print(colors["red"])
    with mapped_png_context("testcolor.png",((0,0),(10,10)),(1000,1000)) as context:
        test_grid.draw(context,colors["red"])


    
if __name__=="__main__":
    main()


