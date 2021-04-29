
namespace Fantastic.CodeAnalysis.Syntax {
    /// <summary>
    /// Contains all tokens and expression constants for parsing
    /// </summary>
    public enum SyntaxType {
        // Tokens
        InvalidToken,
        IdentifierToken,
        EOFToken,
        WhitespaceToken,
        NumberToken,
        PlusToken,
        MinusToken,
        StarToken,
        ForeSlashToken,
        LParenToken,
        RParenToken,
        BangToken,
        DoubleAmpersandToken,
        DoublePipeToken,
        // Expressions
        LiteralExpression,
        UnaryExpression,
        BinaryExpression,
        ParenthesizedExpression,
        // Keywords
        TrueKeyword,
        FalseKeyword,
    }
}
