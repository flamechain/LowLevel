using System;

namespace Fantastic.CodeAnalysis.Binding {
    internal sealed class BoundUnaryExpression : BoundExpression {
        public override BoundNodeType Type => BoundNodeType.UnaryExpressionType;
        public override Type Kind => Operand.Kind; 
        public BoundUnaryOperator OperatorType { get; }
        public BoundExpression Operand { get; }

        public BoundUnaryExpression(BoundUnaryOperator operatorType, BoundExpression operand) {
            OperatorType = operatorType;
            Operand = operand;
        }
    }
}
