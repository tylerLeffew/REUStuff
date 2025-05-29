from Grid import Grid
from context_tools import mapped_png_context
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import tkinter as tk
from tkinter import filedialog
import time
import threading, queue

def choose_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename()
    return file_path



def thresh_and_show(filepath):
    threshold = 0.5
    thresh = None
    initial_thresh = 0.5
    image = cv2.imread(filepath,0)
    image = image/255
    image = 1- image
    # image = image[::-1]
    ret, thresh = cv2.threshold(image,.4,1,cv2.THRESH_BINARY)

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25) 
    
    im = ax.imshow(thresh, interpolation='nearest')
    ax.set_title("Use slider to adjust threshold")
    ax.grid(True)
    # ax.invert_yaxis()

    ax_slider = plt.axes([0.25, 0.1, 0.5, 0.03])  # [left, bottom, width, height]
    threshold_slider = Slider(ax_slider, 'Threshold', 0.0, 1.0, valinit=initial_thresh)


    def update(val):
        nonlocal threshold 
        nonlocal thresh
        threshold = threshold_slider.val
        ret, thresh = cv2.threshold(image,threshold,1,cv2.THRESH_BINARY)
        im.set_data(thresh)
        fig.canvas.draw_idle()
        print(threshold)

    threshold_slider.on_changed(update)
    print("check 1")
    plt.show()
    print("check 2")
    return threshold, thresh

def show_interactive_environment(input_array, resolution=0.1):
    fig, ax = plt.subplots()
    im = ax.imshow(input_array, cmap='gray', interpolation='nearest')
    ax.set_title("Click on a cell to get (row, col)")

    result_q = queue.Queue()

    def timer_callback():
        if not result_q.empty():
            show_grid = result_q.get()
            im.set_data(show_grid.occupancy_array)
            ax.set_title("Updated Occupancy Grid")
            fig.canvas.draw_idle()
            # with mapped_png_context("test_dynamic.png",user_aabb=show_grid.calc_aabb(),svg_size=(1000,1000)) as context:
            #     print("drawing")
            #     show_grid.draw(context)

    def foo(grid_object, position):
        show_grid = grid_object.get_all_shadows(position)
        print(position)
        # with mapped_png_context("test_dynamic_foo_master.png",user_aabb=show_grid.calc_aabb(),svg_size=(1000,1000)) as context:
        #         print("drawing foo master")
        #         grid_object.draw(context)
        # print(show_grid.calc_aabb())
        # with mapped_png_context("test_dynamic_foo.png",user_aabb=show_grid.calc_aabb(),svg_size=(1000,1000)) as context:
        #         print("drawing foo")
        #         show_grid.draw(context)
        print("created grid")
        result_q.put(show_grid)

    def on_click(event):
        if event.inaxes != ax:
            return
        col = int(event.xdata)
        row = int(event.ydata)
        print(input_array.shape)
        user_unit_points = [(col * resolution), (((input_array.shape[0] - row) * resolution))]
        master_grid = Grid(input_array, resolution)
        print(user_unit_points)
        threading.Thread(target=foo, args=(master_grid, user_unit_points), daemon=True).start()

    fig.canvas.mpl_connect('button_press_event', on_click)
    timer = fig.canvas.new_timer(interval=100)
    timer.add_callback(timer_callback)
    timer.start()

    plt.show()      



def main():
    file_path = choose_file()
    # show image with thresh slider (user confirm)
    threshold, threshed = thresh_and_show(file_path)
    print(threshold)
    # have image displayed wait for user click
    show_interactive_environment(threshed)
    # when user clicks, create sim view and overlay to graph
    # upon new click, clear and overlay

if __name__ == "__main__":
    main()
