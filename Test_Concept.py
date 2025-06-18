from Image_Modifier import ImageModifier
import numpy as np
import Raycaster2 as rc
import Array_Toolkit as atk
import math
if __name__ == "__main__":
    array = np.zeros((100, 100))
    # array[(array.shape[0]//2)-10:(array.shape[0]//2)+20, (array.shape[1]//2)-10:(array.shape[1]//2)+5] = 1
    ray = rc.Raycaster(array)

    x, y = 50, 50
    theta = 0             # Facing right (0 radians)
    sa = math.pi          # 180° field of view
    resolution = 9        # 9 evenly spaced rays

    targets = ray.get_ray_endpoints(x, y, theta, sa, resolution)

    
    atk.write_array_to_image(array=ray.working_array, filepath="raytrace3.png")