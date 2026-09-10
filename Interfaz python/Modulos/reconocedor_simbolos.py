from typing import Optional
from reconocedor_tokens import ReconocedorTokens
from tokens import Token

_DELIMITADORES_SIMPLES = frozenset({'{', '}', '(', ')', '[', ']', ';', ',', '.', '$', '*', '/'})


class ReconocedorSimbolosYLimpieza(ReconocedorTokens):

    def ignorar_espacios_y_saltos(self):
        while self.lector.ver_actual() in (' ', '\t', '\n', '\r'):
            self.lector.siguiente_caracter()

    def procesar_comentarios(self):
        if self.lector.espiar() == '/':
            self.lector.siguiente_caracter()  # consume primer /
            self.lector.siguiente_caracter()  # consume segundo /
            while self.lector.ver_actual() is not None and self.lector.ver_actual() != '\n':
                self.lector.siguiente_caracter()
        elif self.lector.espiar() == '*':
            renglon, columna = self.lector.renglon, self.lector.columna
            self.lector.siguiente_caracter()  # consume /
            self.lector.siguiente_caracter()  # consume *
            while self.lector.ver_actual() is not None:
                if self.lector.ver_actual() == '*' and self.lector.espiar() == '/':
                    self.lector.siguiente_caracter()  # consume *
                    self.lector.siguiente_caracter()  # consume /
                    return
                self.lector.siguiente_caracter()
            self.manejador_errores.registrar_error('/* (comentario sin cerrar)', renglon, columna)

    def procesar_operadores_y_delimitadores(self) -> Optional[Token]:
        renglon, columna = self.lector.renglon, self.lector.columna
        c = self.lector.siguiente_caracter()

        if c == '=':
            if self.lector.ver_actual() == '=':
                self.lector.siguiente_caracter()
                return Token('==', '==', renglon, columna)
            return Token('=', '=', renglon, columna)

        elif c == '!':
            if self.lector.ver_actual() == '=':
                self.lector.siguiente_caracter()
                return Token('!=', '!=', renglon, columna)
            self.manejador_errores.registrar_error('!', renglon, columna)
            return None

        elif c == '<':
            if self.lector.ver_actual() == '=':
                self.lector.siguiente_caracter()
                return Token('<=', '<=', renglon, columna)
            return Token('<', '<', renglon, columna)

        elif c == '>':
            if self.lector.ver_actual() == '=':
                self.lector.siguiente_caracter()
                return Token('>=', '>=', renglon, columna)
            return Token('>', '>', renglon, columna)

        elif c == '+':
            if self.lector.ver_actual() == '+':
                self.lector.siguiente_caracter()
                return Token('++', '++', renglon, columna)
            elif self.lector.ver_actual() == '=':
                self.lector.siguiente_caracter()
                return Token('+=', '+=', renglon, columna)
            return Token('+', '+', renglon, columna)

        elif c == '-':
            if self.lector.ver_actual() == '-':
                self.lector.siguiente_caracter()
                return Token('--', '--', renglon, columna)
            elif self.lector.ver_actual() == '=':
                self.lector.siguiente_caracter()
                return Token('-=', '-=', renglon, columna)
            return Token('-', '-', renglon, columna)

        elif c in ('{', '}', '(', ')', '[', ']', ';', ',', '.', '$', '*', '/'):
            return Token(c, c, renglon, columna)

        else:
            self.manejador_errores.registrar_error(c, renglon, columna)
            return None
