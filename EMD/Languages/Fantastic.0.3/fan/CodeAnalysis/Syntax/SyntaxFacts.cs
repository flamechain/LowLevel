
namespace Fantastic.CodeAnalysis.Syntax {
    /// <summary>
    /// Contains constant "facts" about the syntax (e.g. syntax rules)
    /// </summary>
    internal static class SyntaxFacts {
        public static int GetUnaryOperatorPrecedence(this SyntaxType type) {
            switch(type) {
                case SyntaxType.PlusToken:
                case SyntaxType.MinusToken:
                case SyntaxType.BangToken:
                    return 5;

                default:
                    return 0;
            }
        }

        public static int GetBinaryOperatorPrecedence(this SyntaxType type) {
            switch(type) {
                case SyntaxType.StarToken:
                case SyntaxType.ForeSlashToken:
                    return 4;

                case SyntaxType.PlusToken:
                case SyntaxType.MinusToken:
                    return 3;
                
                case SyntaxType.DoubleAmpersandToken:
                    return 2;
                case SyntaxType.DoublePipeToken:
                    return 1;

                default:
                    return 0;
            }
        }

        public static SyntaxType GetKeywordType(string text) {
            switch(text) {
                case "true":
                    return SyntaxType.TrueKeyword;
                case "false":
                    return SyntaxType.FalseKeyword;
                default:
                    return SyntaxType.IdentifierToken;
            }
        }
    }
}
