from Image_Modifier import ImageModifier
import numpy as np
import Raycaster as rc
import Array_Toolkit as atk
if __name__ == "__main__":
    array = np.zeros((100, 100))
    array[(array.shape[0]//2)-10:(array.shape[0]//2)+10, (array.shape[1]//2)-10:(array.shape[1]//2)+5] = 1
    ray = rc.Raycaster(array)
    ray.raycast(10,10,35,90)
    ray.raycast(10,10,11,11)
    ray.raycast(10,10,13,11)
    ray.raycast(90,90,89,90)
    ray.raycast(90,90,90,89, stop_on_intersection=True)
    ray.raycast(90,90,88,87)
    atk.write_array_to_image(array=ray.working_array, filepath="raytrace2.png")