using System.Collections.Generic;

namespace Fantastic.CodeAnalysis.Syntax {
    /// <summary>
    /// Creates tokens
    /// </summary>
    internal sealed class Lexer {
        private readonly string Text;
        private int Position;
        private List<string> Diagnostics = new List<string>();
        public IEnumerable<string> _diagnostics => Diagnostics;
        private char Current => Peek(0);
        private char Lookahead => Peek(1);

        public Lexer(string text) {
            Text = text;
        }

        private char Peek(int offset) {
            int index = Position + offset;

            if (index >= Text.Length)
                return '\0';

            return Text[index];
        }

        private void Next() {
            Position++;
        }

        public SyntaxToken Lex() {
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
            }

            if (char.IsLetter(Current)) {
                int start = Position;

                while (char.IsLetter(Current))
                    Next();

                int length = Position - start;
                string text = Text.Substring(start, length);
                SyntaxType type = SyntaxFacts.GetKeywordType(text);
                return new SyntaxToken(type, start, text, null);
            }

            switch(Current) {
                case '+':
                    return new SyntaxToken(SyntaxType.PlusToken, Position++, "+", null);
                case '-':
                    return new SyntaxToken(SyntaxType.MinusToken, Position++, "-", null);
                case '*':
                    return new SyntaxToken(SyntaxType.StarToken, Position++, "*", null);
                case '/':
                    return new SyntaxToken(SyntaxType.ForeSlashToken, Position++, "/", null);
                case '(':
                    return new SyntaxToken(SyntaxType.LParenToken, Position++, "(", null);
                case ')':
                    return new SyntaxToken(SyntaxType.RParenToken, Position++, ")", null);
                case '!':
                    return new SyntaxToken(SyntaxType.BangToken, Position++, "!", null);
                case '&':
                    if (Lookahead == '&')
                        return new SyntaxToken(SyntaxType.DoubleAmpersandToken, Position+=2, "&&", null);
                    break;
                case '|':
                    if (Lookahead == '|')
                        return new SyntaxToken(SyntaxType.DoublePipeToken, Position+=2, "||", null);
                    break;
            }

            Diagnostics.Add($"ERROR: bad character input: '{Current}'");
            return new SyntaxToken(SyntaxType.InvalidToken, Position++, Text.Substring(Position - 1, 1), null);
        }
    }
}
