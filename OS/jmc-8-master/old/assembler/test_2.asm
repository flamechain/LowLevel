.org 0

; Stack pointer location
.define SPH 0xFFFF
.define SPL 0xFFFE

; Set up the stack at the first 256 bytes of RAM
lda [0x80FF]
sw [SPH], i
sw [SPL], j

jmp [the_call]

some_label:
	mw a, 1
	mw b, 3
	ret

the_call:
	call [some_label]
	jmp [$]

; This should never happen
mw d, 0x55