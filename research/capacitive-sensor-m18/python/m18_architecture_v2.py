"""
M18 Capacitive Sensor — Interactive Architecture Study
======================================================

Versión 2: una sola ventana PyVista/VTK.

- 4 arquitecturas visibles simultáneamente (2x2).
- Objetivo conductor común.
- Vista explosionada.
- Selector H1/H2/H3/H4 mediante radio buttons.
- 3 sliders de parámetros para la arquitectura activa.
- Sliders globales para distancia al objetivo y explosión.
- Sin Tkinter: evita conflictos de ciclos de eventos con Spyder.

IMPORTANTE:
    H1-H4 son arquitecturas CANDIDATAS.
    NO representan la arquitectura interna confirmada de un sensor comercial.

Envolvente conocida:
    Ø18 mm
    L = 69 mm

La capacitancia mostrada actualmente es C_proxy, un indicador didáctico.
Todavía no es un resultado FEM ni un cálculo electrostático real.
"""

from __future__ import annotations

import math
from typing import Callable

import pyvista as pv


# ============================================================
# CONFIGURACIÓN DEL SENSOR
# ============================================================

SENSOR_DIAMETER_MM = 18.0
SENSOR_LENGTH_MM = 69.0


# ============================================================
# VARIABLES GLOBALES
# ============================================================

GLOBAL = {
    "target_distance_mm": 6.0,
    "target_radius_mm": 8.0,
    "excitation_v": 24.0,
    "explosion": 0.0,
}


# ============================================================
# VARIABLES DE LAS ARQUITECTURAS
# ============================================================

PARAMS = {
    "H1": {
        "core_radius_mm": 2.5,
        "gap_mm": 0.8,
        "aux_outer_radius_mm": 7.0,
    },

    "H2": {
        "core_radius_mm": 2.5,
        "gap_mm": 0.8,
        "guard_width_mm": 1.2,
    },

    "H3": {
        "core_radius_mm": 2.5,
        "shield_inner_radius_mm": 3.8,
        "shield_outer_radius_mm": 5.0,
        "external_gap_mm": 0.8,
    },

    "H4": {
        "electrode_radius_mm": 5.5,
        "axial_gap_mm": 2.0,
        "electrode_length_mm": 12.0,
    },
}


# ============================================================
# DEFINICIÓN DE LOS 3 PARÁMETROS DEL PANEL ACTIVO
# ============================================================

ACTIVE_PARAMETER_DEFINITION = {

    "H1": [
        ("core_radius_mm", "Radio core [mm]", 0.5, 5.0, 0.1),
        ("gap_mm", "Entrehierro g [mm]", 0.1, 3.0, 0.1),
        (
            "aux_outer_radius_mm",
            "Radio exterior auxiliar [mm]",
            3.0,
            8.5,
            0.1,
        ),
    ],

    "H2": [
        ("core_radius_mm", "Radio core [mm]", 0.5, 5.0, 0.1),
        ("gap_mm", "Entrehierro g [mm]", 0.1, 2.0, 0.1),
        ("guard_width_mm", "Ancho guarda [mm]", 0.2, 2.0, 0.1),
    ],

    "H3": [
        ("core_radius_mm", "Radio core [mm]", 0.5, 5.0, 0.1),
        (
            "shield_inner_radius_mm",
            "Radio interno shield [mm]",
            2.0,
            6.5,
            0.1,
        ),
        (
            "external_gap_mm",
            "Separación externa [mm]",
            0.1,
            1.5,
            0.1,
        ),
    ],

    "H4": [
        (
            "electrode_radius_mm",
            "Radio electrodo [mm]",
            1.0,
            8.5,
            0.1,
        ),
        (
            "axial_gap_mm",
            "Separación axial [mm]",
            0.2,
            8.0,
            0.1,
        ),
        (
            "electrode_length_mm",
            "Longitud electrodo [mm]",
            2.0,
            25.0,
            0.1,
        ),
    ],
}


# ============================================================
# UTILIDADES
# ============================================================

def mm(value: float) -> float:
    """Convierte mm a unidades gráficas."""
    return value / 10.0


def active_face_z() -> float:
    """Posición de la cara activa del sensor."""
    return -mm(SENSOR_LENGTH_MM / 2.0)


def target_z(distance_mm: float) -> float:
    """Objetivo colocado delante de la cara activa."""
    return active_face_z() - mm(distance_mm)


# ============================================================
# GEOMETRÍA
# ============================================================

def make_disc(
    radius_mm: float,
    center_z_mm: float,
    thickness_mm: float = 0.25,
) -> pv.PolyData:
    """Disco sólido delgado."""

    if radius_mm <= 0:
        raise ValueError("El radio debe ser positivo.")

    disc = pv.Disc(
        inner=0.0,
        outer=mm(radius_mm),
        center=(
            0.0,
            0.0,
            mm(center_z_mm),
        ),
        normal=(
            0.0,
            0.0,
            1.0,
        ),
        r_res=1,
        c_res=96,
    )

    return disc.extrude(
        vector=(
            0.0,
            0.0,
            mm(thickness_mm),
        ),
        capping=True,
    ).triangulate()


def make_ring(
    outer_radius_mm: float,
    inner_radius_mm: float,
    center_z_mm: float,
    thickness_mm: float = 0.25,
) -> pv.PolyData | None:
    """Anillo sólido delgado, sin operaciones booleanas."""

    if inner_radius_mm <= 0:
        return None

    if outer_radius_mm <= inner_radius_mm:
        return None

    ring = pv.Disc(
        inner=mm(inner_radius_mm),
        outer=mm(outer_radius_mm),
        center=(
            0.0,
            0.0,
            mm(center_z_mm),
        ),
        normal=(
            0.0,
            0.0,
            1.0,
        ),
        r_res=1,
        c_res=96,
    )

    return ring.extrude(
        vector=(
            0.0,
            0.0,
            mm(thickness_mm),
        ),
        capping=True,
    ).triangulate()


def make_body(
    explosion: float = 0.0,
) -> pv.PolyData:
    """Carcasa M18 conceptual."""

    body = pv.Cylinder(
        radius=mm(SENSOR_DIAMETER_MM / 2.0),
        height=mm(SENSOR_LENGTH_MM),
        direction=(
            0.0,
            0.0,
            1.0,
        ),
        center=(
            mm(12.0 * explosion),
            0.0,
            0.0,
        ),
        resolution=96,
    )

    return body.triangulate()


def make_target(
    distance_mm: float,
    radius_mm: float,
) -> pv.PolyData:
    """Objetivo metálico conductor."""

    target = pv.Cylinder(
        radius=mm(radius_mm),
        height=mm(0.4),
        direction=(
            0.0,
            0.0,
            1.0,
        ),
        center=(
            0.0,
            0.0,
            target_z(distance_mm),
        ),
        resolution=96,
    )

    return target.triangulate()


# ============================================================
# PROXY DE CAPACITANCIA
# ============================================================

def capacitance_proxy(
    architecture: str,
) -> float:
    """
    Indicador geométrico simplificado.

    NO representa el resultado FEM.
    """

    eps0 = 8.8541878128e-12
    p = PARAMS[architecture]

    if architecture in ("H1", "H2", "H3"):

        area_m2 = (
            math.pi
            * (
                p["core_radius_mm"]
                * 1e-3
            ) ** 2
        )

        if architecture == "H3":

            separation_mm = max(
                p["shield_inner_radius_mm"]
                - p["core_radius_mm"],
                0.05,
            )

        else:

            separation_mm = p["gap_mm"]

    else:

        area_m2 = (
            2.0
            * math.pi
            * p["electrode_radius_mm"]
            * p["electrode_length_mm"]
            * 1e-6
        )

        separation_mm = p["axial_gap_mm"]

    separation_m = max(
        separation_mm * 1e-3,
        1e-9,
    )

    capacitance_f = (
        eps0
        * area_m2
        / separation_m
    )

    return capacitance_f * 1e12


# ============================================================
# ACTORES
# ============================================================

ARCHITECTURE_COLORS = {
    "H1": {
        "core": "tomato",
        "aux": "royalblue",
    },

    "H2": {
        "core": "tomato",
        "guard": "seagreen",
    },

    "H3": {
        "core": "tomato",
        "shield": "gold",
        "outer": "silver",
    },

    "H4": {
        "e1": "tomato",
        "e2": "royalblue",
    },
}


# ============================================================
# CONSTRUCTOR DE H1
# ============================================================

def build_H1(
    explosion: float,
):
    p = PARAMS["H1"]

    z = -SENSOR_LENGTH_MM / 2.0 + 0.2
    s = 7.0 * explosion

    core = make_disc(
        p["core_radius_mm"],
        z,
    )

    core = core.translate(
        (
            mm(-s),
            0.0,
            0.0,
        ),
        inplace=False,
    )

    aux = make_ring(
        p["aux_outer_radius_mm"],
        p["core_radius_mm"] + p["gap_mm"],
        z,
    )

    if aux is not None:

        aux = aux.translate(
            (
                mm(s),
                0.0,
                0.0,
            ),
            inplace=False,
        )

    return [
        (
            core,
            "core",
            1.0,
        ),
        (
            aux,
            "aux",
            0.95,
        ),
    ]


# ============================================================
# CONSTRUCTOR DE H2
# ============================================================

def build_H2(
    explosion: float,
):
    p = PARAMS["H2"]

    z = -SENSOR_LENGTH_MM / 2.0 + 0.2
    s = 7.0 * explosion

    core = make_disc(
        p["core_radius_mm"],
        z,
    )

    core = core.translate(
        (
            mm(-s),
            0.0,
            0.0,
        ),
        inplace=False,
    )

    guard_inner = (
        p["core_radius_mm"]
        + p["gap_mm"]
    )

    guard_outer = (
        guard_inner
        + p["guard_width_mm"]
    )

    guard = make_ring(
        guard_outer,
        guard_inner,
        z,
    )

    if guard is not None:

        guard = guard.translate(
            (
                mm(s),
                0.0,
                mm(1.0 * explosion),
            ),
            inplace=False,
        )

    return [
        (
            core,
            "core",
            1.0,
        ),
        (
            guard,
            "guard",
            0.95,
        ),
    ]


# ============================================================
# CONSTRUCTOR DE H3
# ============================================================

def build_H3(
    explosion: float,
):
    p = PARAMS["H3"]

    z = -SENSOR_LENGTH_MM / 2.0 + 0.2
    s = 8.0 * explosion

    core = make_disc(
        p["core_radius_mm"],
        z,
    )

    core = core.translate(
        (
            mm(-s),
            0.0,
            0.0,
        ),
        inplace=False,
    )

    shield = make_ring(
        p["shield_outer_radius_mm"],
        p["shield_inner_radius_mm"],
        z,
    )

    if shield is not None:

        shield = shield.translate(
            (
                0.0,
                mm(2.5 * explosion),
                0.0,
            ),
            inplace=False,
        )

    outer_inner = (
        p["shield_outer_radius_mm"]
        + p["external_gap_mm"]
    )

    outer = make_ring(
        SENSOR_DIAMETER_MM / 2.0 - 0.5,
        outer_inner,
        z,
    )

    if outer is not None:

        outer = outer.translate(
            (
                mm(s),
                0.0,
                0.0,
            ),
            inplace=False,
        )

    return [
        (
            core,
            "core",
            1.0,
        ),
        (
            shield,
            "shield",
            0.90,
        ),
        (
            outer,
            "outer",
            0.60,
        ),
    ]


# ============================================================
# CONSTRUCTOR DE H4
# ============================================================

def build_H4(
    explosion: float,
):
    p = PARAMS["H4"]

    radius = mm(
        p["electrode_radius_mm"]
    )

    length = mm(
        p["electrode_length_mm"]
    )

    gap = mm(
        p["axial_gap_mm"]
    )

    z0 = -mm(
        SENSOR_LENGTH_MM / 2.0
    )

    z1 = z0 + length / 2.0

    z2 = (
        z0
        + length
        + gap
        + length / 2.0
    )

    e1 = pv.Cylinder(
        radius=radius,
        height=length,
        direction=(
            0.0,
            0.0,
            1.0,
        ),
        center=(
            -mm(4.0 * explosion),
            0.0,
            z1,
        ),
        resolution=96,
    ).triangulate()

    e2 = pv.Cylinder(
        radius=radius,
        height=length,
        direction=(
            0.0,
            0.0,
            1.0,
        ),
        center=(
            mm(4.0 * explosion),
            0.0,
            z2,
        ),
        resolution=96,
    ).triangulate()

    return [
        (
            e1,
            "e1",
            0.95,
        ),
        (
            e2,
            "e2",
            0.95,
        ),
    ]


BUILDERS: dict[
    str,
    Callable[[float], list],
] = {
    "H1": build_H1,
    "H2": build_H2,
    "H3": build_H3,
    "H4": build_H4,
}


# ============================================================
# DASHBOARD
# ============================================================

class M18Study:

    def __init__(self):

        self.active_architecture = "H1"

        # ----------------------------------------------------
        # Plotter único
        # ----------------------------------------------------

        self.plotter = pv.Plotter(
            shape=(2, 2),
            window_size=(
                1550,
                950,
            ),
            title=(
                "M18 Capacitive Sensor "
                "— Architecture Study"
            ),
        )

        self.plotter.set_background(
            "#11131A"
        )

        # ----------------------------------------------------
        # Actores por arquitectura
        # ----------------------------------------------------

        self.actors = {
            "H1": [],
            "H2": [],
            "H3": [],
            "H4": [],
        }

        # ----------------------------------------------------
        # Texto dinámico
        # ----------------------------------------------------

        self.info_actor = None

        # ----------------------------------------------------
        # Widgets
        # ----------------------------------------------------

        self.global_sliders = []
        self.parameter_sliders = []

        # ----------------------------------------------------
        # Construcción inicial
        # ----------------------------------------------------

        self.draw_all()

        self.add_global_controls()
        self.add_architecture_selector()
        self.add_parameter_controls()

        self.add_keyboard_shortcuts()

    # ========================================================
    # DIBUJAR TODO
    # ========================================================

    def draw_all(self):

        for index, architecture in enumerate(
            ("H1", "H2", "H3", "H4")
        ):

            self.draw_architecture(
                index,
                architecture,
            )

        self.update_info()

        self.plotter.render()

    # ========================================================
    # DIBUJAR UNA ARQUITECTURA
    # ========================================================

    def draw_architecture(
        self,
        index: int,
        architecture: str,
    ):

        row = index // 2
        col = index % 2

        self.plotter.subplot(
            row,
            col,
        )

        # ----------------------------------------------------
        # Eliminar actores anteriores
        # ----------------------------------------------------

        for actor in self.actors[
            architecture
        ]:

            try:

                self.plotter.remove_actor(
                    actor,
                    render=False,
                )

            except Exception:

                pass

        self.actors[
            architecture
        ] = []

        # ----------------------------------------------------
        # Carcasa
        # ----------------------------------------------------

        body = make_body(
            GLOBAL["explosion"]
        )

        body_actor = (
            self.plotter.add_mesh(
                body,
                color="lightgray",
                opacity=0.12,
                show_edges=True,
                line_width=1,
                name=(
                    f"{architecture}_body"
                ),
                render=False,
            )
        )

        self.actors[
            architecture
        ].append(
            body_actor
        )

        # ----------------------------------------------------
        # Componentes
        # ----------------------------------------------------

        components = BUILDERS[
            architecture
        ](
            GLOBAL["explosion"]
        )

        for part_index, (
            mesh,
            part_name,
            opacity,
        ) in enumerate(
            components
        ):

            if mesh is None:
                continue

            actor = self.plotter.add_mesh(
                mesh,
                color=ARCHITECTURE_COLORS[
                    architecture
                ][
                    part_name
                ],
                opacity=opacity,
                show_edges=True,
                line_width=1,
                name=(
                    f"{architecture}_"
                    f"{part_name}_{part_index}"
                ),
                render=False,
            )

            self.actors[
                architecture
            ].append(
                actor
            )

        # ----------------------------------------------------
        # Target
        # ----------------------------------------------------

        target = make_target(
            GLOBAL[
                "target_distance_mm"
            ],
            GLOBAL[
                "target_radius_mm"
            ],
        )

        target_actor = (
            self.plotter.add_mesh(
                target,
                color="gold",
                opacity=0.38,
                show_edges=True,
                line_width=1,
                name=(
                    f"{architecture}_target"
                ),
                render=False,
            )
        )

        self.actors[
            architecture
        ].append(
            target_actor
        )

        # ----------------------------------------------------
        # Título
        # ----------------------------------------------------

        title = {
            "H1": (
                "H1 · CENTRAL + "
                "AUXILIAR ANULAR"
            ),

            "H2": (
                "H2 · CENTRAL + "
                "GUARDA"
            ),

            "H3": (
                "H3 · CORE + SHIELD "
                "+ EXTERNO"
            ),

            "H4": (
                "H4 · ELECTRODOS "
                "AXIALES"
            ),
        }[architecture]

        self.plotter.add_text(
            title,
            position="upper_left",
            font_size=12,
            render=False,
        )

        # ----------------------------------------------------
        # Información propia
        # ----------------------------------------------------

        cproxy = (
            capacitance_proxy(
                architecture
            )
        )

        info = (
            f"Ø{SENSOR_DIAMETER_MM:.0f} × "
            f"{SENSOR_LENGTH_MM:.0f} mm\n"
            f"d = "
            f"{GLOBAL['target_distance_mm']:.1f} mm\n"
            f"V = "
            f"{GLOBAL['excitation_v']:.1f} V\n"
            f"C_proxy = "
            f"{cproxy:.3f} pF"
        )

        self.plotter.add_text(
            info,
            position="lower_left",
            font_size=9,
            render=False,
        )

        # ----------------------------------------------------
        # Cámara
        # ----------------------------------------------------

        self.plotter.view_isometric()

        self.plotter.reset_camera()

    # ========================================================
    # ACTUALIZAR TODO
    # ========================================================

    def refresh(self):

        self.draw_all()

    # ========================================================
    # SLIDERS GLOBALES
    # ========================================================

    def add_global_controls(self):

        # Distancia
        slider = self.plotter.add_slider_widget(
            self.on_target_distance,
            rng=(0.5, 30.0),
            value=GLOBAL[
                "target_distance_mm"
            ],
            title="Distancia objetivo d [mm]",
            pointa=(0.04, 0.035),
            pointb=(0.34, 0.035),
            interaction_event="always",
            fmt="%.1f",
        )

        self.global_sliders.append(
            slider
        )

        # Explosion
        slider = self.plotter.add_slider_widget(
            self.on_explosion,
            rng=(0.0, 1.0),
            value=GLOBAL[
                "explosion"
            ],
            title="Explosión",
            pointa=(0.37, 0.035),
            pointb=(0.55, 0.035),
            interaction_event="always",
            fmt="%.2f",
        )

        self.global_sliders.append(
            slider
        )

        # Voltaje
        slider = self.plotter.add_slider_widget(
            self.on_voltage,
            rng=(1.0, 100.0),
            value=GLOBAL[
                "excitation_v"
            ],
            title="Excitación V [V] — preparada para FEM",
            pointa=(0.58, 0.035),
            pointb=(0.94, 0.035),
            interaction_event="always",
            fmt="%.1f",
        )

        self.global_sliders.append(
            slider
        )

    # ========================================================
    # SELECTOR DE ARQUITECTURA
    # ========================================================

    def add_architecture_selector(self):

        base_x = 25
        base_y = 150

        positions = {
            "H1": (
                base_x,
                base_y + 180,
            ),

            "H2": (
                base_x,
                base_y + 120,
            ),

            "H3": (
                base_x,
                base_y + 60,
            ),

            "H4": (
                base_x,
                base_y,
            ),
        }

        for architecture in (
            "H1",
            "H2",
            "H3",
            "H4",
        ):

            self.plotter.add_radio_button_widget(
                callback=(
                    lambda checked,
                    arch=architecture:
                    self.select_architecture(
                        arch,
                        checked,
                    )
                ),
                radio_button_group=(
                    "architecture_selector"
                ),
                value=(
                    architecture
                    == "H1"
                ),
                position=positions[
                    architecture
                ],
                size=26,
                title=architecture,
                background_color="white",
            )

    def select_architecture(
        self,
        architecture: str,
        checked: bool,
    ):

        if not checked:
            return

        self.active_architecture = (
            architecture
        )

        self.sync_parameter_sliders()

        self.update_info()

    # ========================================================
    # SLIDERS DE PARÁMETROS
    # ========================================================

    def add_parameter_controls(self):

        # Tres sliders genéricos.
        # Su significado cambia según H1-H4 seleccionado.

        positions = [
            (
                0.68,
                0.26,
                0.96,
                0.26,
            ),

            (
                0.68,
                0.20,
                0.96,
                0.20,
            ),

            (
                0.68,
                0.14,
                0.96,
                0.14,
            ),
        ]

        for index in range(3):

            definition = (
                ACTIVE_PARAMETER_DEFINITION[
                    "H1"
                ][index]
            )

            _name, label, low, high, step = (
                definition
            )

            slider = self.plotter.add_slider_widget(
                lambda value, i=index:
                self.on_active_parameter(
                    i,
                    value,
                ),
                rng=(low, high),
                value=(
                    PARAMS["H1"][
                        _name
                    ]
                ),
                title=f"P{i+1}: {label}",
                pointa=(
                    positions[index][0],
                    positions[index][1],
                ),
                pointb=(
                    positions[index][2],
                    positions[index][3],
                ),
                interaction_event="always",
                fmt="%.2f",
            )

            self.parameter_sliders.append(
                slider
            )

    # ========================================================
    # SINCRONIZAR SLIDERS ACTIVOS
    # ========================================================

    def sync_parameter_sliders(self):

        definitions = (
            ACTIVE_PARAMETER_DEFINITION[
                self.active_architecture
            ]
        )

        for index, slider in enumerate(
            self.parameter_sliders
        ):

            parameter, label, low, high, step = (
                definitions[index]
            )

            representation = (
                slider.GetRepresentation()
            )

            representation.SetMinimumValue(
                low
            )

            representation.SetMaximumValue(
                high
            )

            representation.SetValue(
                PARAMS[
                    self.active_architecture
                ][parameter]
            )

            # Cambiar el título del slider.
            try:

                representation.SetTitleText(
                    f"P{index + 1}: {label}"
                )

            except Exception:

                pass

        self.plotter.render()

    # ========================================================
    # CALLBACK DE PARÁMETRO
    # ========================================================

    def on_active_parameter(
        self,
        index: int,
        value: float,
    ):

        definitions = (
            ACTIVE_PARAMETER_DEFINITION[
                self.active_architecture
            ]
        )

        parameter = definitions[
            index
        ][0]

        PARAMS[
            self.active_architecture
        ][parameter] = float(
            value
        )

        self.refresh()

        self.sync_parameter_sliders()

    # ========================================================
    # CALLBACKS GLOBALES
    # ========================================================

    def on_target_distance(
        self,
        value: float,
    ):

        GLOBAL[
            "target_distance_mm"
        ] = float(value)

        self.refresh()

    def on_explosion(
        self,
        value: float,
    ):

        GLOBAL[
            "explosion"
        ] = float(value)

        self.refresh()

    def on_voltage(
        self,
        value: float,
    ):

        GLOBAL[
            "excitation_v"
        ] = float(value)

        # Por ahora solo cambia el indicador.
        self.refresh()

    # ========================================================
    # INFORMACIÓN SUPERIOR
    # ========================================================

    def update_info(self):

        # Un texto general único.
        if self.info_actor is not None:

            try:

                self.plotter.remove_actor(
                    self.info_actor,
                    render=False,
                )

            except Exception:

                pass

        definitions = (
            ACTIVE_PARAMETER_DEFINITION[
                self.active_architecture
            ]
        )

        text_lines = [
            (
                "MODELO PARAMÉTRICO — "
                f"ARQUITECTURA ACTIVA: "
                f"{self.active_architecture}"
            ),

            "H1–H4 = modelos candidatos; "
            "interior comercial no confirmado.",

        ]

        for i, (
            parameter,
            label,
            _low,
            _high,
            _step,
        ) in enumerate(
            definitions
        ):

            value = PARAMS[
                self.active_architecture
            ][parameter]

            text_lines.append(
                f"P{i + 1}: "
                f"{label} = "
                f"{value:.2f}"
            )

        self.info_actor = (
            self.plotter.add_text(
                "\n".join(
                    text_lines
                ),
                position="upper_right",
                font_size=9,
                render=False,
            )
        )

        self.plotter.render()

    # ========================================================
    # TECLAS RÁPIDAS
    # ========================================================

    def add_keyboard_shortcuts(self):

        self.plotter.add_key_event(
            "1",
            lambda:
            self.select_architecture(
                "H1",
                True,
            ),
        )

        self.plotter.add_key_event(
            "2",
            lambda:
            self.select_architecture(
                "H2",
                True,
            ),
        )

        self.plotter.add_key_event(
            "3",
            lambda:
            self.select_architecture(
                "H3",
                True,
            ),
        )

        self.plotter.add_key_event(
            "4",
            lambda:
            self.select_architecture(
                "H4",
                True,
            ),
        )

    # ========================================================
    # EJECUCIÓN
    # ========================================================

    def show(self):

        self.plotter.show(
            interactive=True,
            auto_close=True,
        )


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    study = M18Study()

    study.show()
