"""Presentación de errores léxicos."""

import tkinter as tk

from .estilos import COLORES
from .tabla_base import crear_tabla


class TablaErrores(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, bg=COLORES["superficie"])
        marco, self.tabla = crear_tabla(
            self, ("linea", "descripcion"),
            ("# línea", "Descripción del error"), (90, 680), 12,
        )
        self.tabla.tag_configure("error", foreground=COLORES["error"])
        marco.pack(fill="both", expand=True)

    def mostrar(self, errores):
        self.tabla.delete(*self.tabla.get_children())
        for error in errores:
            self.tabla.insert(
                "", tk.END, values=(error.renglon, str(error)),
                tags=("error",),
            )
