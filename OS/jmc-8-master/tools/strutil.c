#include <util.h>

// Trims any characters matching 'characters' from the start and end of a string.
// The string is modified in-place. The string either ends up as NULL in the
// event that it had a length of 0 after the trim or it is a free()-able string. 
char *trim(char **strptr, const char *characters) {
	if (!strptr || !*strptr) {
		return NULL;
	}

	size_t len = strlen(*strptr);

	 // Trim off the start of the string and memmove accordingly 
	size_t start = 0;
	while ((*strptr)[start] != '\0' && strchr(characters, (*strptr)[start])) {
		start++;
	}

	 // Copy the string back onto itself 
	memmove(*strptr, (*strptr) + start, len - start);

	int64_t end = len - start - 1;
	while (end != -1 && (*strptr)[end] != '\0' && strchr(characters, (*strptr)[end])) {
		end--;
	}

	(*strptr)[end + 1] = '\0';

	// Free if the string is now empty. Realloc if the size difference is
	// greater than or equal to 50%.
	if (end == -1) {
		free(*strptr);
		*strptr = NULL;
	} else if ((len / (end + 2)) >= 2) {
		*strptr = realloc(*strptr, end + 2);
	}

	return *strptr;
}
