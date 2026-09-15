from dataclasses import dataclass

PALABRAS_RESERVADAS = {
    'using', 'namespace', 'class', 'static', 'void',
    'int', 'float', 'double', 'string', 'char', 'bool',
    'if', 'else', 'for', 'while', 'return',
    'Console', 'Write', 'Line', 'Read', 'Parse','switch', 
    'case', 'default', 'break', 'continue', 'do', 'foreach', 'in',
    'struct', 'interface','null', 'true', 'false','public', 
    'private', 'protected', 'internal', 'new', 'unsafe', 'fixed',
    'const', 'readonly', 'ref', 'out', 'params', 'this', 'base',
}


@dataclass
class Token:
    tipo: str
    lexema: str
    renglon: int
    columna: int

    def __str__(self):
        return f"[{self.tipo:<20}] '{self.lexema}'\t renglon {self.renglon}, col {self.columna}"


@dataclass
class ErrorLexico:
    caracter: str
    renglon: int
    columna: int

    def __str__(self):
        return (
            f"Error lexico en renglon {self.renglon}, "
            f"columna {self.columna}: caracter inesperado '{self.caracter}'"
        )
