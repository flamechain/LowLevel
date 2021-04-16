#include "lexer.h"

void STInit(const struct SyntaxToken* this, SyntaxKind kind, int position, char text[]) {
    this.Kind = kind;
    this.Position = position;
    this.Text = text;
}

void LInit(const struct Lexer* this, char text[]) {
    this.Text = text;
}

SyntaxKind NextToken(const struct Lexer* this) {
    if ()
}
