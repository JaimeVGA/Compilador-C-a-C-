"""Punto de entrada de la interfaz gráfica del compilador."""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

_SRC_DIR = os.path.dirname(__file__)
_ROOT_DIR = os.path.dirname(_SRC_DIR)
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

from src.persistencia.lector_archivo import LectorArchivo
from src.persistencia.manejador_errores import ManejadorErrores
from src.persistencia.reconocedor_tokens import ReconocedorTokens
from src.presentacion.estilos import COLORES, configurar_estilos, crear_superficie
from src.presentacion.ventana_recursos import VentanaRecursos
from src.presentacion.ventana_resultados import VentanaResultados


class AplicacionAnalizador(tk.Tk):
    """Ventana principal para cargar el archivo y lanzar el análisis."""

    def __init__(self):
        super().__init__()
        self.archivo_actual = ""
        self.ventana_resultados = None
        self.ventana_recursos = None
        self.title("Compilador C# a C++ · Analizador léxico")
        self.geometry("1180x760")
        self.minsize(900, 600)
        self.resizable(True, True)
        self.configure(bg=COLORES["fondo"])
        configurar_estilos(self)
        self._crear_interfaz()

    def _crear_interfaz(self):
        cabecera = tk.Frame(self, bg=COLORES["fondo"])
        cabecera.pack(fill="x", padx=34, pady=(26, 14))
        tk.Label(
            cabecera, text="Analizador léxico",
            font=("Segoe UI", 24, "bold"), bg=COLORES["fondo"],
            fg=COLORES["texto"],
        ).pack(anchor="w")
        tk.Label(
            cabecera, text="Analiza un programa C# y consulta su tira de tokens, símbolos y errores.",
            font=("Segoe UI", 11), bg=COLORES["fondo"],
            fg=COLORES["secundario"],
        ).pack(anchor="w", pady=(4, 0))

        controles = crear_superficie(self)
        controles.pack(fill="x", padx=34, pady=(0, 18))
        self.ruta_var = tk.StringVar(value="Ningún archivo seleccionado")
        tk.Label(
            controles, textvariable=self.ruta_var, anchor="w",
            font=("Segoe UI", 10), bg=COLORES["superficie"],
            fg=COLORES["secundario"],
        ).pack(side="left", fill="x", expand=True, padx=16, pady=12)
        ttk.Button(
            controles, text="Analizar", style="Accent.TButton",
            command=self.analizar_archivo,
        ).pack(side="right", padx=(4, 8), pady=8)
        ttk.Button(
            controles, text="Cargar archivo", command=self.cargar_archivo,
        ).pack(side="right", padx=8, pady=8)
        ttk.Button(
            controles, text="Recursos", command=self.mostrar_recursos,
        ).pack(side="right", padx=(8, 4), pady=8)

        panel_codigo = crear_superficie(self)
        panel_codigo.pack(fill="both", expand=True, padx=34, pady=(0, 14))
        tk.Label(
            panel_codigo, text="Programa fuente (Cualquier cambio que se realice aqui no se reflejara en el análisis, solo es un previsualizador)", anchor="w",
            font=("Segoe UI", 12, "bold"), bg=COLORES["superficie"],
            fg=COLORES["texto"],
        ).pack(fill="x", padx=16, pady=(14, 8))
        self._crear_editor(panel_codigo)

        self.estado_var = tk.StringVar(value="Listo para analizar un archivo.")
        tk.Label(
            self, textvariable=self.estado_var, anchor="w",
            font=("Segoe UI", 9), bg=COLORES["fondo"],
            fg=COLORES["secundario"],
        ).pack(fill="x", padx=36, pady=(0, 14))

    def _crear_editor(self, padre):
        contenedor = tk.Frame(padre, bg=COLORES["superficie"])
        contenedor.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.numeros_linea = tk.Text(
            contenedor, width=5, wrap="none", state="disabled",
            font=("Consolas", 10), bg=COLORES["superficie_alt"],
            fg=COLORES["secundario"], relief="flat", padx=6, pady=10,
            takefocus=0,
        )
        self.codigo = tk.Text(
            contenedor, wrap="none", undo=False, font=("Consolas", 10),
            bg=COLORES["superficie_alt"], fg=COLORES["texto"],
            insertbackground=COLORES["texto"],
            relief="flat", padx=12, pady=10,
        )
        scroll_y = ttk.Scrollbar(contenedor, orient="vertical", command=self._scroll_vertical)
        scroll_x = ttk.Scrollbar(contenedor, orient="horizontal", command=self.codigo.xview)
        self.codigo.configure(
            yscrollcommand=lambda a, b: self._actualizar_scroll(a, b, scroll_y),
            xscrollcommand=scroll_x.set,
        )
        self.numeros_linea.grid(row=0, column=0, sticky="ns")
        self.codigo.grid(row=0, column=1, sticky="nsew")
        scroll_y.grid(row=0, column=2, sticky="ns")
        scroll_x.grid(row=1, column=1, sticky="ew")
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)
        self.codigo.bind("<KeyRelease>", self._actualizar_numeros_linea)
        self._actualizar_numeros_linea()

    def _scroll_vertical(self, *args):
        self.codigo.yview(*args)
        self.numeros_linea.yview(*args)

    def _actualizar_scroll(self, primero, ultimo, scroll):
        scroll.set(primero, ultimo)
        self.numeros_linea.yview_moveto(primero)

    def _actualizar_numeros_linea(self, _event=None):
        total = int(self.codigo.index("end-1c").split(".")[0])
        contenido = "\n".join(str(linea) for linea in range(1, total + 1))
        self.numeros_linea.configure(state="normal")
        self.numeros_linea.delete("1.0", tk.END)
        self.numeros_linea.insert("1.0", contenido)
        self.numeros_linea.configure(state="disabled")

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo C#",
            filetypes=(("Archivos C#", "*.cs"), ("Todos los archivos", "*.*")),
        )
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
        except (OSError, UnicodeError) as error:
            messagebox.showerror("No se pudo cargar el archivo", str(error))
            return
        self.archivo_actual = ruta
        self.ruta_var.set(ruta)
        self.codigo.delete("1.0", tk.END)
        self.codigo.insert("1.0", contenido)
        self._actualizar_numeros_linea()
        self.estado_var.set("Archivo cargado. Presiona «Analizar» para comenzar.")

    def analizar_archivo(self):
        if not self.archivo_actual:
            messagebox.showinfo("Archivo requerido", "Primero selecciona un archivo C#.")
            return
        try:
            lector = LectorArchivo()
            lector.leer_archivo(self.archivo_actual)
            manejador = ManejadorErrores()
            tokens = ReconocedorTokens(lector, manejador).analizar()
        except (OSError, UnicodeError, ValueError) as error:
            messagebox.showerror("Error durante el análisis", str(error))
            return
        errores = manejador.obtener_errores()
        if self.ventana_resultados and self.ventana_resultados.winfo_exists():
            self.ventana_resultados.destroy()
        self.ventana_resultados = VentanaResultados(
            self, self.archivo_actual, tokens, errores
        )
        self.estado_var.set(
            f"Análisis terminado: {len(tokens)} tokens y {len(errores)} errores."
        )

    def mostrar_recursos(self):
        if self.ventana_recursos and self.ventana_recursos.winfo_exists():
            self.ventana_recursos.deiconify()
            self.ventana_recursos.lift()
            self.ventana_recursos.focus_force()
            return
        self.ventana_recursos = VentanaRecursos(self)

if __name__ == "__main__":
    AplicacionAnalizador().mainloop()
