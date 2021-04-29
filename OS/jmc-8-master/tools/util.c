#include <util.h>

/* POSIX compliant getline implementation */
ssize_t getline(char **lineptr, size_t *n, FILE *stream) {
	if (lineptr == NULL || n == NULL || stream == NULL)
		return -1;

	size_t index = 0, size = 128;

	if (*lineptr)
		free(*lineptr);

	*lineptr = malloc(size);
	
	/* Check if the first character is EOF */
	char c = fgetc(stream);
	if (c == EOF) {
		**lineptr = '\0';
		return -1;
	}

	(*lineptr)[index++] = c;

	while ((c = fgetc(stream)) != EOF) {
		/* Expand the buffer if we have run out of space
		 * Add 1 to index so we always have enough space for the null terminator
		 */
		if ((index + 1) == size) {
			size = size + 128;
			*lineptr = realloc(*lineptr, size);
		}

		(*lineptr)[index++] = c;

		/* Include the newline character, but stop reading when it is found */
		if (c == '\n')
			break;
	}

	(*lineptr)[index] = '\0';

	/* Return for errors */
	if (ferror(stream))
		return -1;

	/* Return -1 if nothing was read */
	if (index == 0)
		return -1;

	*n = size;
	return index;
}