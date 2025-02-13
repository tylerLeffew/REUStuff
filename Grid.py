import numpy as np
import math, random

class Grid:
    robot_size = .15
    label = False #False = clear : True = contaminated : default status is clear

    def __init__(self,occupancy_array,resolution=1):
        self.resolution = resolution
        self.occupancy_array = occupancy_array
        self.copy_of_original_grid = np.copy(occupancy_array)
    
    def print_grid(self):
        print(self.occupancy_array)



    def compute_separate_shadows(self):
        shadow_begin_point = []
        list_of_grids_out = []
        shape = self.occupancy_array.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                if self.occupancy_array[i][j] == 1:
                    print("shadow cell found at", i, j)
                    grid_to_add_to_list = self.find_shadow_from(i,j)
                    list_of_grids_out.append(grid_to_add_to_list)
        return list_of_grids_out

    """This method is used in conjunction with compute_separate_shadows().
        When given an initial index, BFS search is done to find all points touching that
        are also occupied """           
    def find_shadow_from(self,start_i,start_j): 
        array_out = np.zeros((self.occupancy_array.shape))
        Q = [(start_i,start_j)]
        while len(Q) > 0:
            i,j = Q.pop()
            array_out[i,j] = 1
            self.occupancy_array[i,j] = 0
            neighbors = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
            for i2,j2 in neighbors:
                if i2<0: continue
                if j2<0: continue
                if i2>= self.occupancy_array.shape[0]: continue
                if j2>= self.occupancy_array.shape[1]: continue
                if self.occupancy_array[i2,j2] == 0: continue
                Q.append((i2,j2))
        grid_object_out = Grid(self.resolution,array_out)
        return grid_object_out
        
    """ This method calculates the user unit bounding box using the resolution provided
        and the size of the array to create a proportional bounding box for mapped_svg/png_context()"""
    def calc_aabb(self):
        self.temp_x = self.occupancy_array.shape[1] * self.resolution
        self.temp_y = self.occupancy_array.shape[0] * self.resolution
        return ((0,0),(self.temp_x,self.temp_y))
    
    """This method draws a square at a given xy of == size to the resolution"""
    def make_square(self,x,y,context):
        context.rectangle(x,y,self.resolution,self.resolution)
        context.fill()
        context.stroke_preserve()

    """This method draws a blue circle at a given xy"""
    def add_robot(self,position_xy,context):
       context.set_line_width(4)
       context.set_source_rgba(0, 0, 255, 1)
       context.arc(position_xy[0],position_xy[1],(self.robot_size),0,2*math.pi)
       context.fill()
       context.stroke_preserve()





    
    """This method draws the occupancy grid of the Grid instance to a given cairo context"""
    def draw(self,context,color=None):
        color_tuple = color
        print("dis the color ",color_tuple)
        if color_tuple:
            context.set_source_rgb(color_tuple[0],color_tuple[1],color_tuple[2])
        position_y = 0
        shape = self.occupancy_array.shape
        for i in range(shape[0]):
            position_x = 0
            for j in range(shape[1]):
                if self.occupancy_array[i,j] == 1:
                    self.make_square(position_x,position_y,context)
                position_x+=self.resolution
            position_y+=self.resolution

    """This method uses a neighborhood search calculate areas of the occupancy array given two vectors """
    def visibility_within_cone(self,grid, u_direction, v_direction):
        u = np.asarray(u_direction, dtype=int)
        v = np.asarray(v_direction, dtype=int)
        origin = np.array([0,0], dtype=int)
        dims = np.asarray(grid.shape, dtype=int)
        m = 0
        k = 0
        position = np.array([0,0], dtype=int)
        while np.all(position < dims):
            while np.all(position < dims):
                if not np.all(position == 0):
                    pos = tuple(position)
                    pos_minus_u = tuple(np.maximum(origin, position - u))
                    pos_minus_v = tuple(np.maximum(origin, position - v))
                    grid[pos] *= (m*grid[pos_minus_u] + 
                              k*grid[pos_minus_v]) / (m + k)
                k += 1
                position += v
            m += 1
            k = 0
            position = m*u
            grid[:] = (grid >= 0.5)

    """This method converts a given coordinate point from human units to the nearest array index
        using the resolution"""
    def find_index_position(self, point_xy):
        x_index = int(point_xy[0]/self.resolution)
        y_index = int(point_xy[1]/self.resolution)
        point_out = [x_index,y_index]
        print("conversion from unit point to index: ",point_out)
        return point_out


    """
    This method takes in a point in human units, and slices the given array current_grid
    from the position of the point, and then applies the visibility within cone algorithm 
    to the slice. The algorithm is applied in each of the four directions (up, right, down, 
    left) and in the four diagonal directions. The result is stored in the slice of the array.""" 
    def slice_visibility_array_from_index(self, indexes, current_grid):
   
    
        unit_to_index = self.find_index_position(indexes)

        x0 = unit_to_index[1]
        y0 = unit_to_index[0]

        self.visibility_within_cone(current_grid[x0:, y0:], [2,1], [1,0])
        self.visibility_within_cone(current_grid[x0:, y0:], [2,1], [1,1])
        self.visibility_within_cone(current_grid[x0:, y0:], [1,2], [1,1])
        self.visibility_within_cone(current_grid[x0:, y0:], [1,2], [0,1])

        self.visibility_within_cone(current_grid[x0::-1, y0:], [2,1], [1,0])
        self.visibility_within_cone(current_grid[x0::-1, y0:], [2,1], [1,1])
        self.visibility_within_cone(current_grid[x0::-1, y0:], [1,2], [1,1])
        self.visibility_within_cone(current_grid[x0::-1, y0:], [1,2], [0,1])

        self.visibility_within_cone(current_grid[x0::-1, y0::-1], [2,1], [1,0])
        self.visibility_within_cone(current_grid[x0::-1, y0::-1], [2,1], [1,1])
        self.visibility_within_cone(current_grid[x0::-1, y0::-1], [1,2], [1,1])
        self.visibility_within_cone(current_grid[x0::-1, y0::-1], [1,2], [0,1])

        self.visibility_within_cone(current_grid[x0:, y0::-1], [2,1], [1,0])
        self.visibility_within_cone(current_grid[x0:, y0::-1], [2,1], [1,1])
        self.visibility_within_cone(current_grid[x0:, y0::-1], [1,2], [1,1])
        self.visibility_within_cone(current_grid[x0:, y0::-1], [1,2], [0,1])

    """This method returns a list of equidistant points along a straight line given the to and from points """
    def points_along_line(self, from_x, to_x, from_y, to_y):
        distance = math.sqrt(math.pow((to_x-from_x),2)+math.pow((to_y-from_y),2))
        point_amount = int(distance/.2)
        print(point_amount," files about to be created")
        list_x = np.linspace(from_x,to_x,point_amount)
        list_y = np.linspace(from_y,to_y,point_amount)
        list_out = list(zip(list_x,list_y))
        print("calculated points = "+str(list_out))
        return list_out
    
    """This method flips all the points in self.occupancy_grid"""
    def switch_points(self):
        shape = self.occupancy_array.shape
        for i in range(shape[0]):                                                                               # <------------- Redundant method find better -----------------
            for j in range(shape[1]):
                self.occupancy_array[i,j] = 1-self.occupancy_array[i,j] 

    """This method is given an index on the occupancy grid in meters and calculates
        all cells that are nonvisible and returns them all non-discretely in a new
        grid instance"""
    def get_all_shadows(self,pursuer_position): # pursuer position given in meters
        self.switch_points()
        array_out = np.copy(self.occupancy_array)
        self.slice_visibility_array_from_index(pursuer_position,array_out)
        grid_out = Grid(self.resolution,array_out)
        grid_out.switch_points()
        self.switch_points()
        grid_out.occupancy_array = grid_out.occupancy_array - self.occupancy_array
        return grid_out

    """This method is given a two points in meters, calculates a list of equidistant points along a line
        from the beginning point to the end point. It then calculates a new grid instance at each point
        with nonvisible regions. It compiles and returns the list of grids"""    
    def get_movement_shadows(self,from_point,to_point): # points are given in meters
        list_of_points = self.points_along_line(from_point[0],to_point[0],from_point[1],to_point[1])
        list_of_grids_out = []
        for i in range(len(list_of_points)):
            print("Using point "+ str(list_of_points[i]) + " to calculate temp grid obj in get_movement_shadows")
            temp_grid_object = self.get_all_shadows(list_of_points[i])
            print("movement shadows of grid",i+1," calculated.")
            list_of_grids_out.append(temp_grid_object)
        return list_of_grids_out
    
    """This method checks if two occupancy grids overlap and returns true 
        if they do and false if they don't"""
    def overlaps(self,comparison_grid):
        return np.any(self.occupancy_array, comparison_grid.occupancy_array)
    
    """basically __str__()"""
    def string_information(self,array_print = False):
        if array_print == True:
            return f"\nGrid shape: {self.occupancy_array.shape}\nResolution of Grid: {self.resolution}\n\nGrid:\n{self.occupancy_array}\n"
        else:
            return f"\nGrid shape: {self.occupancy_array.shape}\nResolution of Grid: {self.resolution}"

    


