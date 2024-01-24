#!/usr/bin/env python3
# Copyright (c) 2021, GeoVista Contributors.
#
# This file is part of GeoVista and is distributed under the 3-Clause BSD license.
# See the LICENSE file in the package root directory for licensing details.

"""
Synthetic Grid
--------------

This example demonstrates how to render a rectilinear grid.

📋 Summary
^^^^^^^^^^

Creates a mesh from 2-D latitude and longitude rectilinear cell bounds.

The resulting mesh contains quad cells.

The data is synthetically generated and targets the mesh faces/cells.

Note that, Natural Earth coastlines are also rendered.

----

"""  # noqa: D205,D212,D400
from __future__ import annotations

import numpy as np

import geovista as gv
import geovista.themes


def main() -> None:
    """Plot the synthetic rectilinear grid.

    Notes
    -----
    .. versionadded:: 0.1.0

    """
    # Create the 2-D spatial coordinates and data.
    M, N = 45, 90
    lats = np.linspace(-90, 90, M + 1)
    lons = np.linspace(-180, 180, N + 1)
    mlons, mlats = np.meshgrid(lons, lats, indexing="xy")
    clim = (0, 1)
    data = np.linspace(*clim, num=M * N)

    # Create the mesh from the synthetic data.
    name = "Synthetic Cells"
    mesh = gv.Transform.from_2d(mlons, mlats, data=data, name=name)

    # Provide mesh diagnostics via logging.
    gv.logger.info("%s", mesh)

    # Plot the rectilinear grid.
    plotter = gv.GeoPlotter()
    sargs = {"title": f"{name} / 1", "shadow": True}
    plotter.add_mesh(
        mesh, clim=clim, cmap="tempo", scalar_bar_args=sargs, show_edges=True
    )
    plotter.add_coastlines()
    plotter.add_axes()
    plotter.add_text(
        "2-D Synthetic Face Data",
        position="upper_left",
        font_size=10,
        shadow=True,
    )
    plotter.camera.zoom(1.3)
    plotter.show()


if __name__ == "__main__":
    main()
