using System;

namespace Fantastic.CodeAnalysis.Binding {
    internal abstract class BoundExpression : BoundNode {
        public abstract Type Kind { get; }
    }
}
