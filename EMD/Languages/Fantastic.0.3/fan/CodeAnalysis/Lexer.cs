using System;
using System.Collections.Generic;
using System.Linq;

namespace Fantastic.CodeAnalysis {
    class Lexer {
        private readonly string Text;
        private int Position;
        private List<string> Diagnostics = new List<string>();
        public IEnumerable<string> _diagnostics => Diagnostics;

        public Lexer(string text) {
            Text = text;
        }

        private char Current {
            get {
                if (Position >= Text.Length)
                    return '\0';

                return Text[Position];
            }
        }

        private void Next() {
            Position++;
        }

        public SyntaxToken NextToken() {
            // <numbers>
            // + - * / ( )
            // <whitespace>

            if (Position >= Text.Length)
                return new SyntaxToken(SyntaxType.EOFToken, Position, "\0", null);

            if (char.IsDigit(Current)) {
                int start = Position;

                while (char.IsDigit(Current))
                    Next();

                int length = Position - start;
                string text = Text.Substring(start, length);

                if (!int.TryParse(text, out int value))
                    Diagnostics.Add($"ERROR: the number {Text} cannot be represented by and int32");

                return new SyntaxToken(SyntaxType.NumberToken, start, text, value);
            } else if (char.IsWhiteSpace(Current)) {
                int start = Position;

                while (char.IsWhiteSpace(Current))
                    Next();

                int length = Position - start;
                string text = Text.Substring(start, length);

                return new SyntaxToken(SyntaxType.WhitespaceToken, start, text, null);
            } else if (Current == '+')
                return new SyntaxToken(SyntaxType.PlusToken, Position++, "+", null);
            else if (Current == '-')
                return new SyntaxToken(SyntaxType.MinusToken, Position++, "-", null);
            else if (Current == '*')
                return new SyntaxToken(SyntaxType.StarToken, Position++, "*", null);
            else if (Current == '/')
                return new SyntaxToken(SyntaxType.ForeSlashToken, Position++, "/", null);
            else if (Current == '(')
                return new SyntaxToken(SyntaxType.LParenToken, Position++, "(", null);
            else if (Current == ')')
                return new SyntaxToken(SyntaxType.RParenToken, Position++, ")", null);

            Diagnostics.Add($"ERROR: bad character input: '{Current}'");
            return new SyntaxToken(SyntaxType.InvalidToken, Position++, Text.Substring(Position - 1, 1), null);
        }
    }
}
