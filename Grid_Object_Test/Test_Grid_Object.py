from Grid import Grid
import numpy as np
import math

"""
This file demonstrates a numpy array and resolution value being used to initialize a Grid object

"""
gold_master = np.array([[0,1,0,1,0],
                        [1,0,1,0,1],
                        [0,1,0,1,0],
                        [1,0,1,0,1],
                        [0,1,0,1,0]],dtype=np.float32)

nx,ny = 225,225
largescale_array = np.zeros((nx,ny))
wx = nx//10 + 1
wy = ny//10 + 1
largescale_array[int(.3*nx):int(.3*nx)+wx,int(.1*ny):int(.1*ny)+wy] = 1 
largescale_array[int(.1*nx):int(.1*nx)+wx,int(.5*ny):int(.5*ny)+wy] = 1 
largescale_array[int(.6*nx):int(.6*nx)+wx,int(.6*ny):int(.6*ny)+wy] = 1


def human_readable_grid_construction():
    """
    Tests the Grid object initialization with a human readable numpy array 
    and a resolution of 1. Verifies that the array passed in matches the 
    array stored in the Grid object instance.
    """
    sample_grid = Grid(1,gold_master)
    print(sample_grid.string_information(1))
    if np.array_equal(sample_grid.occupancy_array,gold_master):
        print("\nInput array matches instance array: Pass")
    else:
        print("\nSomething went wrong: Fail")

def largescale_grid_construction():
    """
    Tests the Grid object initialization with a large-scale numpy array 
    and a resolution of 1. Verifies that the array passed in matches 
    the array stored in the Grid object instance.
    """
    large_grid = Grid(1,largescale_array)
    print(large_grid.string_information())
    if np.array_equal(large_grid.occupancy_array,largescale_array):
        print("\nInput array matches instance array: Pass")
    else:
        print("\nSomething went wrong: Fail")


if __name__ == "__main__":
    print("\n")
    print(gold_master,"\n\nGold master array for reference in test 1")
    print(f"\n{'-'*110}")
    print('Testing for human readable array in a Grid object instance\nExpected result is a grid instance with a 5 by 5 shape, resolution of 1, grid match gold master')
    human_readable_grid_construction()
    print(f"\n{'-'*110}")
    print("testing largescale array\nExpected result: 225 by 225 grid with a resolution of 1")
    largescale_grid_construction()