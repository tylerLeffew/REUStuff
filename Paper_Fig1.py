from Grid import Grid
import numpy as np 
import matplotlib.pyplot as plt
import cv2 , math

def iterate_blocks(array, block_size):
    h, w = array.shape
    if h % block_size != 0 or w % block_size != 0:
        raise ValueError("Array dimensions must be divisible by block size")

    for row in range(0, h, block_size):
        for col in range(0, w, block_size):
            block = array[row:row + block_size, col:col + block_size]
            yield (row, col), block
            
def show_array_simple(array, title="Array Display", cmap='gray'):
    plt.figure(figsize=(6, 6))
    plt.imshow(array, cmap=cmap, interpolation='nearest', origin='lower')
    plt.title(title)
    plt.colorbar()
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def show_array_with_gridlines(array, tick_spacing=10, cmap='coolwarm', title="Array Display"):
    rows, cols = array.shape
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Display the array
    ax.imshow(array, cmap=cmap, interpolation='nearest', origin='lower',
              vmin=np.min(array), vmax=np.max(array))

    # Set up tick/grid spacing
    ax.set_xticks(np.arange(0, cols + 1, tick_spacing))
    ax.set_yticks(np.arange(0, rows + 1, tick_spacing))
    ax.grid(which='both', color='black', linewidth=0.5)

    # Clean up axes
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.set_title(title)

    plt.tight_layout()
    plt.show()
def show_array(array, cell_size=20, title="Array Display", cmap='gray'):
    rows, cols = array.shape
    width = cols * cell_size
    height = rows * cell_size

    fig, ax = plt.subplots(figsize=(6, 6), facecolor='white')
    ax.set_facecolor('white')

    # Show the array scaled to the cell size
    ax.imshow(array, cmap='coolwarm', interpolation='nearest', extent=[0, width, 0, height], origin='lower', vmin=0, vmax=1)

    # Draw grid lines
    xticks = np.arange(0, width + 1, cell_size)
    yticks = np.arange(0, height + 1, cell_size)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(which='both', color='black', linewidth=0.5)

    # Axis formatting
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal')
    ax.set_title(title)

    # Show
    plt.tight_layout()
    plt.show()
def create_grid_display(cell_size, full_size=1000):
    if 400 % cell_size != 0:
        raise ValueError("cell_size must divide evenly into 400")

    num_cells = full_size // cell_size
    grid = np.zeros((num_cells, num_cells))  # All cells start empty (0)

    fig, ax = plt.subplots(figsize=(6, 6), facecolor='white')
    ax.set_facecolor('white')

    # Show the grid with gray color but white background
    ax.imshow(grid, cmap='Greys', extent=[0, full_size, 0, full_size], origin='lower', vmin=0, vmax=1)

    # Set ticks and black grid lines
    print(np.arange(0, full_size+1, cell_size))
    ax.set_xticks(np.arange(0, full_size+1, cell_size))
    ax.set_yticks(np.arange(0, full_size+1, cell_size))
    ax.grid(which='both', color='black', linewidth=0.5)

    # Format axes
    ax.set_xlim(0, full_size)
    ax.set_ylim(0, full_size)
    ax.set_aspect('equal')
    ax.set_title(f"Grid with cell size {cell_size} pixels ({num_cells}x{num_cells}) cells", fontsize=10)

    # Remove axis numbers
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    
    # show_array(grid)

    plt.show()


def gridify_image(image_path, cell_size, full_size=1000):
    # Load grayscale image without resizing
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = image/255
    image = 1- image
    show_array_simple(image)
    ret, thresh = cv2.threshold(image,.8,1,cv2.THRESH_BINARY_INV)
    show_array_simple(thresh)
    # thresh = 1- thresh
    thresh = thresh[::-1]
    image = image[::-1]
    # show_array(image)
    show_array_with_gridlines(thresh ,tick_spacing= cell_size)
    if image is None:
        raise ValueError("Failed to load image")

    height, width = image.shape
    if height % cell_size != 0 or width % cell_size != 0:
        raise ValueError("Image dimensions must be divisible by cell_size")
    
    num_cells = full_size // cell_size
    grid = np.zeros((num_cells, num_cells))

    vx = 0
    vy = 0

    for (row, col), block in iterate_blocks(thresh, cell_size):
        print(f"Block starting at ({row}, {col}) has shape {block.shape}")
        if np.any(block == 1): 
            vx += 1
            grid[row // cell_size, col // cell_size] = 1
    print(vx)
    show_array(grid)
    # return thresh, grid

def show_all_occupancy_grids(grids, cell_size=20, titles=None, cmap='Greys'):
    count = len(grids)
    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols)

    fig, axs = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4), facecolor='white')
    axs = axs.flatten()

    for i, grid in enumerate(grids):
        ax = axs[i]
        size = grid.shape[0] * cell_size
        extent = [0, size, 0, size]

        ax.set_facecolor('white')
        ax.imshow(grid, cmap=cmap, extent=extent, origin='lower', vmin=0, vmax=1)

        # Draw grid lines
        ticks = np.arange(0, size + 1, cell_size)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.grid(which='both', color='black', linewidth=0.5)

        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect('equal')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_title(titles[i] if titles else f"Grid {i+1}")

    # Turn off any unused subplots
    for j in range(count, len(axs)):
        axs[j].axis('off')

    plt.tight_layout()
    plt.show()
    
def main():
    grid1 = create_grid_display(20)
    grid2, grid3 = gridify_image("Images/Input_Images/square_icra.jpeg", 20)
    grids = [grid1, grid2, grid3]
    show_all_occupancy_grids(grids)


    

if __name__ == "__main__":
    grid = create_grid_display(5)
    gridify_image("Images/Input_Images/rsz_large_udayton2.png", 5)
    # main()