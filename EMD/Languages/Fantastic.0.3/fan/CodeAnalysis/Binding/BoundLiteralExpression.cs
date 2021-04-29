using System;

namespace Fantastic.CodeAnalysis.Binding {
    internal sealed class BoundLiteralExpression : BoundExpression {
        public override BoundNodeType Type => BoundNodeType.LiteralExpressionType;
        public override Type Kind => Value.GetType();
        public object Value { get; }

        public BoundLiteralExpression(object value) {
            Value = value;
        }
    }
}
