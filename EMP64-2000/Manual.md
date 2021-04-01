# EMP64-2000 Devoloper Manual

___

## Contents

___

### Chapter One: Execution Environment

- [1.1](#11-modes-of-operation) Modes of Operation
- [1.2](#12-memory-organization) Memory Organization
- [1.3](#13-program-execution-registers) Program Execution Registers
- [1.4](#14-instruction-pointer) Instruction Pointer
- [1.5](#15-operand-size-and-address-size) Operand-Size and Address-Size
- [1.6](#16-operand-addressing) Operand Addressing

### Chapter Two: Data Types

- [2.1](#21-fundamental-data-types) Fundamental Data Types
- [2.2](#22-numeric-data-types) Numeric Data Types
- [2.3](#23-pointer-data-types) Pointer Data Types
- [2.4](#24-string-data-type) String Data Type

### Chapter Three: Instruction Set

- [3.1](#31-summary) Summary
- [3.2](#32-instructions) Instructions

### Chapter Four: Interrupts, and Exceptions

- [4.1](#41-interrupts-and-exceptions) Interrupts and Exceptions

___

## Chapter One - Execution Environment

___

### 1.1 Modes of Operation

There are 2 operation modes.

- **Direct Address Mode** - The CPU starts in this state, where all addresses are direct. More prone to access errors.

- **Virtual Address Mode** - This mode requires page tables to be setup, and uses virtual addresses. Not default because bootup code needs to setup a page table, then switch to this mode.

64-bit mode is always on.

You can also be in protected mode, where system information is limited, like the CPUID instruction.

### 1.2 Memory Organization

There are 2 memory models.

- **Flat Memory Model** - Single segment memory, used by default until segments are defined.

- **Segmented Memory Model** - Memory are seperated into segments to divide machine code, the stack, and data. Addresses are then interpreted where the first 16 bits are the segment, and the rest are the segment sub-address. Each segment can be up to 2^32 bytes, and there can be 2^16 segments.

### 1.3 Program Execution Registers

#### 1.3.1 General Purpose Registers

| Register Type | Registers |
|-|-|
| Byte Registers | AL, BL, CL, DL, DIL, SIL, BPL, SPL, R8B-R15B |
| Word Registers | AX, BL, CX, DX, DI, SI, BP, SP, R8W-R15W |
| Doubleword Registers | EAX, EBX, ECX, EDX, EDI, ESI, EBP, ESP, R8D-R15D |
| Quadword Registers | RAX, RBX, RCX, RDX, RDI, RSI, RBP, RSP, R8-R15 |
|

#### 1.3.2 Segment Registers

There are 3 segment registers. These are all 64-bit addresses that point to specific segments. These are all set to 0 in if the Flat Memory Model is being used.

- **CS** - Points to the code segement.
- **DS** - Points to the data segment.
- **SS** - Points to the stack segment.

#### 1.3.3 EFLAGS Register

This register has data about the processor state and arithmatic results.

| Bit | Summary |
|-|-|
| 0 | **Carry Flag** - On if an instruction has resulted in a overflowed result. |
| 1 | **Zero Flag** - On if an instruction has resulted in a zero result. |
| 2 | **Sign Flag** - On if an instructino has resulted in a negative result. |
| 3 | **Trap Flag** - Used for debuggers who want single-step interrupts. |
| 4 | **Interrupt Enable Flag** - On if maskable interrupts allow to interrupt CPU execution. |
| 5 | **Overflow Flag** - On if an instruction has resulted in a change of the destination sign bit. |
| 6 | **ID Flag** - On if CPUID instruction is enabled. |
| 7 | **Resume Flag** - Controls the CPU's response to debug interrupts. |
|

### 1.4 Instruction Pointer

The instruction pointer holds the address of where the next instruction will execute.

### 1.5 Operand Size and Address Size

The default operand sizes and address sizes are 64-bit, and are only changed by prefixes. This is for optimization of space, because mose operations will deal with 64-bit attributes.

### 1.6 Operand Addressing

A source operand can be:

- Immediate
- Register
- Memory
- I/O Port

A destination operand can be:

- Register
- Memory
- I/O Port

#### 1.6.1 Immediate Operand

This is a constant value that is stored in machine code.

```asm
MOV EAX, 14
```

#### 1.6.2 Register Operand

This is a register of any size.

```asm
MOV EAX, EBX
```

#### 1.6.3 Memory Operand

This is a memory location. This can point to the stack, data, or machine code.

```asm
MOV [0xFF], EAX
```

#### 1.6.4 I/O Port Operand

This is a port where bytes are located to share data on the data bus.

```asm
IN EAX, [0x01]
```

The address is actually an I/O port, not an address.

___

## Chapter Two - Data Types

___

### 2.1 Fundamental Data Types

There are 4 fundamental data types used by the EMP64 series.

| Name | Bits |
|-|-|
| Byte | 8 |
| Word | 16 |
| Doubleword (dword) | 32 |
| Quadword (qword) | 64 |
|

### 2.2 Numeric Data Types

All unsigned integers corespond to fundemental data types, e.g. Word Unsigned Integer.

Signed integers are the same, but the most significant bit is the sign bit. This is used for two's complement and one's complement.

There are only 2 float data types. Single Precision (32-bit) and Double Precision (64-bit).

#### 2.2.1 Single Precision

| 31 | 30-23 | 22-0 |
|-|-|-|
| Sign | Exponent | Value |
|

#### 2.2.2 Double Precision

| 63 | 62-52 | 51-0 |
|-|-|-|
| Sign | Exponent | Value |
|

The EMP64-2000 does not support Double Extended Precision (80-bit).

### 2.3 Pointer Data Types

Near pointers are a 64-bit address. Far pointers are a 64-bit address, where the most significant 16 bits are the segment selector.

### 2.4 String Data Types

Strings are a consecutive sequence of bytes. This was intended for ASCII encoding, but the conversions are handled by the kernel or some other software, so UTF encoding can be used.

___

## Chapter Three - Instruction Set

___

### 3.1 Summary

This as a quick reference table with all the current instructions for the EMP64-2000 specific processor.

| Opcode | Mnemonic | Summary |
|-|-|-|
| 0x00 | NOP | No operation |
| 0x01 | UD | Undefined |
| 0x02 | HLT | Halt until external interrupt |
| 0x03 | INT | Invoke interrupt |
| 0x04 | MOV | Move data to and from registers |
| 0x05 | PUSH | Push value onto stack |
| 0x06 | POP | Pop data from stack |
| 0x07 | CPUID | Get system information |
| 0x08 | CALL | Call procedure |
| 0x09 | RET | Return from procedure |
| 0x0A | JMP | Jump to address |
| 0x0B | SYSEXIT | Shuts down the CPU |
| 0x0C | CMP | Compares operands |
| 0x0D | JNE | Jumps of not equal |
|

### 3.2 Instruction Set

#### 3.2.1 NOP

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $00 | N/A | N/A |
|

No operation.

#### 3.2.2 UD

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $01 | N/A | N/A |
|

Raises an Invalid Opcode exceptions.

#### 3.2.3 HLT

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $02 | N/A | N/A |
|

Stops CPU from executing instructions until an external interrupt.

#### 3.2.4 INT

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $03 | r/m | N/A |
|

Raises an interrupt based on the interrupt code stored in Operand 1.

#### 3.2.5 MOV

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $04 | r/m | r/m |
|

Moves value in Operand 2 into Operand 1.

#### 3.2.6 PUSH

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $05 | r/m | N/A |
|

Puts Operand 1 into the address stored by the stack pointer, and the stack pointer decrements. LILO (Last In Last Out).

#### 3.2.7 POP

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $06 | r/m | N/A |
|

Takes value on top of stack and puts it into Operand 1.

#### 3.2.8 CPUID

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $07 | N/A | N/A |
|

Gets system information depending on what is stored in the RAX register.

#### 3.2.9 CALL

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $08 | r/m | N/A |
|

Pushes instruction pointer onto stack, then move Operand 1 into instruction pointer.

#### 3.2.10 RET

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $09 | N/A | N/A |
|

Pops value from stack into instruction pointer.

#### 3.2.11 JMP

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $0A | r/m | N/A |
|

Moves Operand 1 into instruction pointer.

#### 3.2.12 SYSEXIT

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $0B | N/A | N/A |
|

Shuts down the CPU.

#### 3.2.13 CMP

| Op | Operand 1 | Operand 2 |
|-|-|-|
| $0B | N/A | N/A |
|

Shuts down the CPU.

___

## Chapter Four - Interrupts, and Exceptions

___

### 4.1 Interrupts amd Exceptions

| Code | Description | Source |
|-|-|-|
| 0 | Divide Error | Division instructions |
| 1 | Debug | |
| 2 | Breakpoint | 0xCC instruction |
| 3 | Overflow | INT instruction |
| 4 | Invalid Opcode | UD instruction or reserved opcode |
| 5 | Double Fault | Any interrupt or exception |
| 6 | Segment Not Present | Loading a unexistent segment |
| 7 | Stack Segment Fault | Stack operations |
| 8 | Page Fault | Any memory reference |
| 9 | Math Fault | Floating-point instructions |
| 10 | Machine Check | |
| 11 | Protection Exception | Memory reference to reserved memory |
| 12 | Single Step Interrupt | Trap Flag |
| 12-31 | Reserved | |
| 32-255 | Maskable Interrupts | External interrupt, INT instruction |
|
