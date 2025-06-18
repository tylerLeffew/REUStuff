import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import cv2
import Array_Toolkit as atk

def unpack_contours(contours):
    unpacked_contours = []
    for i in range(len(contours[0])):
        unpacked_contours.append(contours[0][i][0])
    print(unpacked_contours)
    return unpacked_contours

# Create the base array
array = np.zeros((100, 100))
array[20:60, 20:80] = 1
array[70:95, 20:40] = 1
array[75:85, 45:65] = 1
array[65:98, 70:90] = 1

  # So  1me shape to visualize

array = array.astype(np.uint8)
cont , heir = cv2.findContours(array, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

print(cont)
cont2 = unpack_contours(cont)
# Coordinates where you want to place the circles
circle_cells = [(25, 25), (30, 70), (45, 50), (65, 35)]

# Plotting
fig, ax = plt.subplots()
ax.imshow(array, cmap='gray', origin='upper' ) # 'origin=lower' so (0,0) is bottom-left
radius = 2
# Overlay circles 
for (y, x) in cont2:  # (row, col) → (y, x)
    circ = Circle((y, x), radius=radius, edgecolor='red', facecolor='none', linewidth=2)
    ax.add_patch(circ)
    array[x][y] = 0
    radius += 1

# Optional: adjust gridlines or axis if needed
ax.set_xlim(0, array.shape[1])
ax.set_ylim(0, array.shape[0])
ax.set_aspect('equal')
plt.title("Overlay Circles on Grid")
plt.axis('off')
print(len(cont[0]))
print(cont[0][0][0])
print(cont2[0])
atk.write_array_to_image(array=array, filepath="cont_test1.png")
plt.show()

