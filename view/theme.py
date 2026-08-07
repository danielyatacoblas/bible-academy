"""
Sistema de diseño de la aplicación.

Centraliza la paleta de colores, la tipografía, el espaciado y los radios de
borde para que login, dashboard, diálogos y gráficos compartan un mismo
lenguaje visual. Los módulos de interfaz deben importar estas constantes en
lugar de escribir valores literales.
"""

import customtkinter as ctk
from tkinter import ttk

# --------------------------------------------------------------------------
# Paleta
# --------------------------------------------------------------------------

# Marca (azul institucional)
PRIMARY = "#1f538d"
PRIMARY_DARK = "#17416f"
PRIMARY_LIGHT = "#2f6cae"
PRIMARY_SOFT = "#eaf1f8"

# Estados
SUCCESS = "#2f8f5b"
SUCCESS_DARK = "#26744a"
SUCCESS_SOFT = "#e8f4ee"

WARNING = "#d99a1f"
WARNING_DARK = "#b8811a"
WARNING_SOFT = "#fdf3e0"

DANGER = "#c0392b"
DANGER_DARK = "#a03225"
DANGER_SOFT = "#fbeceb"

INFO = "#2f6cae"
INFO_DARK = "#245a94"

ACCENT = "#6b5bb5"
ACCENT_DARK = "#584a99"

NEUTRAL = "#64748b"
NEUTRAL_DARK = "#4d5b6d"

# Superficies y texto
SURFACE = "#ffffff"
SURFACE_ALT = "#f7f9fc"
BACKGROUND = "#eef2f7"
BORDER = "#d8e0e9"

TEXT = "#1f2a37"
TEXT_MUTED = "#5b6b7c"
TEXT_ON_DARK = "#ffffff"
TEXT_ON_PRIMARY_MUTED = "#c3d6ec"

# Barra lateral
SIDEBAR_BG = PRIMARY
SIDEBAR_ACTIVE = PRIMARY_DARK
SIDEBAR_HOVER = PRIMARY_DARK

# --------------------------------------------------------------------------
# Gráficos
# --------------------------------------------------------------------------

CHART_PALETTE = [
    PRIMARY_LIGHT,
    SUCCESS,
    WARNING,
    DANGER,
    ACCENT,
    "#2aa8a0",
    "#d9762f",
    "#a6538a",
]

CHART_FACE = SURFACE
CHART_PLOT_FACE = SURFACE_ALT
CHART_GRID = "#dbe3ec"
CHART_TITLE = PRIMARY
CHART_LABEL = TEXT_MUTED
CHART_TICK = TEXT_MUTED
CHART_SPINE = BORDER

CHART_TITLE_SIZE = 13
CHART_LABEL_SIZE = 10
CHART_TICK_SIZE = 9
CHART_VALUE_SIZE = 9

# --------------------------------------------------------------------------
# Tipografía
# --------------------------------------------------------------------------

FONT_FAMILY = "Segoe UI"
FONT_FAMILY_TABLE = "Segoe UI"

SIZE_DISPLAY = 26
SIZE_TITLE = 20
SIZE_SECTION = 17
SIZE_SUBTITLE = 15
SIZE_BODY = 13
SIZE_SMALL = 12
SIZE_CAPTION = 11
SIZE_METRIC = 32


def font(size=SIZE_BODY, weight="normal"):
    """Crear una fuente de la aplicación con la familia tipográfica común."""
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight=weight)


# --------------------------------------------------------------------------
# Espaciado y radios
# --------------------------------------------------------------------------

SPACE_XS = 4
SPACE_SM = 8
SPACE_MD = 16
SPACE_LG = 24
SPACE_XL = 32

RADIUS_SM = 6
RADIUS_MD = 10
RADIUS_LG = 14

# --------------------------------------------------------------------------
# Estilo de tablas (ttk.Treeview)
# --------------------------------------------------------------------------

ROW_HEIGHT = 36


def apply_treeview_style():
    """Aplicar un estilo consistente a todos los ttk.Treeview de la app."""
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(
        "Treeview",
        background=SURFACE,
        foreground=TEXT,
        fieldbackground=SURFACE,
        rowheight=ROW_HEIGHT,
        borderwidth=0,
        font=(FONT_FAMILY_TABLE, SIZE_SMALL),
    )
    style.configure(
        "Treeview.Heading",
        background=PRIMARY,
        foreground=TEXT_ON_DARK,
        relief="flat",
        padding=(8, 8),
        font=(FONT_FAMILY_TABLE, SIZE_CAPTION, "bold"),
    )
    style.map(
        "Treeview.Heading",
        background=[("active", PRIMARY_DARK)],
        foreground=[("active", TEXT_ON_DARK)],
    )
    style.map(
        "Treeview",
        background=[("selected", PRIMARY_SOFT)],
        foreground=[("selected", TEXT)],
    )
    style.configure(
        "Vertical.TScrollbar",
        background=BORDER,
        troughcolor=SURFACE_ALT,
        bordercolor=SURFACE_ALT,
        arrowcolor=TEXT_MUTED,
    )
    return style


def tag_treeview_rows(tree):
    """Configurar el rayado y los estados de fila de un Treeview."""
    tree.tag_configure("odd", background=SURFACE)
    tree.tag_configure("even", background=SURFACE_ALT)
    tree.tag_configure("activo", background=SUCCESS_SOFT)
    tree.tag_configure("inactivo", background=SURFACE_ALT)
