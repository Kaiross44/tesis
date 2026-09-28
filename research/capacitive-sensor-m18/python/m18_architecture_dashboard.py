"""
Dashboard 3D paramétrico para arquitecturas candidatas de sensor capacitivo M18.

Uso:
    python m18_architecture_dashboard.py

Dependencias:
    pip install pyvista numpy
    Tkinter suele venir incluido con Python en Windows.

Nota metodológica:
    Las arquitecturas H1-H4 son MODELOS CANDIDATOS. No representan la
    arquitectura interna confirmada de un sensor comercial concreto.
"""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk

import pyvista as pv


# ---------------------------------------------------------------------------
# CONFIGURACIÓN DEL ESTUDIO
# ---------------------------------------------------------------------------

SENSOR_DIAMETER_MM = 18.0
SENSOR_LENGTH_MM = 69.0

GLOBAL_DEFAULTS = {
    "target_distance_mm": 6.0,
    "target_radius_mm": 8.0,
    "excitation_v": 24.0,
    "explosion": 0.0,
}

ARCH_DEFAULTS = {
    "H1": {
        "core_radius_mm": 2.5,
        "gap_mm": 0.8,
        "aux_outer_radius_mm": 7.0,
    },
    "H2": {
        "core_radius_mm": 2.5,
        "guard_radius_mm": 4.5,
        "gap_mm": 0.8,
        "guard_width_mm": 1.2,
    },
    "H3": {
        "core_radius_mm": 2.5,
        "shield_inner_radius_mm": 3.8,
        "shield_outer_radius_mm": 5.0,
        "gap_mm": 0.8,
    },
    "H4": {
        "electrode_length_mm": 12.0,
        "axial_gap_mm": 2.0,
        "electrode_radius_mm": 5.5,
    },
}


# ---------------------------------------------------------------------------
# UTILIDADES GEOMÉTRICAS
# ---------------------------------------------------------------------------

def mm(value: float) -> float:
    """Convierte mm a unidades de escena."""
    return value / 10.0


def target_z(distance_mm: float) -> float:
    """Posición del objetivo delante de la cara activa (-Z)."""
    return -mm(SENSOR_LENGTH_MM / 2.0 + distance_mm)


def make_annular_electrode(
    outer_radius_mm: float,
    inner_radius_mm: float,
    height_mm: float,
    center_z_mm: float,
) -> pv.PolyData:
    """Electrodo anular frontal robusto, sin booleanos de VTK."""
    if inner_radius_mm <= 0 or inner_radius_mm >= outer_radius_mm:
        raise ValueError(
            "Debe cumplirse 0 < inner_radius_mm < outer_radius_mm."
        )

    ring = pv.Disc(
        inner=mm(inner_radius_mm),
        outer=mm(outer_radius_mm),
        center=(0, 0, mm(center_z_mm)),
        normal=(0, 0, 1),
        r_res=1,
        c_res=96,
    )

    # Un pequeño espesor evita depender de booleanos entre cilindros.
    # La malla final se triangula para una representación estable.
    extruded = ring.extrude(
        vector=(0, 0, mm(height_mm)),
        capping=True,
    )
    return extruded.triangulate()

def make_sensor_body(explosion: float) -> pv.PolyData:
    """Carcasa externa transparente del M18."""
    body = pv.Cylinder(
        radius=mm(SENSOR_DIAMETER_MM / 2.0),
        height=mm(SENSOR_LENGTH_MM),
        direction=(0, 0, 1),
        center=(0, 0, 0),
        resolution=96,
    )
    # La carcasa se desplaza lateralmente en modo explosionado.
    return body.translate((mm(20.0 * explosion), 0, 0), inplace=False)


def make_front_disc(radius_mm: float, z_mm: float, offset_x_mm: float = 0.0) -> pv.PolyData:
    return pv.Disc(
        inner=0.0,
        outer=mm(radius_mm),
        center=(mm(offset_x_mm), 0, mm(z_mm)),
        normal=(0, 0, 1),
        r_res=1,
        c_res=96,
    )


def add_target(plotter: pv.Plotter, distance_mm: float) -> None:
    """Objetivo conductor común a las cuatro vistas."""
    target = pv.Disc(
        inner=0.0,
        outer=mm(GLOBAL_DEFAULTS["target_radius_mm"]),
        center=(0, 0, target_z(distance_mm)),
        normal=(0, 0, 1),
        r_res=1,
        c_res=96,
    )
    plotter.add_mesh(
        target,
        color="gold",
        opacity=0.65,
        show_edges=True,
        line_width=1,
    )


# ---------------------------------------------------------------------------
# MODELOS CANDIDATOS
# ---------------------------------------------------------------------------

class ArchitectureModel:
    """Genera la geometría visual de una arquitectura candidata."""

    COLORS = {
        "core": "tomato",
        "aux": "royalblue",
        "guard": "seagreen",
        "shield": "gold",
        "body": "lightgray",
        "dielectric": "plum",
    }

    def __init__(self, name: str, title: str, params: dict[str, float]) -> None:
        self.name = name
        self.title = title
        self.params = dict(params)

    def build(self, explosion: float) -> list[tuple[pv.PolyData, dict]]:
        raise NotImplementedError


class H1Model(ArchitectureModel):
    """Electrodo central + electrodo auxiliar anular."""

    def build(self, explosion: float):
        p = self.params
        z = -SENSOR_LENGTH_MM / 2.0
        gap = p["gap_mm"]

        core = make_front_disc(p["core_radius_mm"], z + 0.2, -6.0 * explosion)
        aux = make_annular_electrode(
            p["aux_outer_radius_mm"],
            p["core_radius_mm"] + gap,
            0.8,
            z + 0.2,
        )
        return [
            (core, {"color": self.COLORS["core"], "opacity": 1.0}),
            (aux, {"color": self.COLORS["aux"], "opacity": 0.95}),
        ]


class H2Model(ArchitectureModel):
    """Electrodo central + guarda/blindaje anular."""

    def build(self, explosion: float):
        p = self.params
        z = -SENSOR_LENGTH_MM / 2.0
        gap = p["gap_mm"]
        guard_inner = p["guard_radius_mm"]
        guard_outer = guard_inner + p["guard_width_mm"]

        core = make_front_disc(p["core_radius_mm"], z + 0.25, -7.0 * explosion)
        guard = make_annular_electrode(
            guard_outer,
            guard_inner,
            0.8,
            z + 0.25 + 1.0 * explosion,
        )

        return [
            (core, {"color": self.COLORS["core"], "opacity": 1.0}),
            (guard, {"color": self.COLORS["guard"], "opacity": 0.95}),
        ]


class H3Model(ArchitectureModel):
    """Electrodo interno + shield + electrodo externo."""

    def build(self, explosion: float):
        p = self.params
        z = -SENSOR_LENGTH_MM / 2.0

        core = make_front_disc(p["core_radius_mm"], z + 0.3, -7.5 * explosion)
        shield = make_annular_electrode(
            p["shield_outer_radius_mm"],
            p["shield_inner_radius_mm"],
            0.8,
            z + 0.3,
        )

        outer = make_annular_electrode(
            SENSOR_DIAMETER_MM / 2.0 - 1.0,
            p["shield_outer_radius_mm"] + p["gap_mm"],
            1.0,
            z + 0.3 + 7.5 * explosion,
        )

        return [
            (core, {"color": self.COLORS["core"], "opacity": 1.0}),
            (shield, {"color": self.COLORS["shield"], "opacity": 0.9}),
            (outer, {"color": self.COLORS["body"], "opacity": 0.6}),
        ]


class H4Model(ArchitectureModel):
    """Electrodos cilíndricos separados axialmente."""

    def build(self, explosion: float):
        p = self.params
        r = mm(p["electrode_radius_mm"])
        h1 = mm(p["electrode_length_mm"])
        gap = mm(p["axial_gap_mm"])
        z0 = -SENSOR_LENGTH_MM / 2.0

        e1 = pv.Cylinder(
            radius=r,
            height=h1,
            direction=(0, 0, 1),
            center=(0, 0, mm(z0 + p["electrode_length_mm"] / 2.0)),
            resolution=96,
        )
        e2 = pv.Cylinder(
            radius=r,
            height=h1,
            direction=(0, 0, 1),
            center=(0, 0, mm(
                z0 + p["electrode_length_mm"] * 1.5 + p["axial_gap_mm"]
            )),
            resolution=96,
        )

        # Separación visual en la dirección axial.
        e1 = e1.translate((-mm(5.0 * explosion), 0, 0), inplace=False)
        e2 = e2.translate((mm(5.0 * explosion), 0, 0), inplace=False)

        return [
            (e1, {"color": self.COLORS["core"], "opacity": 0.95}),
            (e2, {"color": self.COLORS["aux"], "opacity": 0.95}),
        ]


ARCHITECTURES: dict[str, ArchitectureModel] = {
    "H1": H1Model(
        "H1",
        "H1 · Central + auxiliar anular",
        ARCH_DEFAULTS["H1"],
    ),
    "H2": H2Model(
        "H2",
        "H2 · Central + guarda",
        ARCH_DEFAULTS["H2"],
    ),
    "H3": H3Model(
        "H3",
        "H3 · Core + shield + externo",
        ARCH_DEFAULTS["H3"],
    ),
    "H4": H4Model(
        "H4",
        "H4 · Electrodos axiales",
        ARCH_DEFAULTS["H4"],
    ),
}


# ---------------------------------------------------------------------------
# MÉTRICAS DE PRIMERA VERSIÓN
# ---------------------------------------------------------------------------

def analytical_capacitance_proxy(area_mm2: float, separation_mm: float, eps_r: float = 1.0) -> float:
    """Proxy didáctico de C en pF; NO es el FEM real."""
    eps0 = 8.8541878128e-12
    area_m2 = area_mm2 * 1e-6
    separation_m = max(separation_mm * 1e-3, 1e-9)
    c_farads = eps0 * eps_r * area_m2 / separation_m
    return c_farads * 1e12


def update_metrics(model: ArchitectureModel, target_distance_mm: float) -> str:
    p = model.params

    if model.name == "H1":
        area = math.pi * p["core_radius_mm"] ** 2
        c_proxy = analytical_capacitance_proxy(
            area,
            p["gap_mm"],
        )
    elif model.name == "H2":
        area = math.pi * p["core_radius_mm"] ** 2
        c_proxy = analytical_capacitance_proxy(
            area,
            p["gap_mm"],
        )
    elif model.name == "H3":
        area = math.pi * p["core_radius_mm"] ** 2
        c_proxy = analytical_capacitance_proxy(
            area,
            p["gap_mm"],
        )
    else:
        area = 2.0 * math.pi * p["electrode_radius_mm"] * p["electrode_length_mm"]
        c_proxy = analytical_capacitance_proxy(
            area,
            p["axial_gap_mm"],
        )

    return (
        f"{model.name}\n"
        f"Objetivo: {target_distance_mm:.1f} mm\n"
        f"C_proxy: {c_proxy:.3f} pF\n"
        f"Nota: proxy geométrico, no FEM"
    )


# ---------------------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------------------

class M18Dashboard:
    def __init__(self) -> None:
        self.global_vars = dict(GLOBAL_DEFAULTS)
        self.control_vars: dict[str, tk.DoubleVar] = {}

        self.plotter = pv.Plotter(
            shape=(2, 2),
            title="M18 Capacitive Sensor — Architecture Study",
            window_size=(1400, 850),
        )
        self.plotter.set_background("#11131A")

        self.actors: dict[str, list] = {name: [] for name in ARCHITECTURES}
        self.text_actors: dict[str, list] = {name: [] for name in ARCHITECTURES}

        self.root = tk.Tk()
        self.root.title("M18 — Control Panel")
        self.root.geometry("430x760")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self._build_control_panel()
        self._draw_all()

        # El panel Tkinter actualiza la escena de forma cooperativa.
        self.root.after(100, self._pump)

    def _build_control_panel(self) -> None:
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        global_tab = ttk.Frame(notebook)
        notebook.add(global_tab, text="Globales")

        self._add_slider(
            global_tab,
            "Distancia objetivo d [mm]",
            "target_distance_mm",
            0.5,
            25.0,
            self.global_vars["target_distance_mm"],
            self._on_global_change,
        )
        self._add_slider(
            global_tab,
            "Radio objetivo [mm]",
            "target_radius_mm",
            1.0,
            12.0,
            self.global_vars["target_radius_mm"],
            self._on_global_change,
        )
        self._add_slider(
            global_tab,
            "Excitación V [V]",
            "excitation_v",
            1.0,
            100.0,
            self.global_vars["excitation_v"],
            self._on_global_change,
        )
        self._add_slider(
            global_tab,
            "Explosión",
            "explosion",
            0.0,
            1.0,
            self.global_vars["explosion"],
            self._on_global_change,
            resolution=0.01,
        )

        self.global_status = tk.StringVar(
            value="Las cuatro arquitecturas comparten estas variables."
        )
        ttk.Label(
            global_tab,
            textvariable=self.global_status,
            wraplength=360,
            justify="left",
        ).pack(padx=12, pady=20)

        # Pestañas independientes por arquitectura.
        self._build_h1_tab(notebook)
        self._build_h2_tab(notebook)
        self._build_h3_tab(notebook)
        self._build_h4_tab(notebook)

        ttk.Label(
            self.root,
            text=(
                "Modelos candidatos H1–H4. Las dimensiones internas no "
                "representan el interior confirmado de un fabricante."
            ),
            wraplength=390,
            justify="left",
        ).pack(padx=12, pady=(0, 10))

    def _add_slider(
        self,
        parent: ttk.Frame,
        label: str,
        key: str,
        low: float,
        high: float,
        value: float,
        callback,
        resolution: float = 0.1,
    ) -> None:
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=12, pady=8)

        value_var = tk.DoubleVar(value=value)
        self.control_vars[key] = value_var

        ttk.Label(frame, text=label).pack(anchor="w")
        scale = tk.Scale(
            frame,
            from_=low,
            to=high,
            resolution=resolution,
            orient="horizontal",
            variable=value_var,
            command=lambda _: callback(key),
        )
        scale.pack(fill="x")

    def _architecture_slider(
        self,
        parent: ttk.Frame,
        arch_name: str,
        param: str,
        label: str,
        low: float,
        high: float,
        resolution: float = 0.1,
    ) -> None:
        full_key = f"{arch_name}.{param}"
        value = ARCHITECTURES[arch_name].params[param]
        var = tk.DoubleVar(value=value)
        self.control_vars[full_key] = var

        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=12, pady=7)

        ttk.Label(frame, text=label).pack(anchor="w")
        tk.Scale(
            frame,
            from_=low,
            to=high,
            resolution=resolution,
            orient="horizontal",
            variable=var,
            command=lambda _: self._on_arch_change(arch_name, param),
        ).pack(fill="x")

    def _build_h1_tab(self, notebook: ttk.Notebook) -> None:
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="H1")
        ttk.Label(tab, text="Central + auxiliar anular").pack(pady=10)
        self._architecture_slider(tab, "H1", "core_radius_mm", "Radio core [mm]", 0.5, 7.0)
        self._architecture_slider(tab, "H1", "gap_mm", "Entrehierro g [mm]", 0.1, 3.0)
        self._architecture_slider(tab, "H1", "aux_outer_radius_mm", "Radio externo auxiliar [mm]", 3.0, 8.5)

    def _build_h2_tab(self, notebook: ttk.Notebook) -> None:
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="H2")
        ttk.Label(tab, text="Central + guarda/blindaje").pack(pady=10)
        self._architecture_slider(tab, "H2", "core_radius_mm", "Radio core [mm]", 0.5, 7.0)
        self._architecture_slider(tab, "H2", "guard_radius_mm", "Radio interno guarda [mm]", 2.0, 8.0)
        self._architecture_slider(tab, "H2", "gap_mm", "Entrehierro g [mm]", 0.1, 3.0)
        self._architecture_slider(tab, "H2", "guard_width_mm", "Ancho guarda [mm]", 0.2, 3.0)

    def _build_h3_tab(self, notebook: ttk.Notebook) -> None:
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="H3")
        ttk.Label(tab, text="Core + shield + electrodo externo").pack(pady=10)
        self._architecture_slider(tab, "H3", "core_radius_mm", "Radio core [mm]", 0.5, 7.0)
        self._architecture_slider(tab, "H3", "shield_inner_radius_mm", "Radio interno shield [mm]", 2.0, 8.0)
        self._architecture_slider(tab, "H3", "shield_outer_radius_mm", "Radio externo shield [mm]", 2.5, 8.5)
        self._architecture_slider(tab, "H3", "gap_mm", "Entrehierro g [mm]", 0.1, 2.0)

    def _build_h4_tab(self, notebook: ttk.Notebook) -> None:
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="H4")
        ttk.Label(tab, text="Electrodos separados axialmente").pack(pady=10)
        self._architecture_slider(tab, "H4", "electrode_length_mm", "Longitud electrodo [mm]", 2.0, 25.0)
        self._architecture_slider(tab, "H4", "axial_gap_mm", "Separación axial [mm]", 0.2, 8.0)
        self._architecture_slider(tab, "H4", "electrode_radius_mm", "Radio electrodo [mm]", 1.0, 8.5)

    def _on_global_change(self, key: str) -> None:
        self.global_vars[key] = self.control_vars[key].get()
        self._draw_all()

    def _on_arch_change(self, arch_name: str, param: str) -> None:
        key = f"{arch_name}.{param}"
        ARCHITECTURES[arch_name].params[param] = self.control_vars[key].get()
        self._draw_all()

    def _clear_architecture(self, index: int, name: str) -> None:
        self.plotter.subplot(index // 2, index % 2)
        for actor in self.actors[name]:
            try:
                self.plotter.remove_actor(actor)
            except Exception:
                pass
        self.actors[name] = []
        for text_actor in self.text_actors[name]:
            try:
                self.plotter.remove_actor(text_actor)
            except Exception:
                pass
        self.text_actors[name] = []

    def _draw_architecture(self, index: int, name: str) -> None:
        self._clear_architecture(index, name)

        row = index // 2
        col = index % 2
        self.plotter.subplot(row, col)

        model = ARCHITECTURES[name]

        # Carcasa común.
        body = make_sensor_body(self.global_vars["explosion"])
        actor_body = self.plotter.add_mesh(
            body,
            color="lightgray",
            opacity=0.18,
            show_edges=True,
            line_width=1,
        )
        self.actors[name].append(actor_body)

        for mesh, kwargs in model.build(self.global_vars["explosion"]):
            actor = self.plotter.add_mesh(mesh, **kwargs, show_edges=True)
            self.actors[name].append(actor)

        # Objetivo y referencia visual.
        target = pv.Cylinder(
            radius=mm(self.global_vars["target_radius_mm"]),
            height=mm(0.4),
            direction=(0, 0, 1),
            center=(0, 0, target_z(self.global_vars["target_distance_mm"])),
            resolution=72,
        )
        target_actor = self.plotter.add_mesh(
            target,
            color="gold",
            opacity=0.35,
            show_edges=True,
        )
        self.actors[name].append(target_actor)

        title_actor = self.plotter.add_text(
            model.title,
            position="upper_left",
            font_size=11,
        )
        metric_actor = self.plotter.add_text(
            update_metrics(
                model,
                self.global_vars["target_distance_mm"],
            ),
            position="lower_left",
            font_size=9,
        )
        self.text_actors[name].extend([title_actor, metric_actor])

        self.plotter.view_isometric()
        self.plotter.reset_camera()

    def _draw_all(self) -> None:
        for index, name in enumerate(ARCHITECTURES):
            self._draw_architecture(index, name)

    def _pump(self) -> None:
        """Mantiene Tkinter y la ventana VTK sincronizadas en Spyder."""
        try:
            self.plotter.update()
        except Exception:
            return
        if self.root.winfo_exists():
            self.root.after(50, self._pump)

    def show(self) -> None:
        # La ventana VTK se muestra de forma interactiva.
        self.plotter.show(interactive_update=True, auto_close=False)

        try:
            self.root.mainloop()
        finally:
            self.close()

    def close(self) -> None:
        try:
            self.plotter.close()
        except Exception:
            pass

        try:
            self.root.destroy()
        except tk.TclError:
            pass


if __name__ == "__main__":
    M18Dashboard().show()
