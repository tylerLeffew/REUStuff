import cv2,math
import numpy as np
from Grid import Grid
from context_tools import mapped_png_context, vflip_font
import matplotlib.pyplot as plt
import color_loader as colors



def show_array(array):
    plt.imshow(array, cmap='gray')
    plt.axis('off')
    plt.show()

def add_robot(position, context):
    
    """
    Draws a blue circle representing a robot at the given position in the given context
    
    Parameters:
    position (tuple of two floats): The x and y coordinates of the position of the robot
    context (cairo.Context): The context in which to draw the robot
    """
    context.set_source_rgb(0, 0, 1)
    context.arc(position[0],position[1],(1.5),0,2*math.pi)
    context.fill()

def label_status(previous_grid, current_grid):
    for shadow in current_grid:
        shadow.label = False
        for old_shadow in previous_grid:
                temp_array = shadow.occupancy_array + old_shadow.occupancy_array
                if np.max(temp_array) == 2 and old_shadow.label == True:
                    shadow.label = True
                    break
    

image = cv2.imread("Images/object_envs/9roomgrid50.png",0)
image = image/255
image = 1- image
ret, thresh = cv2.threshold(image,.4,1,cv2.THRESH_BINARY)
cv2.imshow("image",thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(thresh.dtype)
grid = Grid(thresh,.1)
list_of_points = [(62.9,13.8),(17.5,13.8),(17.5,51.9),(17.5,35.9),(62.1,35.9),(44.3,35.9),(44.3,50.7),(62.1,58.6)] # points to visit

master_grid = Grid(thresh,.1)
path_1, list_of_points1 = master_grid.get_movement_shadows(list_of_points[0],list_of_points[1])
path_2, list_of_points2 = master_grid.get_movement_shadows(list_of_points[1],list_of_points[2])    
# path_3 = master_grid.get_movement_shadows(list_of_points[2],list_of_points[3])    
# path_4 = master_grid.get_movement_shadows(list_of_points[3],list_of_points[4])    
# path_5 = master_grid.get_movement_shadows(list_of_points[4],list_of_points[5])    
# path_6 = master_grid.get_movement_shadows(list_of_points[5],list_of_points[6])    
# path_7 = master_grid.get_movement_shadows(list_of_points[6],list_of_points[7])

list_of_paths = [path_1,path_2]#path_3,path_4,path_5,path_6,path_7]
list_of_points = [list_of_points1,list_of_points2]
first_flag = 0
i = 1
x = 1
color_list = colors.get_color_list()
path1_discreet = []
master_list = [] # this is the compilation of all the paths when broken down into discrete grids: list of lists

def gen_single_path():
    for grid in path_1:
        grids = grid.compute_separate_shadows()
        if first_flag == 0:
            first_flag = 1
            for grid in grids:
                grid.label = True
                print("initialized first set with contaminated shadows")
        path1_discreet.append(grids)              

    for k in range(len(path1_discreet)):
        name = f"Images/Room_test/path{i}.png"
        print(name)
        print(thresh.shape[1],thresh.shape[0])
        print(master_grid.calc_aabb())
        with mapped_png_context(name,master_grid.calc_aabb(),svg_size=(883,714)) as context:
            print("past mapped_png_context")
            if k != 0:
                label_status(path1_discreet[k-1],path1_discreet[k])
            for y in range(len(path1_discreet[k])):
                if path1_discreet[k][y].label == True:
                    path1_discreet[k][y].draw(context,color_list["red"])
                else:
                    path1_discreet[k][y].draw(context,color_list["green"])
                master_grid.draw(context,color_list["black"])
                add_robot(list_of_points1[k],context)

            i += 1
            print("---------- end of mapped_png_context")
        x += 1
        print("----------made it through k = ",k)
        if k == 5:
            exit()

def gen_all_paths():
    for list in list_of_paths:
        path_list = []
        discrete_grid_list = []
        for grid in list:
            grids = grid.compute_separate_shadows()
            discrete_grid_list.append(grids)
        path_list.append(discrete_grid_list)
        discrete_grid_list = []
    master_list.append(path_list)
    path_list = []
    
    for grid in master_list[0][0][0]:
        grid.label = True
        print("initialized first set with contaminated shadows")
    
    for k in range(len(master_list)):
        for l in range(len(master_list[k])):
            name = f"Images/Room_test/path{k+1}-{l+1}.png"
            if l == 0 and k != 0:
                label_status(master_list[k-1][len(master_list[k-1])-1],master_list[k][l])
            elif k == 0 and l == 0:
                with mapped_png_context(name,master_grid.calc_aabb(),svg_size=(883,714)) as context:
                    print("past mapped_png_context")
                    for y in range(len(master_list[k][l])):
                        print(master_list[k][l][y])
                        if master_list[k][l][y].label == True:
                            master_list[k][l][y].draw(context,color_list["red"])
                        else:
                            master_list[k][l][y].draw(context,color_list["green"])
                        master_grid.draw(context,color_list["black"])
                        add_robot(list_of_points[k][l],context)
            else:
                label_status(master_list[k][l-1],master_list[k][l])
                with mapped_png_context(name,master_grid.calc_aabb(),svg_size=(883,714)) as context:
                    print("past mapped_png_context")
                    for y in range(len(master_list[k][l])):
                        if master_list[k][l][y].label == True:
                            master_list[k][l][y].draw(context,color_list["red"])
                        else:
                            master_list[k][l][y].draw(context,color_list["green"])
                        master_grid.draw(context,color_list["black"])
                        add_robot(list_of_points[k][l],context)
                print("---------- end of mapped_png_context")


        
def main():
    gen_all_paths()

if __name__ == "__main__":
    main()
            

