#ifndef UTIL_H
#define UTIL_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

/* strutil.c */
char *trim(char **strptr, const char *characters);

/* util.c */
ssize_t getline(char **lineptr, size_t *n, FILE *stream);

#endif