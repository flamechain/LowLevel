using System;
using System.IO;
using System.Collections.Generic;

namespace asm
{
    class Program
    {
        static void Main(string[] args)
        {
            string path;

            switch (args.Length) {
                case 0:
                    Console.WriteLine("Error 1: No input files");
                    Console.ReadLine();
                    return;
                case 1:
                    path = args[0];
                    break;
                default:
                    Console.WriteLine("Error 2: Too many arguments");
                    Console.ReadLine();
                    return;
            }

            path = Directory.GetCurrentDirectory();
            string filepath = Path.Combine(path, "main.asm");

            if (!File.Exists(filepath)) {
                Console.WriteLine($"Error 3: File '{filepath}' does not exist");
                Console.ReadLine();
                return;
            }

            string[] text = File.ReadAllLines(filepath);
            List<Byte> assembled = new List<Byte>();

            foreach (string i in text) {
                Console.WriteLine(i);
            }
            Console.ReadLine();

            File.WriteAllBytes(Path.Combine(path, "main.o"), assembled.ToArray());
        }
    }
}
