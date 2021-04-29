CC      = gcc
CFLAGS  = -std=c11 -Wall -Wextra -Wpedantic -Wstrict-aliasing
CFLAGS += -Iinclude
LDFLAGS =

SRC  = $(wildcard *.c)
OBJ  = $(SRC:.c=.o)

ASSEMBLER_OBJ = $(filter-out emulator.o, $(OBJ))
EMULATOR_OBJ  = $(filter-out assembler.o, $(OBJ))

.PHONY: all clean

all: emulator assembler

emulator: $(EMULATOR_OBJ)
	$(CC) -o emulator $^ $(LDFLAGS)

assembler: $(ASSEMBLER_OBJ)
	$(CC) -o assembler $^ $(LDFLAGS)

%.o: %.c
	$(CC) -o $@ -c $< $(CFLAGS)	

clean:
	rm -rf assembler emulator