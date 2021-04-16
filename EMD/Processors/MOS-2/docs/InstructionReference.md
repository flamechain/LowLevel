# Instruction Reference

This gives details on how to use each instruction.

| Name/Abbr. | Description | Opcode | Set |
|-|-|-|-|
| [ADD](#add) | Add 2 values | 0x00 |
| [AND](#and) | Logical AND | 0x04 |
| [CMP](#cmp) | Compare 2 values | 0x0A |
| [COPY](#copy) | Stores main memory into disk | 0x1E |
| [DCMT](#dcmt) | Decrement a register | 0x20 |
| [DIV](#div) | Divide 2 values | 0x03 |
| [EXIT](#exit) | Safe way to shutdown system | 0x1A |
| [FETCH](#fetch) | Copy data from register to main memory | 0x1C |
| [GET](#get) | Copy disk memory to main memory | 0x1B |
| [HLT](#hlt) | Wait for event | 0x11 |
| [IN](#in) | Get input from port | 0x0F |
| [INMT](#inmt) | Increments a register | 0x1F |
| [Jcc](#jcc) | Jump if Condition | 0x09 |
| [JMP](#jmp) | Jump to address | 0x08 |
| [LOAD](#load) | Copy data from main memory to register | 0x0B |
| [LOOP](#loop) | Decrement register until 0, then jump | 0x21 |
| [MOV](#mov) | Copy data from register to register | 0x0C |
| [MUL](#mul) | Multiply 2 values | 0x02 |
| [NLFY](#nlfy) | Uninitilize value | 0x17 |
| [NOT](#not) | Logical NOT | 0x07 |
| [NOP](#nop) | No operation | 0x0D |
| [OR](#or) | Logical OR | 0x05 |
| [OUT](#out) | Send output to port | 0x0E |
| [POP](#pop) | Pop data from stack | 0x12 |
| [POPF](#popf) | Pop FLAGS register from stack | 0x13 |
| [PUSH](#push) | Push data to the stack | 0x14 |
| [PUSHF](#pushf) | Push FLAGS register to the stack | 0x15 |
| [SIGN](#sign) | Flip sign of signed number | 0x10 |
| [SET](#set) | Create data address | 0x18 |
| [START](#start) | Loads OS and runs | 0x1D |
| [STORE](#store) | Copy data from main memory to disk | 0x19 |
| [SUB](#sub) | Subtract 2 values | 0x01 |
| [WAIT](#wait) | Wait until not busy | 0x16 |
| [XOR](#xor) | Logical XOR | 0x06 |

## Registers

- **Rs** start register, node1
- **Rt** end register, node 2
- **Rd** result register, store node

## ADD

| opcode | Rs | Rt | Rd | Null |
|-|-|-|-|-|
| 000000 | 5 bits | 5 bits | 5 bits | 11 bits |

## AND

| opcode | Rs | Rt | Rd | Null |
|-|-|-|-|-|
| 000100 | 5 bits | 5 bits | 5 bits | 11 bits |

## CMP

| opcode | Rs | Rt | Null |
|-|-|-|-|
| 001010 | 5 bits | 5 bits | 16 bits |

## COPY

| opcode | RAM start | DISK address |
|-|-|-|
| 011110 | 10 bits | 16 bits |

## DCMT

| opcode | Rd | Null |
|-|-|-|
| 100000 | 5 bits | 21 bits |

## DIV

| opcode | Rs | Rt | Rd | Null |
|-|-|-|-|-|
| 000011 | 5 bits | 5 bits | 5 bits | 11 bits |

## EXIT

| opcode | Null |
|-|-|
| 011010 | 26 bits |

## FETCH

| opcode | Rs | RAM Address | Null |
|-|-|-|-|
| 011100 | 5 bits | 16 bits | 5 bits |

## GET

| opcode | DISK Address | RAM Address |
|-|-|-|
| 011011 | 16 bits | 10 bits |

## HLT

| opcode | Null |
|-|-|
| 010001 | 26 bits |

## IN

## INMT

| opcode | Rd | Null |
|-|-|-|
| 011111 | 5 bits | 21 bits |

## Jcc

| opcode | CMP Address | RAM Address |
|-|-|-|
| 001001 | 10 bits | 16 bits |

## JMP

| opcode | RAM Address | Null |
|-|-|-|
| 001000 | 16 bits | 10 bits |

## LOAD

| opcode | RAM Address | Rd | Null |
|-|-|-|-|
| 001011 | 16 bits | 5 bits | 5 bits |

## LOOP

| opcode | Rs | RAM Address | Null |
|-|-|-|-|
| 100001 | 5 bits | 16 bits | 5 bits |

## MOV

| opcode | Rs | Rd | Null |
|-|-|-|-|
| 001100 | 5 bits | 5 bits | 16 bits |

## MUL

| opcode | Rs | Rt | Rd | Null |
|-|-|-|-|-|
| 000010 | 5 bits | 5 bits | 5 bits | 11 bits |

## NLFY

| opcode | Rd | Null |
|-|-|-|
| 010111 | 5 bits | 21 bits |

## NOT

| opcode | Rs | Rt | Rd | Null |
|-|-|-|-|-|
| 000111 | 5 bits | 5 bits | 5 bits | 11 bits |

## NOP

| opcode | Null |
|-|-|
| 001101 | 26 bits |

## OR

| opcode | Rs | Rt | Rd | Null |
|-|-|-|-|-|
| 000101 | 5 bits | 5 bits | 5 bits | 11 bits |

## OUT

## POP

## POPF

## PUSH

## PUSHF

## SIGN

| opcode | Rs | Rt | Rd | Null |
|-|-|-|-|-|
| 010000 | 5 bits | 5 bits | 5 bits | 11 bits |

## SET

| opcode | Rd | Value | Null |
|-|-|-|-|
| 011000 | 5 bits | 19 bits | 2 bits |

## START

| opcode | Null |
|-|-|
| 011101 | 26 bits |

## STORE

| opcode | DISK Address | Mode | RAM Address |
|-|-|-|-|
| 011001 | 16 bits | 1 bit | 9 bits |

The mode tells if you want to rewrite a DISK Address (`0`) or append a DISK Address (`1`)

## SUB

| opcode | Rs | Rt | Rd | Null |
|-|-|-|-|-|
| 000001 | 5 bits | 5 bits | 5 bits | 11 bits |

## WAIT

| opcode | Null |
|-|-|
| 010110 | 26 bits |

## XOR

| opcode | Rs | Rt | Rd | Null |
|-|-|-|-|-|
| 000110 | 5 bits | 5 bits | 5 bits | 11 bits |
