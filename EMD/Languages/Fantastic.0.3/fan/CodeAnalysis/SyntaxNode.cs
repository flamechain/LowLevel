using System.Collections.Generic;

namespace Fantastic.CodeAnalysis {
    /// <summary>
    /// Base class node with a type from SyntaxType enum, and an ability to get accurate children for SyntaxTree
    /// </summary>
    public abstract class SyntaxNode {
        public abstract SyntaxType Type { get; }
        public abstract IEnumerable<SyntaxNode> GetChildren();
    }
}
