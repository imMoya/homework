import pyvista as pv
from dataclasses import dataclass
from src.postprocess import closest_point_projection_to_surface, compute_drag, plot_meshes, MeshPlotData
from config import *

@dataclass
class cfd:
    volume: pv.PolyData
    surface: pv.PolyData | pv.UnstructuredGrid

if __name__ == "__main__":
    # CAR
    car = cfd(volume=pv.read(CAR_VOLUME_FILE), surface=pv.read(CAR_SURFACE_FILE))
    car.surface = closest_point_projection_to_surface(car.volume, car.surface)
    car.surface.save(CAR_SURFACE_FILE_UPDATED)

    # AIRFOIL
    airfoil = cfd(volume=pv.read(AIRFOIL_VOLUME_FILE), surface=pv.read(AIRFOIL_SURFACE_FILE))
    airfoil.surface = closest_point_projection_to_surface(airfoil.volume, airfoil.surface)
    airfoil.surface.save(AIRFOIL_SURFACE_FILE_UPDATED)

    # CAR PLOT
    plot_list = [
        MeshPlotData(
            car.volume, 
            scalar = "velocity", 
            title = "velocity",
        ),
        MeshPlotData(
            car.surface, 
            scalar = "pressure", 
            title = "pressure",
            kwargs={
                "cmap":"coolwarm"
            }
        )
    ]
    plot_meshes(plot_list)

    # AIRFOIL PLOT
    plot_list = [
        MeshPlotData(
            airfoil.volume, 
            scalar = "velocity", 
            title = "velocity",
        ),
        MeshPlotData(
            airfoil.surface, 
            scalar = "pressure", 
            title = "pressure",
            kwargs={
                "cmap":"coolwarm"
            }
        )
    ]
    plot_meshes(plot_list)
