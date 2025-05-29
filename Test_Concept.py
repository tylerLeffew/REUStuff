import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Dummy data: two binary grids
grid1 = np.random.randint(0, 2, (10, 10))  # Base grid
grid2 = np.random.rand(10, 10)             # Simulated sensor confidence

# Initial threshold to binarize grid2
initial_threshold = 0.5

# Setup plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Make room for slider

# Compute initial overlay
overlay_mask = grid2 > initial_threshold
display = np.zeros((10, 10, 3))
display[grid1 == 1] = [0.7, 0.7, 0.7]      # Base (gray)
display[overlay_mask] = [1.0, 0.0, 0.0]    # Overlay (red)

im = ax.imshow(display, interpolation='nearest')
ax.set_title("Use slider to adjust threshold")
ax.set_xticks(np.arange(10))
ax.set_yticks(np.arange(10))
ax.grid(True)
ax.invert_yaxis()

# Add slider below plot
ax_slider = plt.axes([0.25, 0.1, 0.5, 0.03])  # [left, bottom, width, height]
threshold_slider = Slider(ax_slider, 'Threshold', 0.0, 1.0, valinit=initial_threshold)

# Update function
def update(val):
    threshold = threshold_slider.val
    new_overlay = grid2 > threshold
    new_display = np.zeros((10, 10, 3))
    new_display[grid1 == 1] = [0.7, 0.7, 0.7]
    new_display[new_overlay] = [1.0, 0.0, 0.0]
    im.set_data(new_display)
    fig.canvas.draw_idle()

# Bind slider to update function
threshold_slider.on_changed(update)

plt.show()
