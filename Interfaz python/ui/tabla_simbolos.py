"""Presentación de la tabla de símbolos/identificadores."""

import tkinter as tk

from .estilos import COLORES
from .tabla_base import crear_tabla


class TablaSimbolos(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, bg=COLORES["superficie"])
        tk.Label(
            self, text="Listado de la tabla de símbolos o identificadores",
            font=("Segoe UI", 11, "bold"), bg=COLORES["superficie"],
            fg=COLORES["texto"],
        ).pack(fill="x", padx=8, pady=(4, 10))
        marco, self.tabla = crear_tabla(
            self, ("numero", "identificador"),
            ("#Id", "Nombre del identificador"), (90, 520), 16,
        )
        marco.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def mostrar(self, tokens):
        self.tabla.delete(*self.tabla.get_children())
        vistos = set()
        for token in tokens:
            if token.tipo == "id":
                self._agregar_si_nuevo(token.lexema, vistos)

    def _agregar_si_nuevo(self, identificador, vistos):
        if identificador in vistos:
            return
        vistos.add(identificador)
        numero = len(vistos)
        self.tabla.insert("", tk.END, values=(numero, identificador))
