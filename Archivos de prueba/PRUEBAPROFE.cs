using System;

class Program
{
    static void Main()
    {
        @
        char a;
        char[] b = new char[30];
        ¨
        /*comentario 
        de bloque*/
        unsafe
        {
            int* aptr;
            int[] vec = new int[10];
            int categ = 2;
            int** aVecPtr = null; // int** aVecPtr[3]
            int[,] matriz = new int[2, 2];
        }
        float[] vecFloat = { 2.3f, 5.0f, 3.1f };
        float sueldo = 0f;
        Console.Write("Teclea dos numeros enteros:");
        
        string inputA = Console.ReadLine();
        string inputB = Console.ReadLine();
        a = string.IsNullOrEmpty(inputA) ? '\0' : inputA[0];
        // b = inputB.ToCharArray();

        int c = a % 2;
        if (c == 0)
        {
            Console.WriteLine($"{c} es par\n");
        }
        else
        {
            --c;
            // strcpy(b, "hola");
            Array.Copy("hola".ToCharArray(), b, Math.Min(4, b.Length));
        }

        switch (categ)
        {
            case 1:
                float nsueldo = sueldo * 1.15f;
                break;
            case '2':
                nsueldo = Funcion(2.1f, 3.2f);
                break;
            default:
                Console.Write($"{Funcion(2, 3)}");
                break;
        }

        int i = 5;
        for (i = 5; i >= 0; i--)
            Console.WriteLine($"{i}\n");

        int n = 0;
        int j = 0;
        float pot = 0f;
        float suma = 0f;
        for (i = 0; i <= n; i++)
        {
            pot = 1;
            for (j = 0; j < i; j++)
            {
                pot = pot * 2;
            }
            suma = suma + 1 / pot;
        }

        i = 0;
        while (i <= 4 && suma != 0)
        {
            suma += 2;
            i++;
        }

        i = 1;
        bool calif = false;
        do
        {
            suma *= 2;
            i -= 1;
        } while (i > 0 || calif);

        // return 0;
    }

    static float Funcion(float a, float b)
    {
        int[,] matriz = new int[2, 2];
        char x = ' ', y = '\0';
        int i = 0, j = 0;
        if (!a.Equals(b)) // !a == b
            matriz[i, j] = 0;
        return a + b;
    }
}