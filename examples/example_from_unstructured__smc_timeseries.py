#
# python -i example_from_unstructured__scm_timeseries.py
#

import iris
from iris import NameConstraint
import numpy as np

import geovista as gv


def callback() -> None:
    global cube
    global mesh
    global idx
    global time
    global actor

    idx = (idx + 1) % cube.shape[0]
    name = mesh.active_scalars_name
    mesh[name] = cube[idx].data
    text = time.units.num2date(time.points[idx]).strftime("%Y-%m-%d %H:%M")
    actor.SetText(3, text)


def prepare(fname, std_name):
    cubes = iris.load(fname)

    cube = cubes.extract_cube(std_name)
    lons = cube.coord("longitude").points
    lats = cube.coord("latitude").points
    base_lon_size = cube.attributes["base_lon_size"]
    base_lat_size = cube.attributes["base_lat_size"]

    cx = cubes.extract_cube(NameConstraint(var_name="cx")).data
    cy = cubes.extract_cube(NameConstraint(var_name="cy")).data

    dlon = cx * base_lon_size
    dlat = cy * base_lat_size

    fac = 0.5
    x1 = (lons - fac * dlon).reshape(-1, 1)
    x2 = (lons + fac * dlon).reshape(-1, 1)
    y1 = (lats - fac * dlat).reshape(-1, 1)
    y2 = (lats + fac * dlat).reshape(-1, 1)

    lons = np.hstack([x1, x2, x2, x1])
    lats = np.hstack([y1, y1, y2, y2])

    return cube, lons, lats


fname = "./gbl_2021112300.nc"
cube, lons, lats = prepare(fname, "sea_surface_wave_significant_height")
time = cube.coord("time")
cube.data

idx = 0

mesh = gv.Transform.from_unstructured(
    lons, lats, lons.shape, data=cube.data[idx], name=cube.name()
)

plotter = gv.GeoBackgroundPlotter()
sargs = dict(title=f"{cube.name()} / {cube.units}")
plotter.add_mesh(
    mesh, cmap="balance", show_edges=False, scalar_bar_args=sargs, edge_color="grey"
)
plotter.add_base_layer(color="grey")
resolution = "10m"
plotter.add_coastlines(resolution=resolution, color="white", line_width=2)
plotter.add_axes()
text = time.units.num2date(time.points[idx]).strftime("%Y-%m-%d %H:%M")
actor = plotter.add_text(text, position="upper_right", font_size=10, shadow=True)
plotter.add_text(
    f"Spherical Multi-Cell ({resolution} Coastlines)",
    position="upper_left",
    font_size=10,
    shadow=True,
)
plotter.add_callback(callback, interval=100)
