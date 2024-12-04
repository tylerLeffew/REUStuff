import cairo
import math
import contextlib
from Grid import Grid
import Test_Shadow_Tracking
import numpy as np



"""
This file demonstrates a numpy array and resolution value being used to initialize a Grid object.
"""


def flip_arrayX(array):
    new_array = np.copy(array)
    for i in range(array.shape[0]):
        new_array[i] = array[((array.shape[0]-1)-i)]

def matrix_to_stretch_rectangle(user_aabb, device_aabb):
    """ Return a Cairo transformation matrix that maps the given user
    rectangle into the given device rectangle, both given as (lower left,
    upper right).  Strecthes as needed."""

    xx = (device_aabb[1][0] - device_aabb[0][0]) / (user_aabb[1][0] - user_aabb[0][0])
    x0 = device_aabb[0][0] - xx*user_aabb[0][0]

    yy = ((device_aabb[1][1] - device_aabb[0][1]) / (user_aabb[1][1] - user_aabb[0][1]))
    y0 = device_aabb[0][1] - yy*user_aabb[0][1]
    
    print("xx = ", xx , " x0 = ", x0, " yy = ", yy, " y0 = ", y0)
    matrix = cairo.Matrix(xx=xx, yx=0, xy=0, yy=yy, x0=x0, y0=y0)
    
    return matrix

def matrix_to_fit_rectangle(user_aabb, device_aabb, padding=0.1):
    """Return a matrix that fits the given user rectangle, as large as
    possible, within the given device rectangle.  Does not stretch.  Preserves
    aspect ratio and centers if there's slack."""

    c = user_aabb[1][0] - user_aabb[0][0]  # user width
    d = user_aabb[1][1] - user_aabb[0][1]  # user height

    pad = max(c,d) * padding

    user_aabb = ((user_aabb[0][0]-pad, user_aabb[0][1]-pad),(user_aabb[1][0]+pad,user_aabb[1][1]+pad))

    c = user_aabb[1][0] - user_aabb[0][0]  # user width, padded
    d = user_aabb[1][1] - user_aabb[0][1]  # user height, padded

    b = device_aabb[1][0] - device_aabb[0][0]  # device width
    a = device_aabb[1][1] - device_aabb[0][1]  # device height

    if -a/d >= b/c:
        m = -b/c
        extra = (a - m*d)/m
        real_user_aabb = ((user_aabb[0][0], user_aabb[0][1]-extra/2),(user_aabb[1][0], user_aabb[1][1]+extra/2))
    else:
        m = -a/d;
        extra = (b - m*c)/m;
        real_user_aabb = ((user_aabb[0][0]-extra/2, user_aabb[0][1]),(user_aabb[1][0]+extra/2, user_aabb[1][1]))

    print("real_user_aabb = ",real_user_aabb)
    print("device aabb = ",device_aabb)

    return matrix_to_stretch_rectangle(real_user_aabb, device_aabb)

@contextlib.contextmanager
def mapped_png_context(fullpath, user_aabb, svg_size):
    with cairo.SVGSurface("/dev/null", svg_size[0], svg_size[1]) as surface:
        device_aabb = ((0, svg_size[1]), (svg_size[0], 0))
        context = cairo.Context(surface)
        context.set_matrix(matrix_to_fit_rectangle(user_aabb, device_aabb, padding=0))
        yield context
        surface.write_to_png(fullpath)

def internet_thing():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200, 200)
    ctx = cairo.Context(surface)

    # Set initial color
    ctx.set_source_rgb(1, 0, 0)

    # Draw a rectangle
    ctx.rectangle(10, 10, 80, 80)
    ctx.fill()

    # Create a transformation matrix
    matrix = cairo.Matrix()
    matrix.translate(100, 100)  
    matrix.rotate(math.pi / 4)
    matrix.scale(0.5, 0.5)

    # Apply the matrix
    ctx.transform(matrix)

    # Set a different color
    ctx.set_source_rgb(0, 0, 1)

    # Draw another rectangle
    ctx.rectangle(10, 10, 80, 80)
    ctx.fill()

    surface.write_to_png("transformed_rectangles.png")

def main():
    print("check1")
    grid = Test_Shadow_Tracking.create_cup_grid()
    flip_arrayX(grid.occupancy_array)
    print(np.max(grid.occupancy_array))
    print("check2")
    with mapped_png_context("test_context_man2.png",((0,0),(10,10)),(1000,1000)) as context:
        context.set_source_rgb(1,1,0)
        grid.draw(context)
main()