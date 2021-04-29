using System.Collections.Generic;

namespace Fantastic.CodeAnalysis.Syntax {
    /// <summary>
    /// Unary expression containing an operand (no operator)
    /// </summary>
    public sealed class LiteralExpression : ExpressionSyntax {
        public override SyntaxType Type => SyntaxType.LiteralExpression;
        public SyntaxToken LiteralToken { get; }
        public object Value { get; }

        public LiteralExpression(SyntaxToken literalToken)
            : this(literalToken, literalToken.Value) {
        }

        public LiteralExpression(SyntaxToken literal, object value) {
            LiteralToken = literal;
            Value = value;
        }

        public override IEnumerable<SyntaxNode> GetChildren() {
            yield return LiteralToken;
        }
    }
}
