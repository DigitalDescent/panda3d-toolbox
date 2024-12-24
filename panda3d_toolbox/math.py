"""
"""

import math

from panda3d.core import Vec3, Point2, Point3
from panda3d_toolbox import runtime

def calculate_circle_edge_point(center: Vec3, diameter: float, angle_degrees: float) -> Vec3:
    """
    Calculate the point on the edge of a circle given the center, diameter, and angle.
    """

    # Calculate radius
    radius = diameter / 2

    # Convert angle to radians
    angle_radians = math.radians(angle_degrees)

    # Calculate the x and y coordinates of the point on the edge
    x = center.get_x() + radius * math.cos(angle_radians)
    y = center.get_y() + radius * math.sin(angle_radians)

    return Vec3(x, y, center.get_z())

def map_point_to_screen(nodepath: object, point: object) -> object:
    """
    """

    p3 = runtime.cam.get_relative_point(nodepath, point)
    p2 = Point2()

    if not runtime.base.camlens.project(p3, p2):
        return None

    r2d = Point3(p2[0], 0, p2[1])
    a2d = runtime.base.aspect2d.get_relative_point(runtime.base.render2d, r2d)

    return a2d

def snap_to_grid(node_path: object, grid_size: object) -> tuple:
    """
    """

    x, y, z = node_path[0], node_path[1], node_path[2]
    return (math.floor(x / grid_size[0]) * grid_size[0], 
            math.floor(y / grid_size[1]) * grid_size[1], 
            math.floor(z / grid_size[2]) * grid_size[2])

def get_bounds_of_model(model: object, rotation: float = 0.0) -> tuple:
    """
    """

    h = model.get_h()
    model.set_h(rotation)
    min_corner, max_corner = model.get_tight_bounds()
    model.set_h(h)
    delta = max_corner - min_corner

    return (min_corner, 
            max_corner, 
            Vec3(int(math.ceil(round(delta.get_x(), 1))), 
                 int(math.ceil(round(delta.get_y(), 1))), 
                 int(math.ceil(round(delta.get_z(), 1)))))
