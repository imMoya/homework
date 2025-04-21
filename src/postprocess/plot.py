from typing import List, Optional, Tuple, Any, Dict
import math
import pyvista as pv
from dataclasses import dataclass, field


@dataclass
class MeshPlotData:
    mesh: pv.PolyData
    scalar: str
    title: Optional[str]
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = field(default_factory=dict)

def infer_shape(n: int) -> Tuple[int, int] | str:
    if n <= 1:
        return None
    left = math.ceil(n / 2)
    right = n - left
    return f'{left}|{right}'


def plot_meshes(
    plot_data: List[MeshPlotData],
    *args: Any,
    **kwargs: Any,
) -> None:
    if not plot_data:
        raise ValueError("plot_data must contain at least one MeshPlotData object.")

    shape = infer_shape(len(plot_data))
    plotter = pv.Plotter(shape=shape, *args, **kwargs) if shape else pv.Plotter(*args, **kwargs)

    for idx, data in enumerate(plot_data):
        if shape:
            plotter.subplot(idx)
        plotter.add_mesh(data.mesh, scalars=data.scalar, *data.args, **data.kwargs)
        if data.title:
            plotter.add_text(data.title)

    plotter.link_views()
    plotter.show()
    