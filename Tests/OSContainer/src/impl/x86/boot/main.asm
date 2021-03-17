global _start

section .text
bits 32
_start:
    mov dword [0xb8000], 0x2f4f2f4b
    hlt
