# Reversingx64

Reverse engineering the Intel x86_64 instruction set.

## MOV

- 0x48 prefix means that registers are 64-bit
- 0x66 prefix means 16-bit register mode

- 0x89 is the MOV opcode
- Next byte is as follows:
  - Mode (bits 7 and 6)
  - Op1 (bits 5-3)
  - Op2 (bits 2-0)

### Mode RegReg (0b11)

| Register | Code |
|-|-|
| EAX | 000 |
| ECX | 001 |
| EDX | 010 |
| EBX | 011 |
| ESP | 100 |
| EBP | 101 |
| ESI | 110 |
| EDI | 111 |

Note that the order for ops is source, then destination. This is the opposite of assembly annotation.

### Mode RegIm (?)

For RegIm the opcode contains the register. The first 5 bits are 10111, then the next three are the register. The next bytes are the immediate value.
