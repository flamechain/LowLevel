using System.Collections.Generic;

namespace Fantastic.CodeAnalysis {
    /// <summary>
    /// Takes lexed tokens and parses into SyntaxTree
    /// </summary>
    internal sealed class Parser {
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
                token = lexer.Lex();

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

        private SyntaxToken MatchToken(SyntaxType type) {
            if (Current.Type == type)
                return NextToken();

            Diagnostics.Add($"ERROR: Unexpected token <{Current.Type}>, expected <{type}>");
            return new SyntaxToken(type, Current.Position, null, null);
        }

        public SyntaxTree Parse() {
            ExpressionSyntax expression = ParseExpression();
            SyntaxToken eofToken = MatchToken(SyntaxType.EOFToken);
            return new SyntaxTree(Diagnostics, expression, eofToken);
        }

        private ExpressionSyntax ParseExpression(int parentPrecedence = 0) {
            ExpressionSyntax left;
            int unaryPredecence = Current.Type.GetUnaryOperatorPrecedence();

            if (unaryPredecence != 0 && unaryPredecence >= parentPrecedence) {
                SyntaxToken operatorToken = NextToken();
                ExpressionSyntax operand = ParseExpression(unaryPredecence);
                left = new UnaryExpression(operatorToken, operand);
            } else {
                left = ParsePrimaryExpression();
            }

            while (true) {
                int precedence = Current.Type.GetBinaryOperatorPrecedence();

                if (precedence == 0 || precedence <= parentPrecedence)
                    break;

                SyntaxToken operatorToken = NextToken();
                ExpressionSyntax right = ParseExpression(precedence);
                left = new BinaryExpression(left, operatorToken, right);
            }

            return left;
        }

        private ExpressionSyntax ParsePrimaryExpression() {
            if (Current.Type == SyntaxType.LParenToken) {
                SyntaxToken left = NextToken();
                ExpressionSyntax expression = ParseExpression();
                SyntaxToken right = MatchToken(SyntaxType.RParenToken);
                return new ParenthesizedExpression(left, expression, right);
            }

            SyntaxToken number = MatchToken(SyntaxType.NumberToken);
            return new LiteralExpression(number);
        }
    }
}
