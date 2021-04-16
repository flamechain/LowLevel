using System;
using System.Collections.Generic;
using System.Linq;

namespace Fantastic.CodeAnalysis {
    sealed class SyntaxTree {
        public IReadOnlyList<string> Diagnostics { get; }
        public ExpressionSyntax Root { get; }
        public SyntaxToken EOFToken { get; }

        public SyntaxTree(IEnumerable<string> diagnostics, ExpressionSyntax root, SyntaxToken eofToken) {
            Diagnostics = diagnostics.ToArray();
            Root = root;
            EOFToken = eofToken;
        }

        public static SyntaxTree Parse(string text) {
            Parser parser = new Parser(text);
            return parser.Parse();
        }
    }
}
