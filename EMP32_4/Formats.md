# Formats and Code Tables

## Contents

- [Register Codes](#10-registers)
- [Addressing Modes](#20-addressing-modes)
- [Instruction Formats](#30-instruction-formats)
- [I/O Ports](#40-io-ports)

## 1.0 Registers

### 1.1 Key

| | Meaning |
|-|-|
| E | Extended, 32-bit |
| X | General purpose |
| B | Byte |
||

### 1.2 Register Codes

| Mnemonic | Code | Notes |
|-|-|-|
| EAX | $0 | Syscall param |
| EBX | $1 | Index, syscall param |
| ECX | $2 | Loop counter, syscall param |
| EDX | $3 | Syscall param |
| ESI | $4 | Source index |
| EDI | $6 | Destination index |
| ESP | $5 | Stack pointer |
| EBP | $7 | Base pointer |
| AX | $8 | 16-bit |
| BX | $9 | 16-bit |
| CX | $A | 16-bit |
| DX | $B | 16-bit |
| BAX | $C | 8-bit |
| BBX | $D | 8-bit |
| BCX | $E | 8-bit |
| BDX | $F | 8-bit |
||
| EAO | | Address offset |
||

## 2.0 Addressing Modes

### 2.1 Key

| | Meaning |
|-|-|
| Reg | Register |
| Disp32 | 32-bit value at 32-bit address |
| Disp16 | 16-bit value at 32-bit address |
| Disp8 | 8-bit value at 32-bit address |
| Im32 | 32-bit immediate value |
| Im16 | 16-bit immediate value |
| Im8 | 8-bit immediate value
||

### 2.2 Codes

| Summary | Code |
|-|-|
| Reg, reg | $00 |
| Reg | $01 |
| Reg, Disp32 | $02 |
| Reg, Disp16 | $03 |
| Reg, Disp8 | $04 |
| Reg, Im32 | $05 |
| Reg, Im16 | $06 |
| Reg, Im8 | $07 |
||
| Disp32, Im32 | $08 |
| Disp16, Im16 | $09 |
| Disp8, Im8 | $0A |
| Disp32, Disp32 | $0B |
| Disp16, Disp16 | $0C |
| Disp8, Disp8 | $0D |
| Disp32 | $0E |
| Disp16 | $0F |
| Disp8 | $10 |
||
| Im32, Im32 | $11 |
| Im16, Im16 | $12 |
| Im8, Im8 | $13 |
| Im32 | $14 |
| Im16 | $15 |
| Im8 | $16 |
||

## 3.0 Instruction Formats

### 3.1 Key

| | Meaning |
|-|-|
| Mod | Mode |
| R/m | Register/memory |
||

### 3.2 Formats

| Opcode | Mod | R/m | R/m |
|-|-|-|-|
| 1 byte | 1 byte (if required) | 1, 2, or 4 bytes, or none | 1, 2, or 4 bytes, or none |
||

### 4.0 I/O Ports

| Name | Address |
|-|-|
| COM0 | $F0001 |
| COM1 | $F0002 |
| COM2 | $F0003 |
| COM3 | $F0004 |
| COM4 | $F0005 |
| COM5 | $F0006 |
| COM6 | $F0007 |
| COM7 | $F0008 |
| COM8 | $F0009 |
| COM9 | $F000A |
||
