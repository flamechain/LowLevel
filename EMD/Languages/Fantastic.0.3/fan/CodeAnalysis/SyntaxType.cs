
namespace Fantastic.CodeAnalysis {
    /// <summary>
    /// Contains all tokens and expression constants for parsing
    /// </summary>
    public enum SyntaxType {
        // Tokens
        InvalidToken,
        EOFToken,
        WhitespaceToken,
        NumberToken,
        PlusToken,
        MinusToken,
        StarToken,
        ForeSlashToken,
        LParenToken,
        RParenToken,
        // Expressions
        LiteralExpression,
        UnaryExpression,
        BinaryExpression,
        ParenthesizedExpression,
    }
}
