"""Ventana que agrupa las salidas del análisis léxico."""

import os
import tkinter as tk
from tkinter import ttk

from .estilos import COLORES, crear_superficie
from .tabla_errores import TablaErrores
from .tabla_simbolos import TablaSimbolos
from .tira_tokens import TiraTokens


class VentanaResultados(tk.Toplevel):
    def __init__(self, padre, ruta, tokens, errores):
        super().__init__(padre)
        self.title("Resultados del análisis léxico")
        self.geometry("980x650")
        self.minsize(760, 480)
        self.configure(bg=COLORES["fondo"])
        self.transient(padre)

        cabecera = tk.Frame(self, bg=COLORES["fondo"])
        cabecera.pack(fill="x", padx=28, pady=(24, 14))
        tk.Label(
            cabecera, text="Resultados del análisis léxico",
            font=("Segoe UI", 21, "bold"), bg=COLORES["fondo"],
            fg=COLORES["texto"],
        ).pack(anchor="w")
        tk.Label(
            cabecera, text=os.path.basename(ruta),
            font=("Segoe UI", 10), bg=COLORES["fondo"],
            fg=COLORES["secundario"],
        ).pack(anchor="w", pady=(4, 0))

        resumen = crear_superficie(self)
        resumen.pack(fill="x", padx=28, pady=(0, 14))
        tk.Label(
            resumen, text=f"{len(tokens)} tokens",
            font=("Segoe UI", 10, "bold"), bg=COLORES["superficie"],
            fg=COLORES["exito"],
        ).pack(side="left", padx=16, pady=12)
        tk.Label(
            resumen, text=f"{len(errores)} errores",
            font=("Segoe UI", 10, "bold"), bg=COLORES["superficie"],
            fg=COLORES["error"],
        ).pack(side="left", padx=12, pady=12)

        cuerpo = crear_superficie(self)
        cuerpo.pack(fill="both", expand=True, padx=28, pady=(0, 24))
        pestañas = ttk.Notebook(cuerpo)
        pestañas.pack(fill="both", expand=True, padx=12, pady=12)

        pestaña_tokens = tk.Frame(pestañas, bg=COLORES["superficie"])
        pestaña_simbolos = tk.Frame(pestañas, bg=COLORES["superficie"])
        pestaña_errores = tk.Frame(pestañas, bg=COLORES["superficie"])
        pestañas.add(pestaña_tokens, text="  1. Tira de tokens  ")
        pestañas.add(pestaña_simbolos, text="  2. Tabla de símbolos  ")
        pestañas.add(pestaña_errores, text="  3. Tabla de errores  ")

        TiraTokens(pestaña_tokens).pack(fill="both", expand=True, padx=8, pady=8)
        TablaSimbolos(pestaña_simbolos).pack(fill="both", expand=True, padx=8, pady=8)
        TablaErrores(pestaña_errores).pack(fill="both", expand=True, padx=8, pady=8)

        # Se crean referencias para cargar los datos después de construir las pestañas.
        self.tira_tokens = pestaña_tokens.winfo_children()[0]
        self.tabla_simbolos = pestaña_simbolos.winfo_children()[0]
        self.tabla_errores = pestaña_errores.winfo_children()[0]
        self.tira_tokens.mostrar(tokens)
        self.tabla_simbolos.mostrar(tokens)
        self.tabla_errores.mostrar(errores)
