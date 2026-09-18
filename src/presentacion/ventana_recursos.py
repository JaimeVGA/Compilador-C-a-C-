"""Ventana con los recursos del analizador léxico."""

import sys
import tkinter as tk
from tkinter import ttk

from ..modelos.tokens import PALABRAS_RESERVADAS
from .estilos import COLORES, crear_superficie


_ALFABETO = (
    ("Letras", "a-z, A-Z"),
    ("Dígitos", "0-9"),
    ("Identificadores", "_"),
    ("Operadores", "=  ==  =>  ->  +  ++  +=  -  --  -=  *  *=  /  /="
                   "  %  %=  &  &&  |  ||  ^  ^=  <  <=  >  >=  !  ~  ?  :"),
    ("Delimitadores", "{  }  (  )  [  ]  ;  ,  ."),
    ("Espacios", "espacio, tabulación, salto de línea y retorno de carro"),
)


class VentanaRecursos(tk.Toplevel):
    """Muestra el alfabeto y las palabras reservadas reconocidas."""

    def __init__(self, padre):
        super().__init__(padre)
        self.title("Recursos del analizador léxico")
        self.geometry("900x650")
        self.minsize(700, 480)
        self.resizable(True, True)
        self.configure(bg=COLORES["fondo"])
        if sys.platform == "win32":
            self.wm_attributes("-toolwindow", False)

        cabecera = tk.Frame(self, bg=COLORES["fondo"])
        cabecera.pack(fill="x", padx=28, pady=(24, 14))
        tk.Label(
            cabecera, text="Recursos del analizador léxico",
            font=("Segoe UI", 21, "bold"), bg=COLORES["fondo"],
            fg=COLORES["texto"],
        ).pack(anchor="w")
        tk.Label(
            cabecera,
            text="Elementos que puede reconocer el analizador.",
            font=("Segoe UI", 10), bg=COLORES["fondo"],
            fg=COLORES["secundario"],
        ).pack(anchor="w", pady=(4, 0))

        cuerpo = crear_superficie(self)
        cuerpo.pack(fill="both", expand=True, padx=28, pady=(0, 24))
        pestañas = ttk.Notebook(cuerpo)
        pestañas.pack(fill="both", expand=True, padx=12, pady=12)

        pestaña_alfabeto = tk.Frame(pestañas, bg=COLORES["superficie"])
        pestaña_reservadas = tk.Frame(pestañas, bg=COLORES["superficie"])
        pestañas.add(pestaña_alfabeto, text="  Alfabeto  ")
        pestañas.add(pestaña_reservadas, text="  Palabras reservadas  ")

        self._crear_tabla_alfabeto(pestaña_alfabeto)
        self._crear_lista_reservadas(pestaña_reservadas)

    def _crear_tabla_alfabeto(self, padre):
        marco = tk.Frame(padre, bg=COLORES["superficie"])
        marco.pack(fill="both", expand=True, padx=12, pady=12)
        tabla = ttk.Treeview(
            marco, columns=("categoria", "elementos"),
            show="headings", selectmode="browse",
        )
        tabla.heading("categoria", text="Categoría")
        tabla.heading("elementos", text="Elementos")
        tabla.column("categoria", width=170, minwidth=130, anchor="w")
        tabla.column("elementos", width=600, minwidth=300, anchor="w")
        scroll = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        for categoria, elementos in _ALFABETO:
            tabla.insert("", "end", values=(categoria, elementos))
        tabla.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

    def _crear_lista_reservadas(self, padre):
        marco = tk.Frame(padre, bg=COLORES["superficie"])
        marco.pack(fill="both", expand=True, padx=12, pady=12)
        lista = tk.Listbox(
            marco, bg=COLORES["superficie_alt"],
            fg=COLORES["texto"], selectbackground="#4338ca",
            relief="flat", borderwidth=0, font=("Consolas", 11),
        )
        scroll = ttk.Scrollbar(marco, orient="vertical", command=lista.yview)
        lista.configure(yscrollcommand=scroll.set)
        for palabra in sorted(PALABRAS_RESERVADAS):
            lista.insert(tk.END, palabra)
        lista.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=8)
        scroll.grid(row=0, column=1, sticky="ns", padx=(0, 8), pady=8)
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
