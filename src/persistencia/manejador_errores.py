from typing import List
from ..modelos.tokens import ErrorLexico


class ManejadorErrores:

    def __init__(self):
        self.errores: List[ErrorLexico] = []

    def registrar_error(self, caracter: str, renglon: int, columna: int):
        self.errores.append(ErrorLexico(caracter, renglon, columna))

    def obtener_errores(self) -> List[ErrorLexico]:
        return self.errores
