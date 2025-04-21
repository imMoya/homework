import pyvista as pv
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from src.postprocess import closest_point_projection_to_surface, sum_surface_variables, compute_drag, plot_meshes, MeshPlotData


@dataclass
class cfd:
    volume: pv.PolyData
    surface: pv.PolyData | pv.UnstructuredGrid

if __name__ == "__main__":
    DATA_FOLDER = Path("cfd_data")
    CAR_VOLUME_FILE = DATA_FOLDER / "volume_car.vtp"
    CAR_SURFACE_FILE = DATA_FOLDER / "surface_car.vtp"
    AIRFOIL_VOLUME_FILE = DATA_FOLDER / "volume_spoiler.vtu"
    AIRFOIL_SURFACE_FILE = DATA_FOLDER / "surface_spoiler.vtp"

    car = cfd(volume=pv.read(CAR_VOLUME_FILE), surface=pv.read(CAR_SURFACE_FILE))
    car.surface = closest_point_projection_to_surface(car.volume, car.surface)
    car.surface = sum_surface_variables(car.surface, "pressure", "wall_shear", "drag")
    print("car drag", compute_drag(car.surface))

    airfoil = cfd(volume=pv.read(AIRFOIL_VOLUME_FILE), surface=pv.read(AIRFOIL_SURFACE_FILE))
    airfoil.surface = closest_point_projection_to_surface(airfoil.volume, airfoil.surface)
    airfoil.surface = airfoil.surface.cell_data_to_point_data()
    airfoil.surface = sum_surface_variables(airfoil.surface, "pressure", "wall_shear", "drag")
    print("airfoil drag", compute_drag(airfoil.surface))

    p = pv.Plotter()
    #p.add_points(airfoil.volume, scalars="pressure")
    p.add_mesh(airfoil.surface, scalars="drag", cmap="coolwarm")
    p.show()

    plot_list = [
        MeshPlotData(
            airfoil.volume, 
            scalar = "pressure", 
            title = "pressure",
        ),
        MeshPlotData(
            airfoil.surface, 
            scalar = "drag", 
            title = "drag",
            kwargs={
                "cmap":"coolwarm"
            }
        )
    ]
    plot_meshes(plot_list)


