using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        int N = int.Parse(Console.ReadLine());

        // Generar la serie de Fibonacci menor que N
        HashSet<int> fibonacci = new HashSet<int>();
        int a = 1, b = 2;
        fibonacci.Add(a);
        fibonacci.Add(b);
        
        while (true)
        {
            int next = a + b;
            if (next >= N) break;
            fibonacci.Add(next);
            a = b;
            b = next;
        }

        // Imprimir números menores que N que no están en Fibonacci
        for (int i = 1; i < N; ++i)
        {
            if (!fibonacci.Contains(i))
            {
                Console.Write(i + " ");
            }
        }
    }
}