# Computer v3 CPU Instruction Set

## **Contents**

- [Registers](#registers)
- [Addressing](#addressing)
- [Instructions](#instructions)
- [Reference](#reference)

## **Registers**

### ***Processor Status***

| Name | Purpose |
|-|-|
| Zero Flag | If last operation resulted in a zero |
| Sign Flag | If last operation resulted in bit 7 being on |
| Carry Flag | If last operation needed carry, or resulted in carry; Used as borrow in subtraction |
| Overflow Flag | If last operation resulted in an overflow |
| Trap | Requires interupt after each instruction |
| Break | If inside a break sequence |
| Interupt Disable | Prevent hardware interupts from halting the CPU |
| Unused | Always on, used to finish byte |
|

### ***EAX, EBX, ECX, EDX***

General purpose registers. ECX and EDX are 16 bit.

### ***I/O Register***

Register that contains the input and outputs.

### ***Program Counter***

16 bits that points to where the next instruction is in memory.

### ***Stack Pointer***

Points to where the most recent stack data is. Fixed between registers $0100 and $01FF.

### ***Accumulator***

Register where all the arithmatic and logic operations operate on.

## **Addressing**

There are 9 addressing modes.

| Name | Meaning |
|-|-|
| Accumulator | Operates on the Accumulator register, instead of having a seperate instruction |
| Immediate Byte | Pulls next byte from memory |
| Immediate Word | Pulls next word from memory |
| Absolute | Pulls next word from memory, and uses value from that address |
| Absolute EAX | Pulls next word from memory, adds the contents of the EAX register, and uses the value from that address |
| Absolute ECX | Uses ECX as address |
| Absolute EDX | Uses EDX as address |
| Port | Used for storing I/O for I/O Instructions only; Ports are perment at 0000 -> 0004; Needs 1 byte for Zero Page |
| Indirect | Used for jump tables |
|

## **Instructions**

### ***Load/Store Operations***

These instructions store and load data into registers and memory addresses.

| Name | Description | Affects Flags |
|-|-|-|
| LDAC | Loads Accumulator | [S, Z](#processor-status) |
| LDA | Loads EAX register | [S, Z](#processor-status) |
| LDB | Loads EBX register | [S, Z](#processor-status) |
| LDC | Loads ECX register | [S, Z](#processor-status) |
| LDD | Loads EDX register | [S, Z](#processor-status) |
| STAC | Stores Accumulator | |
| STA | Stores EAX register | |
| STB | Stores EBX register | |
| STC | Stores ECX register | |
| STD | Stores EDX register | |
|

### ***Stack Operations***

These instructions push and pop data from the stack.

| Name | Description | Affects Flags |
|-|-|-|
| PUSH | Pushes data to stack | |
| POP | Pops data from stack | [N, Z](#processor-status) |
| PUSHF | Pushes Processor Status to stack | |
| POPF | Pops Processor Status from stack | All |
| TSA | Transfer stack pointer to EAX | |
| TAS | Transfer EAX to stack pointer | |
|

### ***Logical***

Does bitwise operations on value.

| Name | Description | Affects Flags |
|-|-|-|
| AND | Logical AND | [N, Z](#processor-status) |
| XOR | Exclusive OR | [N, Z](#processor-status) |
| OR | Logical Inclusive OR | [N, Z](#processor-status) |
|

### ***Arithmetic***

Does arithmetic on values.

| Name | Description | Affects Flags |
|-|-|-|
| ADC | Add with carry | [N, O, Z, C](#processor-status) |
| ADD | Add | [N, O, Z](#processor-status) |
| SBC | Subtract with carry | [N, O, Z, C](#processor-status) |
| SUB | Subtract | [N, O, Z](#processor-status) |
| MLC | Multiply with carry | [N, O, Z, C](#processor-status) |
| MUL | Multiply | [N, O, Z](#processor-status) |
| DVC | Divide with carry | [N, O, Z, C](#processor-status) |
| DIV | Divide | [N, O, Z](#processor-status) |
| CMP | Compare 2 values | |
| CPAC | Compare with Accumulator |
| CPA | Compare with EAX | |
| CPB | Compare with EBX | |
| CPC | Compare with ECX | |
| CPD | Compare with EDX | |
|

### ***Increments & Decrements***

Increments and decrements values.

| Name | Description | Affects Flags |
|-|-|-|
| INC | Increment at memory location | [N, Z](#processor-status) |
| DEC | Decrement at memory location | [N, Z](#processor-status) |
| ICAC | Increment Accumulator | [N, Z](#processor-status) |
| ICA | Increment EAX | [N, Z](#processor-status) |
| ICB | Increment EBX | [N, Z](#processor-status) |
| ICC | Increment ECX | [N, Z](#processor-status) |
| ICD | Increment EDX | [N, Z](#processor-status) |
| DCAC | Decrement Accumulator | [N, Z](#processor-status) |
| DCA | Increment EAX | [N, Z](#processor-status) |
| DCB | Increment EBX | [N, Z](#processor-status) |
| DCC | Increment ECX | [N, Z](#processor-status) |
| DCD | Increment EDX | [N, Z](#processor-status) |
|

### ***Shifts***

Shifts value.

| Name | Description | Affects Flags |
|-|-|-|
| ASL | Shift Left | [N, Z, C](#processor-status) |
| LSR | Shift Right | [N, Z, C](#processor-status) |
| ROL | Rotate Left | [N, Z, C](#processor-status) |
| ROR | Rotate Right | [N, Z, C](#processor-status) |
|

### ***Jumps***

Jumps to another address.

| Name | Description | Affects Flags |
|-|-|-|
| JMP | Jumps to address | |
| JSR | Jump to subroutine | |
| RSR | Return from subroutine | |
| JCC | Jump if compare | |
|

### ***Flag Changes***

Changes status flags.

| Name | Description | Affects Flags |
|-|-|-|
| CLI | Clear interrupt disable flag | [I](#processor-status) |
| CLC | Clear carry flag | [C](#processor-status) |
| STI | Set interrupt disable flag | [I](#processor-status) |
| STC | Set carry flag | [C](#processor-status) |

### ***System Functions***

Changes system state, and misc. instructions.

| Name | Description | Affects Flags |
|-|-|-|
| NOP | No operation | |
| BRK | Create interupt | [B](#processor-status) |
| RTI | Return from interupt | All |
| HLT | Sleep CPU until input | |
| IN | Gets input from port | |
| OUT | Sends output to port | |
|
