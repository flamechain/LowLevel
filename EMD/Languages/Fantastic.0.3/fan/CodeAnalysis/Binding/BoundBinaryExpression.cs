using System;

namespace Fantastic.CodeAnalysis.Binding {
    internal sealed class BoundBinaryExpression : BoundExpression {
        public override BoundNodeType Type => BoundNodeType.BinaryExpressionType;
        public override Type Kind => Left.Kind;
        public BoundExpression Left { get; }
        public BoundBinaryOperator OperatorType { get; }
        public BoundExpression Right { get; }

        public BoundBinaryExpression(BoundExpression left, BoundBinaryOperator operatorType, BoundExpression right) {
            Left = left;
            OperatorType = operatorType;
            Right = right;
        }
    }
}
