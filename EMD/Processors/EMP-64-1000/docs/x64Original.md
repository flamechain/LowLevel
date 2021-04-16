# Key

## Complex Registers

**EFLAGS** (16-bits):

| Bit | Label | Description |
|-|-|-|
| 0 | CF | **Carry flag** |
| 1 | PF | **Parity Flag**. Set if even number of 1's. |
| 3 | | Unused |
| 4 | AF | **Auxilary Carry Flag**. On if carry or borrow involves bit 4 of EAX, or lower order 4 bits of operand. Used for BCD format. |
| 5 | | Unused |
| 6 | ZF | **Zero Flag**. |
| 7 | SF | **Sign Flag**. 1 if most significant bit is 1. 0 otherwise. |
| 8 | TF | **Trap Flag**. Single-step that generates an exception after every instruction that can be used by a debug program. |
| 9 | IF | **Interupt Enable Flag**. Set if INTR pin gets valued. |
| 10 | DF | **Direction Flag**. 1 if process string from high to low, 0 if low to high. |
| 11 | OF | **Overflow Flag**. On if result is too big or too small to fit in destination. |
| 12 | IO | **Input/Output Privilage Level Flag**. 0 is only OS and below functions. 1 is OS Services. 2 is Device Drivers. 3 is Application Programs. If the current task is greater than or equal to the privilage level, it can access I/O ports. High bit of IOPL. |
| 13 | PL | Low bit of IOPL. |
| 14 | NT | **Nested Task Flag**. Used in protection mode, on if a system task has invoked another using CALL instead of JMP. |
| 15 | ID | When on it allows the usage of the CPUID instruction. |
| 16 | RF | **Resume flag**. Used by debug registers DR7, DR6. Disables some exceptions. |
| 17 | VM | **Virtual 8086 Mode Flag**. High speed mode with less error detection. |
|

___

**CR0** (16-bits):

| Bit | Label | Description |
|-|-|-|
| 0 | PE | **Protected Mode Enable** |
| 1 | MP | **Monitor Co-Processor** |
| 2 | EM | **Emulation** |
| 3 | TS | **Task Switch** |
| 4 | ET | **Extension Type** |
| 5 | NE | **Numeric Error** |
| 6 | AM | **Alignment Mask** |
| 7 | NW | **Not-Write Through** |
| 8 | CD | **Cache Disable** |
| 9 | PG | **Paging** |
| 10 | | Unused |
| 11 | | Unused |
| 12 | | Unused |
| 13 | | Unused |
| 14 | | Unused |
| 15 | | Unused |
| 16 | WP | **Write Protect** |
| 17 | | Unused |
|

**CR3** (64-bits):

| Bit | Label | Description | Condition |
|-|-|-|-|
| 3 | PWT | **Page-Level Write Through** | CR4.PCIDE = 0 |
| 5 | PCD | **Page-Level Cache Disable** | CR4.PCIDE = 0 |
| 0-11 | PCID | | | CR4.PCIDE = 1 |
| 12-63 | **Physical Base Address of PML4** |
|

**CR4** (32-bits):

| Bit | Label | Description |
|-|-|-|
| 0 | VME | **Virtual-8086 Mode Extensions** |
| 1 | PVI | **Protected Mode Virtual Interrupts** |
| 2 | TSD | **Time Stamp Enable Only in Ring 0** |
| 3 | DE | **Debugging Extensions** |
| 4 | PSE | **Page Size Extension** |
| 5 | PAE | **Physical Address Extension** |
| 6 | MCE | **Machine Check Exception** |
| 7 | PGE | **Page Global Enable** |
| 8 | PCE | **Performance Monitoring Counter Enable** |
| 9 | OSFXSR | **OS Support for FXSAVE and FXRSTOR** |
| 10 | OSXMMEXCPT | **OS Support for Unmasked SIMD Floating Point Exceptions** |
| 11 | UMIP | **User-Mode Instruction Prevention (SGDT, SIDT, SLDT, SMSW, STR Disable)** |
| 12 | | Unused |
| 13 | VMXE | **Virtual Machine Extensions Enable** |
| 14 | SMXE | **Safer Mode Extensions Enable** |
| 15 | | Unused |
| 16 | | Unused |
| 17 | PCIDE | **PCID Enable** |
| 18 | OSXSAVE | **XSAVE And Processor Extended State Enable** |
| 19 | | Unused |
| 20 | SMEP | **Supervisor Mode Executions Protection Enable** |
| 21 | SMAP | **Supervisor Mode Access Protection Enable** |
| 22 | PKE | **Enable Protection Keys for User-Mode Pages** |
| 23 | CET | **Enable Control-Flow Enforcement Technology** |
| 24 | PKS | **Enable Protection Keys for Supervisor-Mode Pages** |
| 25-31 | | Unused |
|

**CR8** (8-bits):

| Bit | Description |
|-|-|
| 0-3 | **Priority** |
| 4-7 | Unused |
|

___

**IA32_EFER** (8-bits):

| Bit | Label | Description |
|-|-|-|
| 0 | SCE | **System Call Extensions** |
| 1 | LME | **Long Mode Enable** |
| 2 | LMA | **Long Mode Active** |
| 3 | NXE | **No-Execute Enable** |
| 4 | SVME | **Secure Virtual Machine Enable** |
| 5 | LMSLE | **Long Mode Segment Limit Enable** |
| 6 | FFXSR | **Fast FXSAVE/FXRSTOR** |
| 7 | TCE | **Translation Cache Extension** |
|

___

**DR0-DR3** (64-bits):

Contain up to 4 addresses for breakpoints to automatically be put in place.

**DR6** (32-bits):

Contains info about debug conditions and exceptions..

**DR7** (32-bits):

| Bit | Description |
|-|-|
| 0 | Local DR0 Breakpoint |
| 1 | Global DR0 Breakpoint |
| 2 | Local DR1 Breakpoint |
| 3 | Global DR1 Breakpoint |
| 4 | Local DR2 Breakpoint |
| 5 | Global DR2 Breakpoint |
| 6 | Local DR3 Breakpoint |
| 7 | Global DR3 Breakpoint |
| 16-17 | Conditions for DR0 |
| 18-19 | Size of DR0 Breakpoint |
| 20-21 | Conditions for DR1 |
| 22-23 | Size of DR1 Breakpoint |
| 24-25 | Conditions for DR2 |
| 26-27 | Size of DR2 Breakpoint |
| 28-29 | Conditions for DR3 |
| 30-31 | Size of DR3 Breakpoint |
|

___

**TR6** (64-bits):

Test Command Register

**TR7** (64-bits):

Test Data Register

___

**GDRT** (80-bits):

0-15 are the size of the GDT
16-79 are the starting address of the GDT

**LDTR** (64-bits):

Stores location of current LDT

**TR** (64-bits):

Stores location of current TSS

**IDTR** (80-bits):

0-15 are the size of the IDT
16-79 are the location of the IDT

## Descriptor Tables

**GDT**:

Global Descriptor Table that stores an entry on each routine, task, data, or code, and goes to that location to do a security check. Then stores results in invisible registers.

**LDT**:

Local Descriptor Table that each program creates for limiting memory accessing for that program.

**TSS**:

Task State Segment (info) about the running task.

| Offset | 0 - 31 |
|-|-|
| 0x04 | RSP0 (low) |
| 0x08 | RSP0 (high) |
| 0x0C | RSP1 (low) |
| 0x10 | RSP1 (high) |
| 0x14 | RSP2 (low) |
| 0x18 | RSP2 (high) |
| 0x24 | IST1 (low) |
| 0x20 | IST1 (high) |
| 0x24 | IST2 (low) |
| 0x28 | IST2 (high) |
| 0x2C | IST3 (low) |
| 0x30 | IST3 (high) |
| 0x34 | IST4 (low) |
| 0x38 | IST4 (high) |
| 0x3C | IST5 (low) |
| 0x40 | IST5 (high) |
| 0x44 | IST6 (low) |
| 0x48 | IST6 (high) |
| 0x4C | IST7 (low) |
| 0x50 | IST7 (high) |
| 0x64 | IOPB Offset |
|

**IDT**:

An Interupt Descripter Table entry contains.

Descripter Table Level is a Ring Level to prevent userspace exiting. Then the gate type, then the location to jump to and the length.

Gate Types:

| Bin | Type |
|-|-|
| 0101 | 32-bit Task Gate |
| 0110 | 16-bit Interrupt Gate |
| 0111 | 16-bit Trap Gate |
| 1110 | 32-bit Interrupt Gate |
| 1111 | 32-bit Trap Gate |
|

Interrupt Gates are for INT instruction. E.g. INT 50 will call the 50th Interrupt Gate Entry.

Trap Gate is similar, but doesn't automatically disable interrupts on entry and reenable on exit.

Task Gate switches to a different task using the TSS.

## All Registers

**Non-Floating Point**:

| 64-bit | 32-bit | 16-bit | 8-bit | Common Uses |
|-|-|-|-|-|
| RAX | EAX | AX | AL | Return value|
| RBX | EBX | BX | BL | |
| RCX | ECX | CX | CL | |
| RDX | EDX | DX | DL | |
| RSI | ESI | SI | SIL | Source Index |
| RDI | EDI | DI | DIL | Destination Index |
| RBP | EBP | BP | BPL | Base Pointer |
| RSP | ESP | SP | SPL | Stack Pointer |
| R8 | R8D | R8W | R8B | |
| R9 | R9D | R9W | R9B | |
| R10 | R10D | R10W | R10B | |
| R11 | R11D | R11W | R11B | |
| R12 | R12D | R12W | R12B | |
| R13 | R13D | R13W | R13B | |
| R14 | R14D | R14W | R14B | |
| R15 | R15D | R15W | R15B | |
|
| EIP | | | | Instruction Pointer |
| | | FLAGS | | Flags Register |
|

**Floating Point**:

| 128-bit | 80-bit | 64-bit |
|-|-|-|
| SSE0 | EES0 | MMX0 |
| SSE1 | EES1 | MMX1 |
| SSE2 | EES2 | MMX2 |
| SSE3 | EES3 | MMX3 |
| SSE4 | EES4 | MMX4 |
| SSE5 | EES5 | MMX5 |
| SSE6 | EES6 | MMX6 |
| SSE7 | EES7 | MMX7 |
| SSE8-15 | | |
|

**Extended**:

| 512-bit | 256-bit | 128-bit |
|-|-|-|
| ZMM0-31 | YMM0-31 | XMM0-31 |
|

## Addressing Modes

All instructions have a prefix if they support multiple sized addressing modes.

| Prefix | Meaning |
|-|-|
| 00 | 8-bit |
| 01 | 16-bit |
| 02 | 32-bit |
| 03 | 64-bit |
| 04 | 80-bit |
| 05 | 128-bit |
| 06 | 256-bit |
| 07 | 512-bit |
|

| Summary |
|-|-|
| Displacement |
| Immediate |
| Register |
| Register + Register |
| Register + Displacement |
| Register + Immediate |
| Displacement + Register |
|
| Register + (Register \* Scale) |
| (Register \* Scale) + Displacement |
|
