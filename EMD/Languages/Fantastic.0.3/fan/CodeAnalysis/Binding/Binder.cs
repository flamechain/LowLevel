using System;
using Fantastic.CodeAnalysis.Syntax;
using System.Collections.Generic;

/// <summary>
/// Namespace for binding, similar class structure; individual comments would be redundent
/// </summary>
namespace Fantastic.CodeAnalysis.Binding {
    /// <summary>
    /// Better syntax tree thats more efficent by rearranging instead of linking prioreties
    /// </summary>
    internal sealed class Binder {
        private readonly List<string> Diagnostics = new List<string>();
        public IEnumerable<string> _diagnostics => Diagnostics;

        public BoundExpression BindExpression(ExpressionSyntax syntax) {
            switch(syntax.Type) {
                case SyntaxType.LiteralExpression:
                    return BindLiteralExpression((LiteralExpression)syntax);
                case SyntaxType.UnaryExpression:
                    return BindUnaryExpression((UnaryExpression)syntax);
                case SyntaxType.BinaryExpression:
                    return BindBinaryExpression((BinaryExpression)syntax);
                default:
                    throw new Exception($"Unexpected syntax {syntax.Type}");
            }
        }

        private BoundExpression BindLiteralExpression(LiteralExpression syntax) {
            object value = syntax.Value ?? 0;
            return new BoundLiteralExpression(value);
        }

        private BoundExpression BindUnaryExpression(UnaryExpression syntax) {
            BoundExpression boundOperand = BindExpression(syntax.Operand);
            BoundUnaryOperator? boundOperator = BindUnaryOperator(syntax.Operator.Type, boundOperand.Kind);
            
            if (boundOperator == null) {
                Diagnostics.Add($"ERROR: Unary operator '{syntax.Operator.Type}' is not defined for type {boundOperand.Kind}");
                return boundOperand;
            }

            return new BoundUnaryExpression(boundOperator.Value, boundOperand);
        }

        private BoundExpression BindBinaryExpression(BinaryExpression syntax) {
            BoundExpression boundLeft = BindExpression(syntax.Left);
            BoundExpression boundRight = BindExpression(syntax.Right);
            BoundBinaryOperator? boundOperator = BindBinaryOperator(syntax.Operator.Type, boundLeft.Kind, boundRight.Kind);

            if (boundOperator == null) {
                Diagnostics.Add($"ERROR: Binary operator '{syntax.Operator.Type}' is not defined for types {boundLeft.Kind} and {boundRight.Kind}");
                return boundLeft;
            }

            return new BoundBinaryExpression(boundLeft, boundOperator.Value, boundRight);
        }

        private BoundUnaryOperator? BindUnaryOperator(SyntaxType type, Type operandType) {
            if (operandType == typeof(int)) {
                switch (type) {
                    case SyntaxType.PlusToken:
                        return BoundUnaryOperator.Identity;
                    case SyntaxType.MinusToken:
                        return BoundUnaryOperator.Negation;
                    default:
                        throw new Exception($"Unexpected unary operator {type}");
                }
            } else if (operandType == typeof(bool)) {
                switch (type) {
                    case SyntaxType.BangToken:
                        return BoundUnaryOperator.LogicalNot;
                }
            }

            return null;
        }

        private BoundBinaryOperator? BindBinaryOperator(SyntaxType type, Type leftType, Type rightType) {
            if (leftType == typeof(int) && rightType == typeof(int)) {
                switch (type) {
                    case SyntaxType.PlusToken:
                        return BoundBinaryOperator.Addition;
                    case SyntaxType.MinusToken:
                        return BoundBinaryOperator.Subtraction;
                    case SyntaxType.StarToken:
                        return BoundBinaryOperator.Multiplication;
                    case SyntaxType.ForeSlashToken:
                        return BoundBinaryOperator.Division;
                    default:
                        throw new Exception($"Unexpected unary operator {type}");
                }
            } else if (leftType == typeof(bool) && rightType == typeof(bool)) {
                switch (type) {
                    case SyntaxType.DoubleAmpersandToken:
                        return BoundBinaryOperator.LogicalAnd;
                    case SyntaxType.DoublePipeToken:
                        return BoundBinaryOperator.LogicalOr;
                    default:
                        throw new Exception($"Unexpected unary operator {type}");
                }
            }

            return null;
        }
    }
}
