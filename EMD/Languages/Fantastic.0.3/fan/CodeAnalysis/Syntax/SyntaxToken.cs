using System.Collections.Generic;
using System.Linq;

namespace Fantastic.CodeAnalysis.Syntax {
    /// <summary>
    /// Token with attributes for parsing
    /// </summary>
    public sealed class SyntaxToken : SyntaxNode {
        public override SyntaxType Type { get; }
        public int Position { get; }
        public string Text { get; }
        public object Value { get; }

        public SyntaxToken(SyntaxType type, int position, string text, object value) {
            Type = type;
            Position = position;
            Text = text;
            Value = value;
        }

        public override IEnumerable<SyntaxNode> GetChildren() {
            return Enumerable.Empty<SyntaxNode>();
        }
    }
}
