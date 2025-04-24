from pathlib import Path
from src.postprocess import MeshPlotData

# File directories
DATA_FOLDER = Path("cfd_data")
CAR_VOLUME_FILE = DATA_FOLDER / "volume_car.vtp"
CAR_SURFACE_FILE = DATA_FOLDER / "surface_car.vtp"
CAR_SURFACE_FILE_UPDATED = DATA_FOLDER / "surface_car_updated.vtp"
AIRFOIL_VOLUME_FILE = DATA_FOLDER / "volume_spoiler.vtu"
AIRFOIL_SURFACE_FILE = DATA_FOLDER / "surface_spoiler.vtp"
AIRFOIL_SURFACE_FILE_UPDATED = DATA_FOLDER / "surface_spoiler_updated.vtp"
