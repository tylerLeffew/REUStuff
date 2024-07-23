import numpy as np
import math
from context_tools import mapped_svg_context


class Grid:
    robot_size = .15

    def __init__(self,resolution,occupancy_array):
        self.resolution = resolution
        self.occupancy_array = occupancy_array
        self.copy_of_original_grid = np.copy(occupancy_array)
    
    def print_grid(self):
        print(self.occupancy_array)



    def compute_separate_shadows(self):
    # return list of grid objects (1 for each shadow)
        # loop through cells
        # find a cell that is a shadow
        # bfs to find rest of shadow
        # add to list
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

        # return grid
        
    
    

    
    def calc_aabb(self):
        self.temp_x = self.occupancy_array.shape[1] * self.resolution
        self.temp_y = self.occupancy_array.shape[0] * self.resolution
        return ((0,0),(self.temp_x,self.temp_y))
    
    def make_square(self,x,y,context):
        # context.set_line_width(4)
        # context.set_source_rgba(100, 0, 0, opacity)
        context.rectangle(x,y,self.resolution,self.resolution)
        context.fill()
        context.stroke_preserve()

    def add_robot(self,position_xy,context):
       context.set_line_width(4)
       context.set_source_rgba(0, 0, 255, 1)
       context.arc(position_xy[0],position_xy[1],(self.robot_size),0,2*math.pi)
       context.fill()
       context.stroke_preserve()

    def visualize_pursuer_movement(self,from_point,to_point,path_name,svg_size):
        list_of_grids = self.get_movement_shadows(from_point,to_point)
        aabb = self.calc_aabb()
        for i in range(len(list_of_grids)):
            file_name = f"{path_name}{i+1:04d}.svg"
            # below is only visualization
            with mapped_svg_context(file_name,aabb,svg_size) as context:
                self.draw(context,list_of_grids[i])
                print(file_name + " created")



    
    
    def draw(self,context):
        position_y = 0
        shape = self.occupancy_array.shape
        for i in range(shape[0]):
            position_x = 0
            for j in range(shape[1]):
                if self.occupancy_array[i,j] == 1:
                    self.make_square(position_x,position_y,context)
                position_x+=self.resolution
            position_y+=self.resolution


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

    def find_index_position(self, point_xy):
        x_index = int(point_xy[0]/self.resolution)
        y_index = int(point_xy[1]/self.resolution)
        point_out = [x_index,y_index]
        return point_out

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

        # self.occupancy_grid[x0,y0] = 0

    def points_along_line(self, from_x, to_x, from_y, to_y):
        distance = math.sqrt(math.pow((to_x-from_x),2)+math.pow((to_y-from_y),2))
        point_amount = int(distance/0.5)
        print(point_amount," files about to be created")
        list_x = np.linspace(from_x,to_x,point_amount)
        list_y = np.linspace(from_y,to_y,point_amount)
        list_out = list(zip(list_x,list_y))
        return list_out
    
    def switch_points(self):
        shape = self.occupancy_array.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                self.occupancy_array[i,j] = 1-self.occupancy_array[i,j] 

    def get_all_shadows(self,pursuer_position): # pursuer position given in meters
        self.switch_points()
        array_out = np.copy(self.occupancy_array)
        self.slice_visibility_array_from_index(pursuer_position,array_out)
        grid_out = Grid(self.resolution,array_out)
        grid_out.switch_points()
        self.switch_points()
        return grid_out
    
    def get_movement_shadows(self,from_point,to_point): # points are given in meters
        list_of_points = self.points_along_line(from_point[0],to_point[0],from_point[1],to_point[1])
        list_of_grids_out = []
        for i in range(len(list_of_points)):
            temp_grid_object = self.get_all_shadows(list_of_points[i])
            print("movement shadows of grid",i+1," calculated.")
            list_of_grids_out.append(temp_grid_object)
        return list_of_grids_out
    
    def get_array_from_grid_object(self):
        return self.occupancy_array
    
    def overlaps(self,comparison_grid):
        shape = self.occupancy_array.shape
        comparison_grid_array = np.copy(comparison_grid.occupancy_array)
        for i in range(shape[0]):
            for j in range(shape[1]):
                if self.occupancy_array[i,j] >0 and comparison_grid_array[i,j]>0: return True
        return False
    

    


