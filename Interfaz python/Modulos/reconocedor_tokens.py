from typing import List
from lector_archivo import LectorArchivo
from manejador_errores import ManejadorErrores
from tokens import Token


class ReconocedorTokens:

    def __init__(self, lector: LectorArchivo, manejador_errores: ManejadorErrores):
        self.lector = lector
        self.manejador_errores = manejador_errores

    def analizar(self) -> List[Token]:
        # Importaciones diferidas para evitar importaciones circulares
        from reconocedor_ids import ReconocedorIDsYReservadas
        from reconocedor_numeros import ReconocedorNumeros
        from reconocedor_cadenas import ReconocedorCadenasYCaracteres
        from reconocedor_simbolos import ReconocedorSimbolosYLimpieza

        tokens: List[Token] = []
        ids_rec = ReconocedorIDsYReservadas(self.lector, self.manejador_errores)
        num_rec = ReconocedorNumeros(self.lector, self.manejador_errores)
        cadenas_rec = ReconocedorCadenasYCaracteres(self.lector, self.manejador_errores)
        simbolos_rec = ReconocedorSimbolosYLimpieza(self.lector, self.manejador_errores)

        while self.lector.ver_actual() is not None:
            simbolos_rec.ignorar_espacios_y_saltos()
            if self.lector.ver_actual() is None:
                break

            c = self.lector.ver_actual()

            if c.isalpha() or c == '_':
                tk = ids_rec.procesar()
                if tk:
                    tokens.append(tk)

            elif c.isdigit():
                tk = num_rec.procesar()
                if tk:
                    tokens.append(tk)

            elif c in ('"', "'"):
                tk = cadenas_rec.procesar()
                if tk:
                    tokens.append(tk)

            elif c == '/' and self.lector.espiar() in ('/', '*'):
                simbolos_rec.procesar_comentarios()

            else:
                tk = simbolos_rec.procesar_operadores_y_delimitadores()
                if tk:
                    tokens.append(tk)

        return tokens
