; LW override that automatically loads I and J
LWA %r0, [%i1]:
	lda [%i1]
	lw %r0

; Override for register memory address	
LWA %r0, [%r1, %r2]:
	mw i, %r1
	mw j, %r2
	lw %r0
	
; SW override that automatically loads I and J
SWA [%i0], %r1:
	lda [%i0]
	sw %r1
	
; Override for register memory address
SWA [%r0, %r1], %r2:
	mw i, %r0
	mw j, %r1
	sw %r2

; Call a subroutine at a known location
CALL [%i0]:
	push (($ + 8) > 8)  	; 2 byte
	push (($ + 7) & 0xFF)  	; 2 bytes
	lda [%i0]       		; 3 bytes
	jnz 1           		; 1 byte
	
; Call a subroutine at an unknown location
CALL [%r0, %r1]:
	push (($ + 10) > 8)  	; 2 byte
	push (($ + 9) & 0xFF)  	; 2 bytes
	mw i, %r0				; 2 bytes
	mw j, %r1				; 2 bytes
	jnz 1					; 2 bytes

; Return from a subroutine
RET:
	pop i
	pop j
	jnz 1

; Unconditional jump to a register address
JMP [%r0, %r1]:
    mw i, %r0
    mw j, %r1
    jnz 1

; Unconditional jump to a constant address
JMP [%i0]:
    lda [%i0]
    jnz 1

; Jump if less than
JLT %r0, %x1:
	cmp %r0, %x1
	and f, 0x01
	jnz f

; Jump if less than or equal to
JLT %r0, %x1:
	cmp %r0, %x1
	and f, 0x03
	jnz f

; Jump if equal to
JEQ %r0, %x1:
	cmp %r0, %x1
	and f, 0x02
	jnz f

; Jump if greater than
JGT %r0, %x1:
	cmp %r0, %x1
	and f, 0x04
	jnz f

; Jump if greater than or equal to
JGT %r0, %x1:
	cmp %r0, %x1
	and f, 0x06
	jnz f

; Jump if zero
JZ %r0:
	jeq %r0, f
	
; Jump if carry
JC:
	and f, 0x08
	jnz f
	
; Jump if borrow
JB:
	and f, 0x10
	jnz f

; Jump if overflow
JO:
	and f, 0x20
	jnz f
	
; Bitwise NOT
NOT %r0:
	nor %r0, %r0

; Bitwise NAND
NAND %r0, %x1:
	and %r0, %x1
	not %r0

; Bitwise XNOR
XNOR %r0, %x1:
	mw f, %x1
	nand f, %r0
	or %r0, %x1
	and %r0, f

; Bitwise XOR
XOR %r0, %x1:
	mw f, %x1
	or f, %r0
	nand %r0, %x1
	and %r0, f
