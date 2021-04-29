; JMC-8 Fibbonacci test

; Number of iterations to run
.define ITERATIONS 5

; Start at the beginning of memory
.org 0

mw a, 1

; Set up the stack at 0x80FF
lda [0x80FF]
sw [0xFFFE], i
sw [0xFFFD], j

mw b, 1

jmp [$]

main:
	mw c, ITERATIONS	; C is the counter
	mw a, 0x01			; Starting numbers
	mw b, 0x01
	lda [.fib_1]
	jnz 1

.fib_1:
	sub c, 1			; Can be replaced with 'dec c' once macros are working
	cmp c, 0			; Check if our counter is zero
	and f, 0x20			; Use only the 'greater' bit of the flags register
	lda [.done]
	jnz f 

	add a, b			; Compute the next number in the sequence
	mw d, a				; D is our result
	lda [.fib_2]
	jnz 1

; Same thing as above except reverse A and B
.fib_2:
	sub c, 1
	cmp c, 0
	and f, 0x20
	lda [.done]
	jnz f

	add b, a
	mw d, b
	lda [.fib_1]
	jnz 1

; Result is in D
.done:
	lda [$]
	mw a, $.h
	mw b, $.l
	jnz 1