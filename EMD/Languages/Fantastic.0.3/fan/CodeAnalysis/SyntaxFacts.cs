
namespace Fantastic.CodeAnalysis {
    /// <summary>
    /// Contains constant "facts" about the syntax (e.g. syntax rules)
    /// </summary>
    internal static class SyntaxFacts {
        public static int GetUnaryOperatorPrecedence(this SyntaxType type) {
            switch(type) {
                case SyntaxType.PlusToken:
                case SyntaxType.MinusToken:
                    return 3;

                default:
                    return 0;
            }
        }

        public static int GetBinaryOperatorPrecedence(this SyntaxType type) {
            switch(type) {
                case SyntaxType.StarToken:
                case SyntaxType.ForeSlashToken:
                    return 2;

                case SyntaxType.PlusToken:
                case SyntaxType.MinusToken:
                    return 1;

                default:
                    return 0;
            }
        }
    }
}
