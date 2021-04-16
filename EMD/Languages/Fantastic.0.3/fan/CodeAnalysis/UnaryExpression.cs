using System.Collections.Generic;

namespace Fantastic.CodeAnalysis {
    /// <summary>
    /// Expression with operator and operand
    /// </summary>
    public sealed class UnaryExpression : ExpressionSyntax {
        public override SyntaxType Type => SyntaxType.UnaryExpression;
        public ExpressionSyntax Operand { get; }
        public SyntaxToken Operator { get; }

        public UnaryExpression(SyntaxToken operatorToken, ExpressionSyntax operand) {
            Operator = operatorToken;
            Operand = operand;
        }

        public override IEnumerable<SyntaxNode> GetChildren() {
            yield return Operator;
            yield return Operand;
        }
    }
}
