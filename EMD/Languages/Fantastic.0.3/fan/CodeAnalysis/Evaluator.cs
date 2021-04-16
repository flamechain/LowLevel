using System;

namespace Fantastic.CodeAnalysis {
    /// <summary>
    /// Evaulates parsed SyntaxTree
    /// </summary>
    internal sealed class Evaluator {
        private readonly ExpressionSyntax Root;

        public Evaluator(ExpressionSyntax root) {
            Root = root;
        }

        public int Evaluate() {
            return EvaluateExpression(Root);
        }

        private int EvaluateExpression(ExpressionSyntax node) {
            if (node is LiteralExpression n)
                return (int)n.LiteralToken.Value;
            else if (node is UnaryExpression u) {
                int operand = EvaluateExpression(u.Operand);

                if (u.Operator.Type == SyntaxType.PlusToken)
                    return operand;
                else if (u.Operator.Type == SyntaxType.MinusToken)
                    return -operand;
                else
                    throw new Exception($"Unexpected unary operator {u.Operator.Type}");
            } else if (node is BinaryExpression b) {
                int left = EvaluateExpression(b.Left);
                int right = EvaluateExpression(b.Right);

                if (b.Operator.Type == SyntaxType.PlusToken)
                    return left + right;
                else if (b.Operator.Type == SyntaxType.MinusToken)
                    return left - right;
                else if (b.Operator.Type == SyntaxType.StarToken)
                    return left * right;
                else if (b.Operator.Type == SyntaxType.ForeSlashToken)
                    return left / right;
                else
                    throw new Exception($"Unexpected binary operator {b.Operator.Type}");
            } else if (node is ParenthesizedExpression p)
                return EvaluateExpression(p.Expression);

            throw new Exception($"Unexpected binary operator {node.Type}");
        }
    }
}
