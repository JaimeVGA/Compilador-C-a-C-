"""Paleta y estilos compartidos por los componentes de la interfaz."""

import tkinter as tk
from tkinter import ttk


COLORES = {
    "fondo": "#111827",
    "superficie": "#1f2937",
    "superficie_alt": "#273449",
    "texto": "#f3f4f6",
    "secundario": "#9ca3af",
    "primario": "#6366f1",
    "primario_hover": "#818cf8",
    "borde": "#374151",
    "error": "#f87171",
    "error_fondo": "#3f1d2e",
    "exito": "#34d399",
}


def configurar_estilos(ventana):
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure(
        "TButton", font=("Segoe UI", 10), padding=(14, 8),
        background=COLORES["superficie"], foreground=COLORES["texto"],
        bordercolor=COLORES["borde"],
    )
    estilo.configure(
        "Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(16, 9),
        background=COLORES["primario"], foreground="white", borderwidth=0,
    )
    estilo.map("Accent.TButton", background=[("active", COLORES["primario_hover"])])
    estilo.configure(
        "Treeview", background=COLORES["superficie_alt"], fieldbackground=COLORES["superficie_alt"],
        foreground=COLORES["texto"], rowheight=28, font=("Segoe UI", 10),
        bordercolor=COLORES["borde"],
    )
    estilo.configure(
        "Treeview.Heading", background="#374151",
        foreground=COLORES["texto"], font=("Segoe UI", 10, "bold"), padding=8,
    )
    estilo.map("Treeview", background=[("selected", "#4338ca")])
    estilo.configure("TNotebook", background=COLORES["superficie"], borderwidth=0)
    estilo.configure("TNotebook.Tab", padding=(18, 10), font=("Segoe UI", 10, "bold"))


def crear_superficie(padre):
    return tk.Frame(
        padre, bg=COLORES["superficie"], highlightthickness=1,
        highlightbackground=COLORES["borde"],
    )
