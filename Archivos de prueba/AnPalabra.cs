using System;

class Program
{
    static void Main()
    {
        // Leer la cadena de entrada
        string palabra = Console.ReadLine();

        if (palabra != null)
        {
            // 1. Contar la cantidad de letras
            int cantidadLetras = palabra.Length;

            // 2. Contar las vocales
            int cantidadVocales = 0;
            foreach (char c in palabra)
            {
                char cLower = char.ToLower(c);
                if (cLower == 'a' || cLower == 'e' || cLower == 'i' || cLower == 'o' || cLower == 'u')
                {
                    cantidadVocales++;
                }
            }

            // 3. Invertir la cadena
            char[] charArray = palabra.ToCharArray();
            Array.Reverse(charArray);
            string palabraInvertida = new string(charArray);

            // Imprimir los resultados
            Console.WriteLine(cantidadLetras);
            Console.WriteLine(cantidadVocales);
            Console.WriteLine(palabraInvertida);
        }
    }
}