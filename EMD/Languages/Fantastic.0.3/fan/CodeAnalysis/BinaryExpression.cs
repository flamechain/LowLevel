using System;
using System.Collections.Generic;
using System.Linq;

namespace Fantastic.CodeAnalysis {
    sealed class BinaryExpression : ExpressionSyntax {
        public ExpressionSyntax Left { get; }
        public SyntaxNode Operator { get; }
        public ExpressionSyntax Right { get; }
        public override SyntaxType Type => SyntaxType.BinaryExpression;

        public BinaryExpression(ExpressionSyntax left, SyntaxToken operatorToken, ExpressionSyntax right) {
            Left = left;
            Operator = operatorToken;
            Right = right;
        }

        public override IEnumerable<SyntaxNode> GetChildren() {
            yield return Left;
            yield return Operator;
            yield return Right;
        }
    }
}
