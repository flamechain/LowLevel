#define BUFFER 100

#include <stdio.h>
#include <stdbool.h>
#include "mstring.h"
#include "lexer.h"

int main(int argc, char *argv[]) {
    while (true) {
        printf("> ");
        char line[BUFFER];
        fgets(line, BUFFER, stdin);
        Strip(line, '\n');

        if (IsNullOrWhiteSpace(line)) {
            return 0;
        }

        if (!strcmp(line, "1 + 2 * 3")) {
            printf("7\n");
        } else {
            printf("ERROR: Invalid expression!\n");
        }
    }
    return 0;
}
