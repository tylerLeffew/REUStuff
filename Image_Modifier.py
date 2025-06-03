import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class ImageModifier:
    def __init__(self, path = None):
        self.saved_threshold = 0
        self.working_array = None
        if path is None:
            self.file_path = self._choose_image()
        else:
            self.file_path = path
    
    def show_array_simple(self, title="Array Display", cmap='gray'):
        input_copy = np.copy(self.working_array)
        input_copy = input_copy[::-1]
        plt.figure(figsize=(6, 6))
        plt.imshow(input_copy, cmap=cmap, interpolation='nearest', origin='lower')
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    def _choose_image(self):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename()
        return file_path
    
    def _thresh_and_show(self, filepath):
        threshold = 0.5
        thresh = None
        initial_thresh = 0.5
        image = cv2.imread(filepath, 0)
        image = image / 255
        ret, thresh = cv2.threshold(image, 0.8, 1, cv2.THRESH_BINARY)

        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.35)
        im = ax.imshow(image, interpolation='nearest')
        ax.set_title("Use slider to adjust threshold")
        ax.grid(False)

        ax_slider = plt.axes([0.25, 0.2, 0.5, 0.03])
        threshold_slider = Slider(ax_slider, 'Threshold', 0.0, 1.0, valinit=initial_thresh)

        ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
        invert_button = Button(ax_button, 'Invert Bits')

        def update(val):
            nonlocal threshold
            nonlocal thresh
            threshold = threshold_slider.val
            ret, thresh = cv2.threshold(image, threshold, 1, cv2.THRESH_BINARY)
            im.set_data(thresh)
            fig.canvas.draw_idle()

        def invert(event):
            nonlocal thresh
            nonlocal image
            if image is not None:
                image = 1 - image
                im.set_data(thresh)
                fig.canvas.draw_idle()

        threshold_slider.on_changed(update)
        invert_button.on_clicked(invert)

        plt.show()
        self.saved_threshold = threshold
        self.working_array = thresh
        return thresh
    
    def _iterate_blocks(self,array, block_size):
        h, w = array.shape
        if h % block_size != 0 or w % block_size != 0:
            raise ValueError("Array dimensions must be divisible by block size")

        for row in range(0, h, block_size):
            for col in range(0, w, block_size):
                block = array[row:row + block_size, col:col + block_size]
                yield (row, col), block

    def _gridify_image(self, input_array, cell_size):
        full_size = input_array.shape[0]
        if input_array is None:
            raise ValueError("input array is None")

        if input_array.shape[0] != input_array.shape[1]:
            raise ValueError("input array is not square")
        
        height, width = input_array.shape
        if height % cell_size != 0 or width % cell_size != 0:
            raise ValueError("image dimensions must be divisible by cell_size")
        
        num_cells = full_size // cell_size
        grid = np.zeros((num_cells, num_cells))

        for (row, col), block in self._iterate_blocks(input_array, cell_size):
            if np.any(block == 1): 
                grid[row // cell_size, col // cell_size] = 1

        self.working_array = grid
        return grid
    def dynamic_threshold(self):
        threshed = self._thresh_and_show(self.file_path)
        return threshed
    
    def project_image(self, cell_size):
        grid = self._gridify_image(self.working_array, cell_size)
        return grid
    
    def write_image(self, filepath):
        print(self.working_array.dtype)
        self.working_array = self.working_array.astype(np.uint8)
        self.working_array = self.working_array * 255 
        cv2.imwrite(filepath, self.working_array)
        self.working_array = self.working_array / 255
        self.working_array = self.working_array.astype(np.float64)
        
