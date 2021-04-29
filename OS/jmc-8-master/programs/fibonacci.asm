; Fibonacci number calculator for JMC-8
; Also (sort of) acts as a kernel - this a test program that isn't dependent
; on the full OS environemnt
.org 0
.define COUNT 5

.microcode asjf
.microcode

; Set up registers
; A and B are operation registers, C is count, D is final

fibonacci:
	mw a, 1
	mw b, 0
	mw c, COUNT

.loop_a:
	add a, b
	sub c, 1
	jnz c, [loop_b]
	jmp [.done]

.loop_b:
	add b, a
	sub c, 1
	jnz c, [loop_a]
	jmp [.done]

.done:
	mw a, d
	jmp [$]