using System;
using System.Collections.Generic;
using System.Linq;

namespace Fantastic.CodeAnalysis {
    sealed class NumberExpression : ExpressionSyntax {
        public override SyntaxType Type => SyntaxType.NumberExpression;
        public SyntaxToken NumberToken { get; }

        public NumberExpression(SyntaxToken number) {
            NumberToken = number;
        }

        public override IEnumerable<SyntaxNode> GetChildren() {
            yield return NumberToken;
        }
    }
}
