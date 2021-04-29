using System;
using Fantastic.CodeAnalysis.Binding;

namespace Fantastic.CodeAnalysis {
    /// <summary>
    /// Evaulates parsed SyntaxTree
    /// </summary>
    internal sealed class Evaluator {
        private readonly BoundExpression Root;

        public Evaluator(BoundExpression root) {
            Root = root;
        }

        public object Evaluate() {
            return EvaluateExpression(Root);
        }

        private object EvaluateExpression(BoundExpression node) {
            if (node is BoundLiteralExpression n)
                return n.Value;
            else if (node is BoundUnaryExpression u) {
                object operand = EvaluateExpression(u.Operand);

                switch(u.OperatorType) {
                    case BoundUnaryOperator.Identity:
                        return (int)operand;
                    case BoundUnaryOperator.Negation:
                        return -(int)operand;
                    default:
                        throw new Exception($"Unexpected unary operator {u.OperatorType}");
                }
            } else if (node is BoundBinaryExpression b) {
                int left = (int)EvaluateExpression(b.Left);
                int right = (int)EvaluateExpression(b.Right);

                switch(b.OperatorType) {
                    case BoundBinaryOperator.Addition:
                        return left + right;
                    case BoundBinaryOperator.Subtraction:
                        return left - right;
                    case BoundBinaryOperator.Multiplication:
                        return left * right;
                    case BoundBinaryOperator.Division:
                        return left / right;
                    default:
                        throw new Exception($"Unexpected binary operator {b.OperatorType}");
                }
            }

            throw new Exception($"Unexpected binary operator {node.Type}");
        }
    }
}
