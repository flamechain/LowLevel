using System;
using System.Linq;
using Fantastic.CodeAnalysis;
using Fantastic.CodeAnalysis.Syntax;
using Fantastic.CodeAnalysis.Binding;

namespace Fantastic {
    internal static class Program {
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
                Binder binder = new Binder();
                BoundExpression boundExpression = binder.BindExpression(syntaxTree.Root);
                string[] diagnostics = syntaxTree.Diagnostics.Concat(binder._diagnostics).ToArray();

                if (showTree) {
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    PrettyPrint(syntaxTree.Root);
                    Console.ResetColor();
                }

                if (!diagnostics.Any()) {
                    Evaluator e = new Evaluator(boundExpression);
                    object result = e.Evaluate();
                    Console.WriteLine(result);
                } else {
                    Console.ForegroundColor = ConsoleColor.DarkRed;

                    foreach (string diagnostic in diagnostics)
                        Console.WriteLine(diagnostic);

                    Console.ResetColor();
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
