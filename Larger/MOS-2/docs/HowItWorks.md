# How It Works

This is a big file including how my MOSv2 works.

## Contents

- [Instruction Set](#instruction-set)
- [Data Types](#data-types)

## Instruction Set

This is the main instruction format I am using:

| op | rs | rt | rd | shamt | func |
|-|-|-|-|-|-|
| 6 bits | 5 bits | 5 bits | 5 bits | 5 bits | 6 bits |

- *op* is the opcode / instruction code
- *rs* and *rt* are the first and second registers
- *rd* is the destination register
- *shamt* is the shift amount when using shift instructions
- *func* selects an arithmetic instruction with *op*

I am also using this format for the load and store instructions:

| op | rs | rt | address |
|-|-|-|-|
| 6 bits | 5 bits | 5 bits | 16 bits |

- *op* is the opcode
- *rs* is the register for loads and stores, or arithmetic instructions
- *rt* is the destination
- *address* is an address for assisting in some instructions e.g. disk loading, disk writing, ram jumping...

And finally the last format im using for jump instructions:

| op | address|
|-|-|
| 6 bits | 26 bits |

- *op* is the opcode
- *address* is a 26 bit address. Flexible for future upgrades

Now the instructions im using.

| Name/Abbr. | Description | Opcode | Set |
|-|-|-|-|
| ADD | Add 2 values | 0x00 |
| AND | Logical AND | 0x04 |
| CMP | Compare 2 values | 0x0A |
| COPY | Stores main memory into disk | 0x1E |
| DCMT | Decrement a register | 0x20 |
| DIV | Divide 2 values | 0x03 |
| EXIT | Safe way to shutdown system | 0x1A |
| FETCH | Copy data from register to main memory | 0x1C |
| GET | Copy disk memory to main memory | 0x1B |
| HLT | Wait for event | 0x11 |
| IN | Get input from port | 0x0F |
| INMT | Increments a register | 0x1F |
| Jcc | Jump if Condition | 0x09 |
| JMP | Jump to address | 0x08 |
| LOAD | Copy data from main memory to register | 0x0B |
| LOOP | Decrement register until 0, then jump | 0x21 |
| MOV | Copy data from register to register | 0x0C |
| MUL | Multiply 2 values | 0x02 |
| NLFY | Uninitilize value | 0x17 |
| NOT | Logical NOT | 0x07 |
| NOP | No operation | 0x0D |
| OR | Logical OR | 0x05 |
| OUT | Send output to port | 0x0E |
| POP | Pop data from stack | 0x12 |
| POPF | Pop FLAGS register from stack | 0x13 |
| PUSH | Push data to the stack | 0x14 |
| PUSHF | Push FLAGS register to the stack | 0x15 |
| SIGN | Flip sign of signed number | 0x10 |
| SET | Create data address | 0x18 |
| START | Loads OS and runs | 0x1D |
| STORE | Copy data from main memory to disk | 0x19 |
| SUB | Subtract 2 values | 0x01 |
| WAIT | Wait until not busy | 0x16 |
| XOR | Logical XOR | 0x06 |

## Data Types

Im using the R-Type, J-Type, and I-Type memory code formats with 32 bit data width, so for normal values since I had 32 bits to work with, I had each data have a 4-bit header with info about the next 28 bits.

### Format

| Data Type | Signed Flag | Data |
|-|-|-|
| 3 bits | 1 bit (Only for signed values) | 29 bits (28 for signed values) |

### Data Type Codes

| Type | Code |
|-|-|
| Unsigned Int | 0x0 |
| Unsinged Float | 0x1 |
| Int | 0x2 |
| Float | 0x3 |
| Bool | 0x4 |
| Char | 0x5 |
| Array Header | 0x6 |
| Null | 0x7 |

### Complex Formats

Bool:

| Code | Null | Value |
|-|-|-|
| 100 | 28 bits | 1 bit |

Char:

| Code | Value |
|-|-|
| 101 | 29 bits |

Null:

| Code | Null |
|-|-|
| 111 | 29 bits |

Array Header:

| Code | Content Code | Address Allocation |
|-|-|-|
| 110 | 3 bits | 26 bits |

## Registers

There are a total possible 32 registers.

The first register is the FLAGS register, in this format:

| Carry | HLT | Zero | Sign | Overflow | Direction | Trap | Interupt |
|-|-|-|-|-|-|-|-|
| bit 0x7 | bit 0x6 | bit 0x5 | bit 0x4 | bit 0x3 | bit 0x2 | bit 0x1 | bit 0x0 |

- *Carry* is a status flag to show if the most recent ALU operation resulted in a carry
- *HLT* is a status flag that HLT instruction reads to see if something else has happened
- *Zero* is a status flag to show if the most recent ALU operation resulted in zero
- *Sign* is a status flag to show the sign of the most recent ALU operation
- *Overflow* is a status flag to show if the most recent ALU operation resulted in overflow
- *Direction* is a control flag to choose the direction of reading char arrays
- *Trap* is a control flag, and used for single step debugging
- *Interupt* is a control flag choosing if the CPU will react to external hardware interupts

The rest hold other types of data. The remaining are general purpose.

| Position | Type |
|-|-|
| 0x00 | FLAGS |
| 0x01 | Data |
| 0x02 | Data |
| 0x03 | Data |
| 0x04 | Data |
| 0x05 | Data |
| 0x06 | Data |
| 0x07 | Data |
| 0x08 | Data |
| 0x09 | Data |
| 0x0A | Data |
| 0x0B | Data |
| 0x0C | Data |
| 0x0D | Program Counter |
