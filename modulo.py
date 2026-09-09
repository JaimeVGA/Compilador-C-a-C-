import os

class CSharpFileReader:
 

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.content = ""
        self.pos = 0
        self.line = 1
        self.column = 1

    def load_file(self) -> bool:
 
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Error: El archivo '{self.filepath}' no existe.")
        
        with open(self.filepath, 'r', encoding='utf-8') as file:
            self.content = file.read()
        return True

    def get_next_char(self):
        """Obtiene el siguiente carácter del archivo y actualiza la posición (línea y columna)."""
        if self.pos >= len(self.content):
            return None  

        char = self.content[self.pos]
        self.pos += 1

        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    def peek_char(self):
        """Retorna el siguiente carácter sin avanzar el puntero de lectura."""
        if self.pos >= len(self.content):
            return None
        return self.content[self.pos]

    def get_position(self) -> tuple:
        """Devuelve la ubicación actual en el archivo fuente: (línea, columna)."""
        return self.line, self.column



if __name__ == "__main__":
    reader = CSharpFileReader("HolaMundo.cs") ##MODIFICAR ESTA LINEA CON LA RUTA DE ARCHIVO A PROBAR,
    
    try:
        reader.load_file()
        print("Archivo cargado exitosamente. Leyendo primeros caracteres:")
        
        # Ejemplo de lectura carácter por carácter
        while True:
            linea, col = reader.get_position()
            char = reader.get_next_char()
            if char is None:
                break
            print(f"Línea {linea}, Col {col} -> Carácter: {repr(char)}")


            #MI IDEA ES QUE JUSTO DESPUES DEL PRINT EMPIECEN A LLAMAR LAS FUNCIONES QUE RECONOCERAN A QUE ESTA SE VA, DE ESO SE VAN A GUIAR DE LA TABLA QUE ESTA HACIENDO JOEL Y LEVI,
            
    except Exception as e:
        print(e)