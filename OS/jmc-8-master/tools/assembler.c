#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdarg.h>
#include <ctype.h>

#include <util.h>
#include <jmc.h>

// JMC Assembler
// Single pass assembler that supports JMC-8 assembly language, JMC-8 microcode,
// and JMC-8/EZ16 instructions.
// 
// Functions internally as a pipeline:
// File -> Tokenizer -> Expander -> Assembler -> Patcher -> Object File

 // Current state of the assembler program 
enum AssemblerState { STATE_INIT, STATE_ASSEMBLE, STATE_ERROR } assembler_state;

// Represents a patch that needs to be made in the state byte array because an
// unknown label was encountered.
struct Patch {
    char *label;
    uintptr_t location;
};

// Used for the state input stack, essentially a file object wrapper which also
// keeps track of the current line number and the contents of the current line.
struct InputFile {
    char *filename;
    FILE *file;
    char *line;
    size_t lineno;
};

 // Macro used to quickly get a pointer to the current file in processing 
#define current_file (state.input_stack.array + (state.input_stack.size - 1))

 // Global assembler state variables 
struct State {
     // Initial input ASM file and output binary file path 
    char *input, *output;

     // List of patches (unknown labels and their locations in memory) 
    struct { size_t size; struct Patch *array; } patches;

     // Final output buffer 
    struct { size_t size; uint8_t *array; } bytes;

    // Stack of files being read into the assembler. Handled in this manner
    // for easy .include directives. Assembler finished when the size of the
    // input stack returns to zero.
    struct { size_t size; struct InputFile *array; } input_stack;

    // True if the .microcode macro was found ANYWHERE in any input file
    // It must be the first content of any microcode file
    bool microcode;

    // Origin of output. Only allowed to be set once.
    // Defaults to an origin of 0x0000
    // Not valid when .microcode is true
    struct { size_t address; bool set; } origin;
} state;

// Assembler macros (prefixed with '.')
enum Macro {
    MACRO_MICROCODE,    // Indicates a microcode file rather than regular asm
    MACRO_INCLUDE,      // Includes another file in-place
    MACRO_DEFINE,       // Defines what follows as a replacement for the symbol
    MACRO_ORG           // Sets the origin for the assembler to use
};

 // Forward declarations 
void cleanup();
void _assert(bool, bool, const char *, ...);
void push_file(char *);
void pop_file();
char *remove_comments(char **);
char *process_expressions(char **);

 // Prints the usage message to stdout
void print_usage() {
    printf(
        "JMC-8 Assembler                        \n"
        "USAGE:                                 \n"
        "   assembler [options] [file]          \n"
        "OPTIONS:                               \n"
        "   -o <file> to specify output file    \n"
        "   -h or --help to print this dialog   \n"
    );
}

// Assembler assertion based on specified condition
// Exits the program with exit code 1 if critical is true and condition is false
// Takes further parameters such that it acts like printf() that autoamatically
// appends a newline
void _assert(bool condition, bool critical, const char *format, ...) {
    if (condition) {
        return;
    }

    // Print the assembler state before the error 
    printf("[%s] ", assembler_state == STATE_INIT ? "INIT" : "ASSEMBLER");
    printf("ERROR: ");

    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);

    // TODO: Print file/line no
    if (current_file) {
        printf(" (%s:%i)", current_file->filename, current_file->lineno + 1);
    }

    printf("\n");

    if (critical) {
        cleanup();
        exit(1);
    }
}

 // Cleans up after the assembler 
void cleanup() {
    free(state.input);
    free(state.output);

     // Clean up the rest of the file stack 
    while (state.input_stack.size > 0) {
        pop_file();
    }
}

 // Pushes the file with the specified path to the top of the input stack 
void push_file(char *path) {
     // Open the file and ensure that there are no errors 
    FILE *file = fopen(path, "r");
    _assert(file, true, "Could not open file %s", strerror(errno));

     // Ensure space enough for this file pointer 
    state.input_stack.size++;
    state.input_stack.array = realloc(state.input_stack.array, state.input_stack.size * sizeof(struct InputFile));
    
     // Create the InputFile struct and add it to the end of the stack 
    state.input_stack.array[state.input_stack.size - 1]  = (struct InputFile) {
        .filename = strdup(path),
        .file = file,
        .line = NULL,
        .lineno = 0
    };
}

 // Pops (removes) the file from the top of the input stack and closes it 
void pop_file() {
    _assert(state.input_stack.size > 0, true, "[INTERNAL] Extra file popped from stack");

     // Free InputFile data 
    fclose(current_file->file);
    free(current_file->filename);

    if (current_file->line) {
        free(current_file->line);
    }

     // Decrement the stack size and realloc or free accordingly 
    state.input_stack.size--;
    size_t new_size = state.input_stack.size * sizeof(struct InputFile);

    if (new_size == 0) {
        free(state.input_stack.array);
        state.input_stack.array = NULL;
    } else {
        state.input_stack.array = realloc(state.input_stack.array, new_size);
    }
}

// Removes comments for a line, processes the string IN PLACE.
// If the line ended up being just a comment, then the lineptr is also set to
// NULL to indicate an empty string that was free'd.
char *remove_comments(char **lineptr) {
    // Replace the leftmost semicolon with a null terminating character
    // Only reallocate the string if we replaced the first character so the
    // string is now empty - otherwise, leave that extra space in the line for
    // the eventual macro expansion that will (probably) require some extra space.
    size_t len = strlen(*lineptr);

    for (int64_t i = (int64_t) len; i >= 0; i--) {
        if ((*lineptr)[i] == ';') {
            if (i == 0) {
                free(*lineptr);
                *lineptr = NULL;
            } else {
                (*lineptr)[i] = '\0';
            }

            break;
        }
    }

    return *lineptr;
}

// Capitalize every character in lineptr in-place
// Ignores anything within single or double quotes and takes escaped characters
// into account
char *capitalize(char **lineptr) {
    // In double quotes, in single quotes
    bool dq = false, sq = false;

    size_t len = strlen(*lineptr);
    for (size_t i = 0; i < len; i++) {
        // Get current character and previous character
        char *c = &(*lineptr)[i], *p = i == 0 ? '\0' : (c - 1);
        
        if (*c == '\"') {
            dq = dq ? (*p == '\\') : !sq;
        } else if (*c == '\'') {
            sq = sq ? (*p == '\\') : !dq;
        } else if (!dq && !sq) {
            *c = toupper(*c); // Uppercase character in place
        }
    }

    return *lineptr;
}

// Macro implementation for .microcode macro
void macro_microcode(const char *ln) {
    // Warn if line is any different than .microcode
    _assert(!strcmp(ln, ".MICROCODE"), false, "Warning: .microcode takes no arguments");

    // Set microcode flag, warn if it has already been set
    _assert(!state.microcode, false, "Warning: multiple .microcode");
    state.microcode = true;
}

// Macro implementation for .include macro
void macro_include(const char *ln) {

}

// Macro implementation for .define macro
void macro_define(const char *ln) {

}

// Macro implementation for .org macro
void macro_org(const char *ln) {

}

// Identifies the macro on on the specified line
// NOTE: Assumess ln starts with a '.' and is NOT a label (ends with :)
static enum Macro identify_macro(const char *ln) {
    // Get length of macro name and allocate stack space
    size_t len = strcspn(ln + 1, " ");
    char macro[len + 1];

    // Copy identifier into the string and null terminate
    memcpy(macro, ln + 1, len);
    macro[len] = '\0';

    // Indtify the macro with strcmp
    if (!strcmp(macro, "MICROCODE"))    { return MACRO_MICROCODE; }
    if (!strcmp(macro, "ORG"))          { return MACRO_ORG; }
    if (!strcmp(macro, "DEFINE"))       { return MACRO_DEFINE; }
    if (!strcmp(macro, "INCLUDE"))      { return MACRO_INCLUDE; }

    // Unknown macro
    _assert(false, true, "Invalid macro %s", macro);
    return 0;
}

// Handles macros
char *process_macros(char **lineptr) {
    size_t len = strlen(*lineptr);

    // Check that this line...
    // (1) is a macro (starts with .)
    // (2) is not a label (does not end with :)
    if ((*lineptr)[0] == '.' && (*lineptr)[len - 1] != ':') {
        enum Macro m = identify_macro(*lineptr);
        switch (m) {
            case MACRO_MICROCODE:   macro_microcode(*lineptr);  break;
            case MACRO_ORG:         macro_org(*lineptr);        break;
            case MACRO_DEFINE:      macro_define(*lineptr);     break;
            case MACRO_INCLUDE:     macro_include(*lineptr);    break;
            default: _assert(false, true, "[INTERNAL] Invalid enum Macro %i", m);
        }
    }

    return *lineptr;
}

int main(int argc, const char *argv[]) {
     // Initialize assembler state variables 
    assembler_state = STATE_INIT;

     // Parse options as specified in usage 
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-h") || !strcmp(argv[i], "--help")) {
            print_usage();
            exit(0);
        } else if (!strcmp(argv[i], "-o")) {
            _assert(i + 1 < argc, true, "Invalid options, try running with --help");
            state.output = strdup(argv[i + 1]);
        } else {
            _assert(!state.input, true, "More than one input file specified");
            state.input = strdup(argv[i]);
        }
    }

    _assert(state.input, true, "No input file specified");      

     // Assign the default output if one was not given 
    if (!state.output) {
        state.output = strdup("a.out");
    }

    assembler_state = STATE_ASSEMBLE;

     // Push the initial file to the top of the input stack 
    push_file(state.input);

    size_t read, length;

     // Stream files line by line and assemble  
    while (state.input_stack.size > 0) {
         // Read a line from the current file 
        read = getline(&current_file->line, &length, current_file->file);
        current_file->lineno++;

         // read == -1 either means EOF or error 
        if (read == (size_t) -1) {
            if (strlen(current_file->line) == 0) {
                pop_file();
            } else {
                _assert(false, true, "Error reading from file %s: %s", current_file->filename, strerror(errno));
            }

            continue;
        }

        // Duplicate the current line so we can operate on it in-place 
        char *line = strdup(current_file->line);

        // Remove extraneous whitespace 
        if (!trim(&line, " \t\n\r\v")) continue;

        // Remove comments 
        if (!remove_comments(&line)) continue;

        // Capitalize the line for further processing
        if (!capitalize(&line)) continue;

        // Process macros
        if (!process_macros(&line)) continue;
        
        printf("[PROCESSED] %s\n", line);
        free(line);
    }
}