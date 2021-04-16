#ifndef LEXER_H
#define LEXER_H

// TODO: Split SyntaxToken and SyntaxKind into seperate files and rename LInit and STInit both to Init. Consider switching to C++?

enum SyntaxKind {
};

struct SyntaxToken {
    SyntaxKind Kind;
    int Position;
    char Text[100];

    void (*STInit)(const struct SyntaxToken*, SyntaxKind kind, int position, char text[]);
};

struct Lexer {
    char Text[100];
    int Position;

    void (*LInit)(const struct Lexer*, char*);
    SyntaxToken (*NextToken)(const struct Lexer*);
    char (*Current)(const struct Lexer*);
    void (*Next)(const struct Lexer*)

};

void STInit(const struct SyntaxToken*, SyntaxKind kind, int position, char textp[]);

void LInit(const struct Lexer*, char text[]);
void NextToken(const struct Lexer*);

#endif
