import numpy as np
import pyvista as pv
from typing import Literal


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


def compute_drag(surface: pv.PolyData, variable="drag"):
    surface = surface.point_data_to_cell_data()
    drag = surface[variable]

    normals = surface.cell_normals
    areas = surface.compute_cell_sizes()["Area"]
    freestream_dir = np.array([1.0, 0.0, 0.0])

    dot_products = np.einsum("ij,j->i", normals, freestream_dir)
    drag_contrib = drag * dot_products * areas

    return np.sum(drag_contrib)
