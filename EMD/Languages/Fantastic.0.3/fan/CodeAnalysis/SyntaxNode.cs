using System;
using System.Collections.Generic;
using System.Linq;

namespace Fantastic.CodeAnalysis {
    abstract class SyntaxNode {
        public abstract SyntaxType Type { get; }
        public abstract IEnumerable<SyntaxNode> GetChildren();
    }
}
