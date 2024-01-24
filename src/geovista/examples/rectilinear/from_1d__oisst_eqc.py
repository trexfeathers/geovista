#!/usr/bin/env python3
# Copyright (c) 2021, GeoVista Contributors.
#
# This file is part of GeoVista and is distributed under the 3-Clause BSD license.
# See the LICENSE file in the package root directory for licensing details.

"""
OISST AVHRR Grid (Projected)
----------------------------

This example demonstrates how to render a projected rectilinear grid.

📋 Summary
^^^^^^^^^^

Creates a mesh from 1-D latitude and longitude rectilinear cell bounds.

The resulting mesh contains quad cells.

The example uses NOAA/NECI 1/4° Daily Optimum Interpolation Sea Surface Temperature
(OISST) v2.1 Advanced Very High Resolution Radiometer (AVHRR) gridded data
(https://doi.org/10.25921/RE9P-PT57). The data targets the mesh faces/cells.

Note that, a threshold is also applied to remove land ``NaN`` cells, and a
NASA Blue Marble base layer is rendered along with Natural Earth coastlines.
The mesh is also transformed to the Equidistant Cylindrical (Plate Carrée)
conformal cylindrical projection.

----

"""  # noqa: D205,D212,D400
from __future__ import annotations

import geovista as gv
from geovista.pantry.data import oisst_avhrr_sst
import geovista.themes


def main() -> None:
    """Plot a projected OISST AVHRR rectilinear grid.

    Notes
    -----
    .. versionadded:: 0.1.0

    """
    # Load the sample data.
    sample = oisst_avhrr_sst()

    # Create the mesh from the sample data.
    mesh = gv.Transform.from_1d(sample.lons, sample.lats, data=sample.data)
    # sphinx_gallery_start_ignore
    # Provide mesh diagnostics via logging.
    gv.logger.info("%s", mesh)
    # sphinx_gallery_end_ignore

    # Remove cells from the mesh with NaN values.
    mesh = mesh.threshold()

    # Plot the rectilinear grid.
    crs = "+proj=eqc"
    plotter = gv.GeoPlotter(crs=crs)
    sargs = {"title": f"{sample.name} / {sample.units}", "shadow": True}
    plotter.add_mesh(mesh, scalar_bar_args=sargs)
    plotter.add_base_layer(texture=gv.blue_marble())
    plotter.add_coastlines()
    plotter.add_axes()
    plotter.add_text(
        f"NOAA/NCEI OISST AVHRR ({crs})",
        position="upper_left",
        font_size=10,
        shadow=True,
    )
    plotter.view_xy()
    plotter.camera.zoom(1.5)
    plotter.show()


if __name__ == "__main__":
    main()
