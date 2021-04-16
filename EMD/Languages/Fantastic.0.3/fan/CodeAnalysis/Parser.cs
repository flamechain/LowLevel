using System;
using System.Collections.Generic;
using System.Linq;

namespace Fantastic.CodeAnalysis {
    class Parser {
        private readonly SyntaxToken[] Tokens;
        private int Position;
        private List<string> Diagnostics = new List<string>();
        private SyntaxToken Current => Peek(0);
        public IEnumerable<string> _diagnostics => Diagnostics;

        public Parser(string text) {
            List<SyntaxToken> tokens = new List<SyntaxToken>();

            Lexer lexer = new Lexer(text);
            SyntaxToken token;

            do {
                token = lexer.NextToken();

                if (token.Type != SyntaxType.WhitespaceToken && token.Type != SyntaxType.InvalidToken)
                    tokens.Add(token);

            } while (token.Type != SyntaxType.EOFToken);

            Tokens = tokens.ToArray();
            Diagnostics.AddRange(lexer._diagnostics);
        }

        private SyntaxToken NextToken() {
            SyntaxToken current = Current;
            Position++;
            return current;
        }

        private SyntaxToken Peek(int offset) {
            int index = Position + offset;

            if (index >= Tokens.Length)
                return Tokens[Tokens.Length - 1];

            return Tokens[index];
        }

        private SyntaxToken Match(SyntaxType type) {
            if (Current.Type == type)
                return NextToken();

            Diagnostics.Add($"ERROR: Unexpected token <{Current.Type}>, expected <{type}>");
            return new SyntaxToken(type, Current.Position, null, null);
        }

        public SyntaxTree Parse() {
            ExpressionSyntax expression = ParseTerm();
            SyntaxToken eofToken = Match(SyntaxType.EOFToken);
            return new SyntaxTree(Diagnostics, expression, eofToken);
        }

        private ExpressionSyntax ParseFactor() {
            ExpressionSyntax left = ParsePrimaryExpression();

            while (Current.Type == SyntaxType.StarToken || Current.Type == SyntaxType.ForeSlashToken) {
                SyntaxToken operatorToken = NextToken();
                ExpressionSyntax right = ParsePrimaryExpression();
                left = new BinaryExpression(left, operatorToken, right);
            }

            return left;
        }

        private ExpressionSyntax ParseTerm() {
            ExpressionSyntax left = ParseFactor();

            while (Current.Type == SyntaxType.PlusToken || Current.Type == SyntaxType.MinusToken) {
                SyntaxToken operatorToken = NextToken();
                ExpressionSyntax right = ParseFactor();
                left = new BinaryExpression(left, operatorToken, right);
            }

            return left;
        }

        private ExpressionSyntax ParseExpression() {
            return ParseTerm();
        }

        private ExpressionSyntax ParsePrimaryExpression() {
            if (Current.Type == SyntaxType.LParenToken) {
                SyntaxToken left = NextToken();
                ExpressionSyntax expression = ParseExpression();
                SyntaxToken right = Match(SyntaxType.RParenToken);
                return new ParenthesizedExpression(left, expression, right);
            }

            SyntaxToken number = Match(SyntaxType.NumberToken);
            return new NumberExpression(number);
        }
    }
}
