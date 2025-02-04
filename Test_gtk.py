import json
import cairo
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

# --- Helper Functions --- #

def load_polygon_from_json(file_path):
    """Load polygon data from a JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Extract vertices from JSON
    vertices = [[v["x"], v["y"]] for v in data["vertices"]]
    
    return vertices

# --- GTK4 Setup for Drawing --- #

class PolygonWindow(Gtk.Window):
    def __init__(self, app):
        super().__init__(title="Polygon Visualization", application=app)

        self.set_default_size(800, 600)

        # Load polygon from JSON file
        self.polygon = load_polygon_from_json("L.json")

        # Set up drawing area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_draw_func(self.on_draw)
        self.set_child(self.drawing_area)

    def on_draw(self, drawing_area, cr, width, height):
        """The updated draw function that accepts extra arguments."""
        # Clear the drawing area
        cr.set_source_rgb(1, 1, 1)  # White background
        cr.paint()

        # Adjust the polygon coordinates to center it and zoom
        self.center_and_zoom_polygon(cr, drawing_area)

    def center_and_zoom_polygon(self, cr, drawing_area):
        """Center the polygon in the drawing area with 5% padding."""
        vertices = self.polygon

        # Get the size of the drawing area
        width = drawing_area.get_allocated_width()
        height = drawing_area.get_allocated_height()

        # Calculate the bounding box of the polygon
        min_x = min(vertex[0] for vertex in vertices)
        max_x = max(vertex[0] for vertex in vertices)
        min_y = min(vertex[1] for vertex in vertices)
        max_y = max(vertex[1] for vertex in vertices)

        # Calculate the width and height of the polygon's bounding box
        polygon_width = max_x - min_x
        polygon_height = max_y - min_y

        # Calculate the padding (5% of the drawing area's width/height)
        padding_x = width * 0.05
        padding_y = height * 0.05

        # Calculate the available space for scaling (90% of the drawing area size)
        available_width = width - 2 * padding_x
        available_height = height - 2 * padding_y

        # Calculate the scaling factor for both x and y directions, preserving aspect ratio
        scale_x = available_width / polygon_width
        scale_y = available_height / polygon_height

        # Use the smaller scale factor to maintain the aspect ratio
        scale = min(scale_x, scale_y)

        # Apply translation to move the polygon to the center
        translate_x = (width - available_width) / 2 - min_x * scale
        translate_y = (height - available_height) / 2 - min_y * scale

        # Apply translation first, then scaling
        cr.translate(translate_x, translate_y)
        cr.scale(scale, scale)

        # Draw the polygon
        self.draw_polygon(cr)

    def draw_polygon(self, cr):
        """Draw the polygon edges using the original coordinates."""
        vertices = self.polygon

        # Set the drawing style
        cr.set_line_width(2)
        cr.set_source_rgb(0, 0, 0)  # Black color for polygon lines
        cr.move_to(vertices[0][0], vertices[0][1])

        # Connect each vertex
        for x, y in vertices[1:]:
            cr.line_to(x, y)

        cr.close_path()
        cr.stroke()

# --- GTK Application --- #

class PolygonApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.PolygonApp")

    def do_activate(self):
        window = PolygonWindow(self)
        window.show()

    def do_shutdown(self):
        print("Application is shutting down.")

# --- Main Entry Point --- #

def main():
    app = PolygonApp()
    app.run()

if __name__ == "__main__":
    main()
