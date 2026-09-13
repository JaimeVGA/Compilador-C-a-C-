"""Interfaz gráfica para ejecutar el análisis léxico del compilador."""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


MODULOS_DIR = os.path.join(os.path.dirname(__file__), "Modulos")
if MODULOS_DIR not in sys.path:
    sys.path.insert(0, MODULOS_DIR)

from lector_archivo import LectorArchivo
from manejador_errores import ManejadorErrores
from reconocedor_tokens import ReconocedorTokens
from tokens import PALABRAS_RESERVADAS


class AplicacionAnalizador(tk.Tk):
    """Ventana principal del analizador léxico."""

    COLORES = {
        "fondo": "#111827",
        "panel": "#1f2937",
        "panel_alt": "#273449",
        "texto": "#f3f4f6",
        "secundario": "#9ca3af",
        "primario": "#6366f1",
        "primario_hover": "#818cf8",
        "borde": "#374151",
        "error": "#f87171",
        "error_fondo": "#3f1d2e",
        "exito": "#34d399",
    }

    def __init__(self):
        super().__init__()
        self.archivo_actual = ""
        self.ventana_resultados = None
        self._configurar_ventana()
        self._configurar_estilos()
        self._crear_interfaz()

    def _configurar_ventana(self):
        self.title("Analizador léxico · C# a C++")
        self.geometry("1180x760")
        self.minsize(900, 600)
        self.configure(bg=self.COLORES["fondo"])

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=(14, 8),
            background=self.COLORES["panel"],
            foreground=self.COLORES["texto"],
            bordercolor=self.COLORES["borde"],
        )
        estilo.configure(
            "Accent.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 9),
            background=self.COLORES["primario"],
            foreground="white",
            borderwidth=0,
        )
        estilo.map("Accent.TButton", background=[
            ("active", self.COLORES["primario_hover"])
        ])
        estilo.configure(
            "Treeview",
            background=self.COLORES["panel_alt"],
            fieldbackground=self.COLORES["panel_alt"],
            foreground=self.COLORES["texto"],
            rowheight=29,
            font=("Segoe UI", 10),
            borderwidth=0,
        )
        estilo.configure(
            "Treeview.Heading",
            background="#374151",
            foreground=self.COLORES["texto"],
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )
        estilo.map("Treeview", background=[("selected", "#4338ca")])

    def _crear_interfaz(self):
        encabezado = tk.Frame(self, bg=self.COLORES["fondo"])
        encabezado.pack(fill="x", padx=32, pady=(26, 12))

        tk.Label(
            encabezado,
            text="Analizador léxico",
            font=("Segoe UI", 24, "bold"),
            bg=self.COLORES["fondo"],
            fg=self.COLORES["texto"],
        ).pack(anchor="w")
        tk.Label(
            encabezado,
            text="Carga un archivo C# para identificar tokens y errores léxicos.",
            font=("Segoe UI", 11),
            bg=self.COLORES["fondo"],
            fg=self.COLORES["secundario"],
        ).pack(anchor="w", pady=(4, 0))

        barra = tk.Frame(self, bg=self.COLORES["panel"], highlightthickness=1,
                         highlightbackground=self.COLORES["borde"])
        barra.pack(fill="x", padx=32, pady=(0, 16))

        self.ruta_var = tk.StringVar(value="Ningún archivo seleccionado")
        tk.Label(
            barra,
            textvariable=self.ruta_var,
            anchor="w",
            font=("Segoe UI", 10),
            bg=self.COLORES["panel"],
            fg=self.COLORES["secundario"],
        ).pack(side="left", fill="x", expand=True, padx=16, pady=12)
        ttk.Button(
            barra, text="Cargar archivo", command=self.cargar_archivo
        ).pack(side="right", padx=(4, 8), pady=8)
        ttk.Button(
            barra, text="Analizar", style="Accent.TButton",
            command=self.analizar_archivo
        ).pack(side="right", padx=8, pady=8)

        contenido = tk.PanedWindow(
            self, orient=tk.HORIZONTAL, sashwidth=7, bg=self.COLORES["fondo"],
            bd=0, relief="flat"
        )
        contenido.pack(fill="both", expand=True, padx=32, pady=(0, 16))

        panel_codigo = self._crear_panel(contenido, "Código fuente cargado")
        contenido.add(panel_codigo, minsize=600, stretch="always")

        self.codigo = self._crear_texto(panel_codigo, "#111827")

        self.estado_var = tk.StringVar(value="Listo para analizar un archivo.")
        tk.Label(
            self, textvariable=self.estado_var, anchor="w",
            font=("Segoe UI", 9), bg=self.COLORES["fondo"],
            fg=self.COLORES["secundario"]
        ).pack(fill="x", padx=34, pady=(0, 14))

    def _crear_panel(self, padre, titulo):
        panel = tk.Frame(
            padre, bg=self.COLORES["panel"], highlightthickness=1,
            highlightbackground=self.COLORES["borde"]
        )
        tk.Label(
            panel, text=titulo, anchor="w", font=("Segoe UI", 12, "bold"),
            bg=self.COLORES["panel"], fg=self.COLORES["texto"]
        ).pack(fill="x", padx=16, pady=(14, 8))
        return panel

    def _crear_texto(self, padre, fondo):
        contenedor = tk.Frame(padre, bg=self.COLORES["panel"])
        contenedor.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        texto = tk.Text(
            contenedor, wrap="none", undo=False, font=("Consolas", 10),
            bg=fondo, fg=self.COLORES["texto"], insertbackground=self.COLORES["texto"],
            relief="flat", padx=12, pady=10
        )
        scroll_y = ttk.Scrollbar(contenedor, orient="vertical", command=texto.yview)
        scroll_x = ttk.Scrollbar(contenedor, orient="horizontal", command=texto.xview)
        texto.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        texto.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)
        return texto

    def _crear_resultados(self, padre):
        contenedor = tk.Frame(padre, bg=self.COLORES["panel"])
        contenedor.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.tokens = self._crear_tabla(
            contenedor, ("tipo", "lexema", "renglon", "columna"),
            ("Tipo", "Lexema", "Renglón", "Columna"),
            (150, 230, 85, 85)
        )
        self.errores = self._crear_tabla(
            contenedor, ("mensaje", "renglon", "columna"),
            ("Error léxico", "Renglón", "Columna"),
            (360, 85, 85)
        )
        self.errores.tag_configure("error", foreground=self.COLORES["error"])
        self._crear_contadores(contenedor)

    def _abrir_ventana_resultados(self, tokens, errores):
        if self.ventana_resultados is not None and self.ventana_resultados.winfo_exists():
            self.ventana_resultados.destroy()

        ventana = tk.Toplevel(self)
        self.ventana_resultados = ventana
        ventana.title("Análisis léxico · resultados")
        ventana.geometry("1050x680")
        ventana.minsize(800, 500)
        ventana.configure(bg=self.COLORES["fondo"])
        ventana.transient(self)

        encabezado = tk.Frame(ventana, bg=self.COLORES["fondo"])
        encabezado.pack(fill="x", padx=26, pady=(22, 12))
        tk.Label(
            encabezado, text="Resultado del análisis léxico",
            font=("Segoe UI", 20, "bold"), bg=self.COLORES["fondo"],
            fg=self.COLORES["texto"]
        ).pack(anchor="w")
        tk.Label(
            encabezado, text=os.path.basename(self.archivo_actual),
            font=("Segoe UI", 10), bg=self.COLORES["fondo"],
            fg=self.COLORES["secundario"]
        ).pack(anchor="w", pady=(3, 0))

        resumen = tk.Frame(
            ventana, bg=self.COLORES["panel"], highlightthickness=1,
            highlightbackground=self.COLORES["borde"]
        )
        resumen.pack(fill="x", padx=26, pady=(0, 14))
        tk.Label(
            resumen, text="Desglose del análisis", anchor="w",
            font=("Segoe UI", 11, "bold"), bg=self.COLORES["panel"],
            fg=self.COLORES["texto"]
        ).pack(side="left", padx=16, pady=14)
        tk.Label(
            resumen, text=f"{len(tokens)} tokens", font=("Segoe UI", 11, "bold"),
            bg=self.COLORES["panel"], fg=self.COLORES["exito"]
        ).pack(side="right", padx=(8, 16), pady=14)
        tk.Label(
            resumen, text=f"{len(errores)} errores", font=("Segoe UI", 11, "bold"),
            bg=self.COLORES["panel"], fg=self.COLORES["error"]
        ).pack(side="right", padx=8, pady=14)

        cuerpo = tk.Frame(ventana, bg=self.COLORES["panel"])
        cuerpo.pack(fill="both", expand=True, padx=26, pady=(0, 24))
        pestañas = ttk.Notebook(cuerpo)
        pestañas.pack(fill="both", expand=True, padx=14, pady=14)
        pestaña_lexemas = tk.Frame(pestañas, bg=self.COLORES["panel"])
        pestaña_analisis = tk.Frame(pestañas, bg=self.COLORES["panel"])
        pestaña_errores = tk.Frame(pestañas, bg=self.COLORES["panel"])
        pestañas.add(pestaña_lexemas, text="  Tira de tokens  ")
        pestañas.add(pestaña_analisis, text="  Análisis léxico  ")
        pestañas.add(pestaña_errores, text="  Tabla de errores  ")

        tabla_lexemas = self._crear_tabla(
            pestaña_lexemas, ("lexema", "token"),
            ("Lexema", "Token"), (600, 300)
        )
        self.tokens = self._crear_tabla(
            pestaña_analisis, ("tipo", "lexema", "renglon", "columna"),
            ("Tipo", "Lexema", "Renglón", "Columna"), (170, 450, 90, 90)
        )
        self.errores = self._crear_tabla(
            pestaña_errores, ("mensaje", "renglon", "columna"),
            ("Error léxico", "Renglón", "Columna"), (500, 90, 90)
        )
        self.errores.tag_configure("error", foreground=self.COLORES["error"])
        self._mostrar_tabla_lexemas(tabla_lexemas)
        self._mostrar_tokens(tokens)
        self._mostrar_errores(errores)
        ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)

    def _mostrar_tabla_lexemas(self, tabla):
        filas = [
            (r"Letra (Letra | Digito)*", "id"),
            (r"Digito+", "nint"),
            (r"Digito+ . Digito+", "nfloat"),
            (r'"(Letra | Digito)*"', "LiteralCadena"),
            (r"'Letra | Digito'", "LiteralCaracter"),
            ("=", "="), ("+", "+"), ("-", "-"), ("/", "/"), ("*", "*"),
            ("==", "=="), ("!=", "!="), ("<", "<"), (">", ">"),
            ("<=", "<="), (">=", ">="), ("{", "{"), ("}", "}"),
            ("(", "("), (")", ")"), ("[", "["), ("]", "]"),
            (";", ";"), (",", ","), (".", "."), ("+=", "+="),
            ("-=", "-="), ("++", "++"), ("--", "--"), ("$", "$"),
        ]
        filas.extend((palabra, palabra) for palabra in sorted(PALABRAS_RESERVADAS))
        for lexema, token in filas:
            tabla.insert("", tk.END, values=(lexema, token))

    def _crear_tabla(self, padre, columnas, encabezados, anchos):
        tabla = ttk.Treeview(padre, columns=columnas, show="headings")
        for columna, encabezado, ancho in zip(columnas, encabezados, anchos):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=ancho, anchor="w")
        scroll = ttk.Scrollbar(padre, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tabla

    def _crear_contadores(self, padre):
        pie = tk.Frame(padre, bg=self.COLORES["panel"])
        pie.pack(fill="x", pady=(10, 0))
        self.tokens_var = tk.StringVar(value="0 tokens")
        self.errores_var = tk.StringVar(value="0 errores")
        tk.Label(pie, textvariable=self.tokens_var, bg=self.COLORES["panel"],
                 fg=self.COLORES["exito"], font=("Segoe UI", 10, "bold")).pack(
                     side="left")
        tk.Label(pie, textvariable=self.errores_var, bg=self.COLORES["panel"],
                 fg=self.COLORES["error"], font=("Segoe UI", 10, "bold")).pack(
                     side="right")

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo C#",
            filetypes=(("Archivos C#", "*.cs"), ("Todos los archivos", "*.*"))
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
        if self.ventana_resultados is not None and self.ventana_resultados.winfo_exists():
            self.ventana_resultados.destroy()
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
        self._abrir_ventana_resultados(tokens, errores)
        self.estado_var.set(
            "Análisis terminado: {} tokens y {} errores.".format(
                len(tokens), len(errores)
            )
        )

    def _limpiar_resultados(self):
        if self.ventana_resultados is not None and self.ventana_resultados.winfo_exists():
            self.ventana_resultados.destroy()

    def _mostrar_tokens(self, tokens):
        for item in self.tokens.get_children():
            self.tokens.delete(item)
        for token in tokens:
            self.tokens.insert("", tk.END, values=(
                token.tipo, token.lexema, token.renglon, token.columna
            ))

    def _mostrar_errores(self, errores):
        for item in self.errores.get_children():
            self.errores.delete(item)
        for error in errores:
            self.errores.insert("", tk.END, values=(
                str(error), error.renglon, error.columna
            ), tags=("error",))


if __name__ == "__main__":
    AplicacionAnalizador().mainloop()
