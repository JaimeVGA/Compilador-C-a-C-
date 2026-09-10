from typing import Optional
from reconocedor_tokens import ReconocedorTokens
from tokens import Token


class ReconocedorCadenasYCaracteres(ReconocedorTokens):

    def procesar(self) -> Optional[Token]:
        if self.lector.ver_actual() == '"':
            return self._procesar_cadena()
        elif self.lector.ver_actual() == "'":
            return self._procesar_caracter()
        return None

    def _procesar_cadena(self) -> Optional[Token]:
        renglon, columna = self.lector.renglon, self.lector.columna
        self.lector.siguiente_caracter()  # consume "
        lexema = '"'
        while self.lector.ver_actual() is not None and self.lector.ver_actual() != '"':
            if self.lector.ver_actual() == '\n':
                self.manejador_errores.registrar_error('"(cadena sin cerrar)', renglon, columna)
                return None
            lexema += self.lector.siguiente_caracter()
        if self.lector.ver_actual() == '"':
            lexema += self.lector.siguiente_caracter()  # consume "
            return Token('LiteralCadena', lexema, renglon, columna)
        self.manejador_errores.registrar_error('"(cadena sin cerrar)', renglon, columna)
        return None

    def _procesar_caracter(self) -> Optional[Token]:
        renglon, columna = self.lector.renglon, self.lector.columna
        self.lector.siguiente_caracter()  # consume '
        lexema = "'"
        if self.lector.ver_actual() is not None and self.lector.ver_actual() != "'":
            lexema += self.lector.siguiente_caracter()
        if self.lector.ver_actual() == "'":
            lexema += self.lector.siguiente_caracter()  # consume '
            return Token('LiteralCaracter', lexema, renglon, columna)
        self.manejador_errores.registrar_error("'(caracter sin cerrar)", renglon, columna)
        return None
