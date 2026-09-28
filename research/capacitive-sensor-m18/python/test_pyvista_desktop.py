"""
Minimal PyVista desktop-window diagnostic for Spyder.

This does NOT load the M18 model.
It only checks whether the current Anaconda/Python installation
can open a native VTK desktop window.
"""

import pyvista as pv

pv.set_jupyter_backend("none")

print("PyVista:", pv.__version__)
print("Testing native VTK window...")

plotter = pv.Plotter(
    off_screen=False,
    notebook=False,
    window_size=(900, 650),
)

plotter.set_background("black")
plotter.add_mesh(
    pv.Cube(),
    color="white",
    show_edges=True,
)

plotter.add_text(
    "VTK TEST — si ves esta ventana, PyVista está funcionando.",
    position="upper_left",
    font_size=12,
)

plotter.show(
    interactive=True,
    auto_close=True,
    jupyter_backend="none",
)
