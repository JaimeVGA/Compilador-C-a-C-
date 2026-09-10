import os
from typing import Optional


class LectorArchivo:

    def __init__(self):
        self.ruta_archivo = ""
        self.contenido = ""
        self.indice_actual = 0
        self.renglon = 1
        self.columna = 1

    def leer_archivo(self, ruta: str):
        self.ruta_archivo = ruta
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"El archivo '{ruta}' no existe.")
        with open(ruta, 'r', encoding='utf-8') as f:
            self.contenido = f.read()

    def ver_actual(self) -> Optional[str]:
        if self.indice_actual < len(self.contenido):
            return self.contenido[self.indice_actual]
        return None

    def espiar(self, offset: int = 1) -> Optional[str]:
        idx = self.indice_actual + offset
        if idx < len(self.contenido):
            return self.contenido[idx]
        return None

    def actualizar_posicion(self, char: str):
        if char == '\n':
            self.renglon += 1
            self.columna = 1
        else:
            self.columna += 1

    def siguiente_caracter(self) -> Optional[str]:
        if self.indice_actual >= len(self.contenido):
            return None
        char = self.contenido[self.indice_actual]
        self.indice_actual += 1
        self.actualizar_posicion(char)
        return char

    def retroceder(self):
        if self.indice_actual > 0:
            self.indice_actual -= 1
            if self.columna > 1:
                self.columna -= 1
