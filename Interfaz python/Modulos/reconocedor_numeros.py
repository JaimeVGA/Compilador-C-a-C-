from typing import Optional
from reconocedor_tokens import ReconocedorTokens
from tokens import Token


class ReconocedorNumeros(ReconocedorTokens):

    def procesar(self) -> Optional[Token]:
        renglon, columna = self.lector.renglon, self.lector.columna
        lexema = ""
        while self.lector.ver_actual() is not None and self.lector.ver_actual().isdigit():
            lexema += self.lector.siguiente_caracter()
        if (self.lector.ver_actual() == '.' and
                self.lector.espiar() is not None and
                self.lector.espiar().isdigit()):
            lexema += self.lector.siguiente_caracter()
            while self.lector.ver_actual() is not None and self.lector.ver_actual().isdigit():
                lexema += self.lector.siguiente_caracter()
            if self.lector.ver_actual() in ('f', 'F', 'd', 'D', 'm', 'M'):
                lexema += self.lector.siguiente_caracter()
            return Token('nfloat', lexema, renglon, columna)
        if self.lector.ver_actual() in ('f', 'F'):
            lexema += self.lector.siguiente_caracter()
            return Token('nfloat', lexema, renglon, columna)
        return Token('nint', lexema, renglon, columna)
