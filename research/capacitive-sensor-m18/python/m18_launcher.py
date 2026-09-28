"""
Launcher for the M18 PyVista viewer.

Run this file from Spyder instead of m18_architecture.py.
It starts the 3D application in a separate Python process so
Spyder/IPython cannot interfere with the VTK event loop.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    current_dir = Path(__file__).resolve().parent
    viewer = current_dir / "m18_architecture.py"

    if not viewer.exists():
        raise FileNotFoundError(
            f"No se encontró el visor: {viewer}"
        )

    env = os.environ.copy()

    # Explicitly request a desktop VTK render window.
    env["PYVISTA_JUPYTER_BACKEND"] = "none"
    env["PYVISTA_OFF_SCREEN"] = "false"

    subprocess.Popen(
        [sys.executable, str(viewer), "--vtk-viewer"],
        cwd=str(current_dir),
        env=env,
        creationflags=(
            subprocess.CREATE_NEW_PROCESS_GROUP
            if sys.platform.startswith("win")
            else 0
        ),
    )

    print("Visor M18 iniciado en un proceso Python independiente.")


if __name__ == "__main__":
    main()
