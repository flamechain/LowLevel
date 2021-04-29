using System.Collections.Generic;

namespace Fantastic.CodeAnalysis.Syntax {
    /// <summary>
    /// Expression for expressions contained in parenthesis
    /// </summary>
    public sealed class ParenthesizedExpression : ExpressionSyntax {
        public SyntaxToken LParenToken;
        public ExpressionSyntax Expression;
        public SyntaxToken RParenToken;
        public override SyntaxType Type => SyntaxType.ParenthesizedExpression;

        public ParenthesizedExpression(SyntaxToken lParenToken, ExpressionSyntax expression, SyntaxToken rParenToken) {
            LParenToken = lParenToken;
            Expression = expression;
            RParenToken = rParenToken;
        }

        public override IEnumerable<SyntaxNode> GetChildren() {
            yield return LParenToken;
            yield return Expression;
            yield return RParenToken;
        }
    }
}
