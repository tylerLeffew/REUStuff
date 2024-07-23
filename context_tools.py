import cairo
import contextlib
import math

## Some helpers for using Cairo contexts for drawing things.

# Dependencies:
#   Installed via apt:
#         libcairo2-dev pkg-config python3-dev 
#         python3-gi python3-gi-cairo gir1.2-gtk-3.0 libgirepository1.0-dev
#
#   Installed via pip3:
#         pycairo PyGObject

# Some helpful documentation:
#   https://pygobject.readthedocs.io/en/latest/getting_started.html
#   https://pygobject.readthedocs.io/en/latest/guide/cairo_integration.html

def matrix_to_stretch_rectangle(user_aabb, device_aabb):
    """ Return a Cairo transformation matrix that maps the given user
    rectangle into the given device rectangle, both given as (lower left,
    upper right).  Strecthes as needed."""

    xx = (device_aabb[1][0] - device_aabb[0][0]) / (user_aabb[1][0] - user_aabb[0][0])
    x0 = device_aabb[0][0] - xx*user_aabb[0][0]

    yy = (device_aabb[1][1] - device_aabb[0][1]) / (user_aabb[1][1] - user_aabb[0][1])
    y0 = device_aabb[0][1] - yy*user_aabb[0][1]

    return cairo.Matrix(xx=xx, yx=0, xy=0, yy=yy, x0=x0, y0=y0)

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

    return matrix_to_stretch_rectangle(real_user_aabb, device_aabb)

def vflip_font(context):
    """ Change the current font matrix by inverting its vertical axis.  This is
    important if we've re-wired the coordinate system to have the origin in the
    bottom left (where it belongs). """

    m = context.get_font_matrix()
    m.yy = -m.yy
    context.set_font_matrix(m)

@contextlib.contextmanager
def mapped_png_context(fullpath, user_aabb, svg_size):
    with cairo.SVGSurface("/dev/null", svg_size[0], svg_size[1]) as surface:
        device_aabb = ((0, svg_size[1]), (svg_size[0], 0))
        context = cairo.Context(surface)
        context.set_matrix(matrix_to_fit_rectangle(user_aabb, device_aabb, padding=0.1))
        yield context
        surface.write_to_png(fullpath)
        

@contextlib.contextmanager
def mapped_svg_context(fullpath, user_aabb, svg_size):
    with cairo.SVGSurface(fullpath, svg_size[0], svg_size[1]) as surface:
        device_aabb = ((0, svg_size[1]), (svg_size[0], 0))
        context = cairo.Context(surface)
        context.set_matrix(matrix_to_fit_rectangle(user_aabb, device_aabb, padding=0.1))
        yield context 

@contextlib.contextmanager
def mapped_pdf_context(fullpath, user_aabb, pdf_size):
    with cairo.PDFSurface(fullpath, pdf_size[0], pdf_size[1]) as surface:
        device_aabb = ((0, pdf_size[1]), (pdf_size[0], 0))
        context = cairo.Context(surface)
        context.set_matrix(matrix_to_fit_rectangle(user_aabb, device_aabb, padding=0.1))
        yield context 


def draw_arrowhead(ctx, start, end, length, spread, filled=True):
    v = (start[0] - end[0], start[1] - end[1])
    angle_center = math.atan2(v[1], v[0])
    angle_left = angle_center + spread/2
    tip_left = (end[0] + length*math.cos(angle_left), end[1] + length*math.sin(angle_left))
    angle_right = angle_center - spread/2
    tip_right = (end[0] + length*math.cos(angle_right), end[1] + length*math.sin(angle_right))

    if filled:
        ctx.move_to(end[0], end[1])
        ctx.line_to(tip_left[0], tip_left[1])
        ctx.line_to(tip_right[0], tip_right[1])
        ctx.line_to(end[0], end[1])
        ctx.fill()

    ctx.move_to(end[0], end[1])
    ctx.line_to(tip_left[0], tip_left[1])
    ctx.move_to(tip_right[0], tip_right[1])
    ctx.line_to(end[0], end[1])
    ctx.stroke()

