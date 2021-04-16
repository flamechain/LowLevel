using System.Collections.Generic;

namespace Fantastic.CodeAnalysis {
    /// <summary>
    /// Unary expression containing an operand (no operator)
    /// </summary>
    public sealed class LiteralExpression : ExpressionSyntax {
        public override SyntaxType Type => SyntaxType.LiteralExpression;
        public SyntaxToken LiteralToken { get; }

        public LiteralExpression(SyntaxToken literal) {
            LiteralToken = literal;
        }

        public override IEnumerable<SyntaxNode> GetChildren() {
            yield return LiteralToken;
        }
    }
}
