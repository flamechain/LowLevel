using System;
using System.Collections.Generic;
using System.Linq;
using Fantastic.CodeAnalysis;

namespace Fantastic {
    class Program {
        static void Main(string[] args) {
            bool showTree = false;

            Console.WriteLine("Fantastic Compiler 0.3:");

            while (true) {
                Console.Write("> ");

                string line = Console.ReadLine();
                
                if (string.IsNullOrWhiteSpace(line))
                    continue;
                else if (line == "$showTree") {
                    showTree = !showTree;
                    Console.WriteLine(showTree ? "=> Showing parse trees" : "=> Hiding parse trees");
                    continue;
                } else if (line == "cls") {
                    Console.Clear();
                    Console.WriteLine("Fantastic Compiler 0.3:");
                    continue;
                } else if (line == "exit") {
                    return;
                }

                SyntaxTree syntaxTree = SyntaxTree.Parse(line);
                ConsoleColor color = Console.ForegroundColor;

                if (showTree) {
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    PrettyPrint(syntaxTree.Root);
                    Console.ForegroundColor = color;
                }

                if (!syntaxTree.Diagnostics.Any()) {
                    Evaluator e = new Evaluator(syntaxTree.Root);
                    int result = e.Evaluate();
                    Console.WriteLine(result);
                } else {
                    Console.ForegroundColor = ConsoleColor.DarkRed;

                    foreach (string diagnostic in syntaxTree.Diagnostics)
                        Console.WriteLine(diagnostic);

                    Console.ForegroundColor = color;
                }
            }
        }

        static void PrettyPrint(SyntaxNode node, string indent = "", bool isLast = true) {
            string marker = isLast ? "└──" : "├──";

            Console.Write(indent);
            Console.Write(marker);
            Console.Write(node.Type);

            if (node is SyntaxToken t && t.Value != null) {
                Console.Write(" ");
                Console.Write(t.Value);
            }

            Console.WriteLine();

            indent += isLast ? "   " :  "│  ";

            SyntaxNode lastChild = node.GetChildren().LastOrDefault();

            foreach (SyntaxNode child in node.GetChildren())
                PrettyPrint(child, indent, child == lastChild);
        }
    }
}
