import numpy as np
import pyvista as pv
from typing import Literal, Optional


def closest_point_projection_to_surface(
    volume: pv.PolyData | pv.UnstructuredGrid,
    surface: pv.PolyData,
    field_name: str = "pressure",
    method: Literal["interpolate", "sample"] = "interpolate",
):
    if field_name not in volume.point_data and field_name in volume.cell_data:
        volume = volume.cell_data_to_point_data()

    match method:
        case "interpolate":
            return surface.interpolate(volume, n_points=1)
        case "sample":
            return surface.sample(volume)


def sum_surface_variables(surface: pv.PolyData, var1: str, var2: str, var_result: str):
    data = surface.point_data

    data[var_result] = data[var1] + data[var2]
    return surface


def subtract_surface_variables(
    surface: pv.PolyData, var1: str, var2: str, var_result: str
):
    data = surface.point_data

    data[var_result] = data[var1] - data[var2]
    return surface


def compute_drag(
    surface: pv.PolyData,
    pressure_name: Optional[str] = "pressure",
    shear_name: Optional[str] = "wall_shear",
):
    surface = surface.point_data_to_cell_data()

    pressure = surface[pressure_name]
    wall_shear = surface[shear_name]

    normals = surface.cell_normals
    areas = surface.compute_cell_sizes()["Area"]

    pressure_force_x = pressure * normals[:, 0] * areas
    shear_force = wall_shear * areas

    total_drag = np.sum(pressure_force_x + shear_force)

    return total_drag
