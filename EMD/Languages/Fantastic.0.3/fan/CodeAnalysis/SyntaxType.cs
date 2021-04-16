using System;
using System.Collections.Generic;
using System.Linq;

namespace Fantastic.CodeAnalysis {
    enum SyntaxType {
        NumberToken = 0,
        WhitespaceToken = 1,
        PlusToken = 2,
        MinusToken = 3,
        StarToken = 4,
        ForeSlashToken = 5,
        LParenToken = 6,
        RParenToken = 7,
        InvalidToken = 8,
        EOFToken = 9,
        BinaryExpression = 10,
        NumberExpression = 11,
        ParenthesizedExpression = 12,
    }
}
