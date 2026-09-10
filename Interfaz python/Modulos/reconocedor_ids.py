from typing import Optional
from reconocedor_tokens import ReconocedorTokens
from tokens import Token, PALABRAS_RESERVADAS


class ReconocedorIDsYReservadas(ReconocedorTokens):

    def procesar(self) -> Optional[Token]:
        renglon, columna = self.lector.renglon, self.lector.columna
        lexema = ""
        while self.lector.ver_actual() is not None and (
            self.lector.ver_actual().isalpha() or
            self.lector.ver_actual().isdigit() or
            self.lector.ver_actual() == '_'
        ):
            lexema += self.lector.siguiente_caracter()
        tipo = lexema if lexema in PALABRAS_RESERVADAS else 'id'
        return Token(tipo, lexema, renglon, columna)
