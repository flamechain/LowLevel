#include "mstring.h"

int IsNullOrWhiteSpace(char string[]) {
    if (string == NULL) {
        return 1;
    }
    
    for (int i=0; i < strlen(string); i++) {
        if (string[i] != ' ' && string[i] != '\r' && string[i] != '\t' && string[i] != '\n') {
            return 0;
        }
    }

    return 1;
}

void Strip(char* str, char c) {
    char *pr = str, *pw = str;
    while (*pr) {
        *pw = *pr++;
        pw += (*pw != c);
    }
    *pw = '\0';
}
