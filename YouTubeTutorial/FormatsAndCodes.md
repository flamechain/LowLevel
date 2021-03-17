# Formats and Codes

## Register Codes

| Key | Meaning |
|-|-|
| E | Extended, 32-bit |
| X | General purpose |
| B | Byte |
||

| Mnemonic | Code | Notes |
|-|-|-|
| EAX | $0 | Syscall param |
| EBX | $1 | Index, syscall param |
| ECX | $2 | Loop counter, syscall param |
| EDX | $3 | Syscall param |
| ESI | $4 | Source index |
| EDI | $6 | Destination index |
| ESP | $5 | Stack pointer |
| EBP | $7 | Address Offset |
| AX | $8 | 16-bit |
| BX | $9 | 16-bit |
| CX | $A | 16-bit |
| DX | $B | 16-bit |
| BAX | $C | 8-bit |
| BBX | $D | 8-bit |
| BCX | $E | 8-bit |
| BDX | $F | 8-bit |
||

## Addressing Modes

| Summary | Code |
|-|-|
| Reg, Im16 | $06 |
| Reg, Im8 | $07 |
||

## Instruction Format

| Opcode | Mod | R/m | R/m |
|-|-|-|-|
| 1 byte | 1 byte (if required) | 1, 2, or 4 bytes or None | 1, 2, or 4 bytes or None |
||

## I/O Ports

| Name | Address |
|-|-|
| COM0 | $F0001 |
||
