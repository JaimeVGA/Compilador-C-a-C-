"""Presentación de la tira de tokens."""

import tkinter as tk

from .estilos import COLORES
from .tabla_base import crear_tabla


class TiraTokens(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, bg=COLORES["superficie"])
        marco, self.tabla = crear_tabla(
            self, ("linea", "lexema", "token"),
            ("# línea", "Lexema", "Token"), (90, 360, 220), 18,
        )
        marco.pack(fill="both", expand=True)

    def mostrar(self, tokens):
        self.tabla.delete(*self.tabla.get_children())
        for token in tokens:
            self.tabla.insert(
                "", tk.END,
                values=(token.renglon, token.lexema, token.tipo),
            )
