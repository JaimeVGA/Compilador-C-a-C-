import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from lector_archivo import LectorArchivo
from manejador_errores import ManejadorErrores
from reconocedor_tokens import ReconocedorTokens

_DIR = os.path.dirname(__file__)


def imprimir_resultados(ruta, tokens, errores):
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  ANALISIS LEXICO: {ruta}")
    print(sep)

    print(f"\n{'[ TOKENS ENCONTRADOS ]':^60}")
    print("-" * 60)
    if tokens:
        for tk in tokens:
            print(tk)
    else:
        print("  (ninguno)")

    print(f"\n{'[ ERRORES LEXICOS ]':^60}")
    print("-" * 60)
    if errores:
        for err in errores:
            print(err)
    else:
        print("  No se encontraron errores lexicos.")

    print(f"\n  Total tokens : {len(tokens)}")
    print(f"  Total errores: {len(errores)}")
    print(sep)


def main():
    ruta = os.path.join(_DIR, '..', 'HolaMundo.cs')

    lector = LectorArchivo()
    lector.leer_archivo(ruta)

    manejador = ManejadorErrores()
    reconocedor = ReconocedorTokens(lector, manejador)
    tokens = reconocedor.analizar()

    imprimir_resultados(ruta, tokens, manejador.obtener_errores())


if __name__ == "__main__":
    main()
