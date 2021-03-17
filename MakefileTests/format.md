# Instruction Format

I want all instructions to be the same length for assembler simplicity

16 bit computer

| Opcode | Mode | Params |
|-|-|-|
| 1 byte | 1 byte | 3 bytes |

| Mode | Code | Summary | Size Distribution |
|-|-|-|-|
| RR | 000 | Register and Register | 1, 1 |
| Rm | 001 | Register and Displacement | 1, 2 |
| mR | 010 | Displacement and Register | 2, 1 |
| RI | 011 | Register and Immediate | 1, 2 |
| mI | 100 | Displacement and Immediate | 2, 1 |
| Ad | 101 | Displacement | 2 |
| IM | 110 | Immediate | 2 |
| IM8 | 111 | Immediate | 1 |

| Register | Code | Size | Use |
|-|-|-|-|
| EAX | 0000 | 16-bit | General, syscall param 1 |
| EBX | 0001 | 16-bit | General, syscall param 2 |
| ECX | 0010 | 16-bit | General, syscall param 3 |
| EDX | 0011 | 16-bit | General, syscall param 4 |
| ESI | 0100 | 16-bit | General |
| ESP | 0101 | 16-bit | General |
| EDI | 0110 | 16-bit | Procedure results |
| EBP | 0111 | 16-bit | Address offest |
| AX | 1000 | 8-bit | General |
| BX | 1001 | 8-bit | General |
| CX | 1010 | 8-bit | General |
| DX | 1011 | 8-bit | General |

Instructions:

- int, 0x0
- call, 0x1
- ret, 0x2

- jmp, 0x3
- cmp, 0x4
- je, 0x5
- jge, 0x6
- jne, 0x7

- dec, 0x8
- inc, 0x9

- push, 0xA
- pop, 0xB
- mov, 0xC

- add, 0xD
- sub, 0xE

- hlt, 0xF

Basic Syntax:

```asm
include utils.inc                   ; imports utils.asm

section .data                       ; variable section
    message: .ascii "Hello, world!" ; string
    msg_len: len message            ; length of string

section .code                       ; procedures

main PROC                           ; main
    mov eax, %ebp                   ; mov eax, value of ebp
    ret                             ; return, sets edi with return (default 0)
main END

section .text                       ; non-func instructions

_start:                             ; OS jumps here, auto global
    call main                       ; invokes function
    jmp exit                        ; jump to label

exit:                               ; exit label
    call clearReg                   ; function from utils, clears general registers
    ret                             ; return to OS
```
