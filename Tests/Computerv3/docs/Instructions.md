# Instruction Set

## Contents

||||||||||||||
|-|-|-|-|-|-|-|-|-|-|-|-|-|
| ADC | ADD | AND | ASL | BRK | CLC | CLI | CMP | CPA | CPAC | CPB | CPC | CPD |
| DCA | DCAC | DCB | DCC | DCD | DEC | DIV | DVC | HLT | ICA | ICAC | ICB | ICC | ICD |
| IN | INC | JCC | JMP | JSR | LDA | LDAC | LDB | LDC | LDD | LSR | MLC | MUL |
| NOP | OR | OUT | POP | POPF | PUSH | PUSHF | ROL | ROR | RSR | RTI | SBC | SLC |
| SLI | STA | STAC | STB | STC | STD | SUB | TAS | TSA | XOR |
|

Clock cycles are used whenever you fetch a byte, or write a byte, +1 for the instruction.

## ADC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $A0 | 2 | 3 |
| Absolute | $A1 | 3 | 4 |
| Absolute EAX | $A2 | 3 | 5 |
| Absolute ECX | $A3 | 1 | 4 |
| Absolute EDX | $A4 | 1 | 4 |
|

## ADD

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $A5 | 2 | 3 |
| Absolute | $A6 | 3 | 4 |
| Absolute EAX | $A7 | 3 | 5 |
| Absolute ECX | $A8 | 1 | 4 |
| Absolute EDX | $A9 | 1 | 4 |
|

## AND

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $AA | 2 | 3 |
| Absolute | $AB | 3 | 4 |
| Absolute EAX | $AC | 3 | 5 |
| Absolute ECX | $AD | 1 | 4 |
| Absolute EDX | $AE | 1 | 4 |
|

## ASL

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Accumulator | $AF | 1 | 3 |
| Absolute | $B0 | 3 | 4 |
| Absolute EAX | $B1 | 3 | 5 |
| Absolute ECX | $B2 | 1 | 4 |
| Absolute EDX | $B3 | 1 | 4 |
|

## BRK

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $B4 | 1 | 6 |
|

## CLC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $B5 | 1 | 2 |
|

## CLI

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $B6 | 1 | 2 |
|

## CMP

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Absolute, Absolute | $B7 | 5 | 1 |
|

## CPA

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Absolute | $B8 | 3 | 1 |
|

## CPAC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Absolute | $B9 | 3 | 1 |
|

## CPB

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Absolute | $BA | 3 | 1 |
|

## CPC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Absolute | $BB | 3 | 1 |
|

## CPD

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Absolute | $BC | 3 | 1 |
|

## DCA

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $BD | 1 | 3 |
|

## DCAC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $BE | 1 | 3 |
|

## DCB

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $BF | 1 | 3 |
|

## DCC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $C0 | 1 | 3 |
|

## DCD

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $C1 | 1 | 3 |
|

## DEC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $CD | 1 | 3 |
| Absolute | $CE | 3 | 4 |
| Absolute EAX | $CF | 3 | 5 |
| Absolute ECX | $D0 | 1 | 4 |
| Absolute EDX | $D1 | 1 | 4 |
|

## DIV

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $C2 | 2 | 3 |
| Absolute | $C3 | 3 | 4 |
| Absolute EAX | $C4 | 3 | 5 |
| Absolute ECX | $C5 | 1 | 4 |
| Absolute EDX | $C6 | 1 | 4 |
|

## DVC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $C7 | 2 | 3 |
| Absolute | $C8 | 3 | 4 |
| Absolute EAX | $C9 | 3 | 5 |
| Absolute ECX | $CA | 1 | 4 |
| Absolute EDX | $CB | 1 | 4 |
|

## HLT

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $01 | 1 | ~Inf (Until Interupt) |
|

## ICA

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $D2 | 1 | 3 |
|

## ICAC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $D3 | 1 | 3 |
|

## ICB

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $D4 | 1 | 3 |
|

## ICC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $D5 | 1 | 3 |
|

## ICD

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $D6 | 1 | 3 |
|

## IN

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Port | $D7 | 2 | 3 |
|

## INC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $D8 | 1 | 3 |
| Absolute | $D9 | 3 | 4 |
| Absolute EAX | $DA | 3 | 5 |
| Absolute ECX | $DB | 1 | 4 |
| Absolute EDX | $DC | 1 | 4 |
|

## JCC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Bytes*+Imemdiate Byte | $DD | 5 | 5 |
| Immediate Bytes*+Absolute | $DE | 3 | 7 |
| Immediate Bytes*+Indirect | $DF | 3 | 9 |
|

* Requires 3 additional bytes containing compare instruction

## JMP

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Absolute | $E0 | 3 | 3 |
| Indirect | $E1 | 3 | 5 |
|

## JSR

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Absolute | $E2 | 3 | 4 |
|

## LDA

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $E3 | 2 | 3 |
| Absolute | $E4 | 3 | 4 |
| Absolute EAX | $E5 | 3 | 5 |
| Absolute ECX | $E6 | 1 | 4 |
| Absolute EDX | $E7 | 1 | 4 |
|

## LDAC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $E8 | 2 | 2 |
| Absolute | $E9 | 3 | 4 |
| Absolute EAX | $EA | 3 | 5 |
| Absolute ECX | $EB | 1 | 4 |
| Absolute EDX | $EC | 1 | 4 |
|

## LDB

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $ED | 2 | 3 |
| Absolute | $EE | 3 | 4 |
| Absolute EAX | $EF | 3 | 5 |
| Absolute ECX | $F0 | 1 | 4 |
| Absolute EDX | $F1 | 1 | 4 |
|

## LDC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $F2 | 2 | 3 |
| Absolute | $F3 | 3 | 4 |
| Absolute EAX | $F4 | 3 | 5 |
| Absolute ECX | $F5 | 1 | 4 |
| Absolute EDX | $F6 | 1 | 4 |
|

## LDD

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $F7 | 2 | 3 |
| Absolute | $F8 | 3 | 4 |
| Absolute EAX | $F9 | 3 | 5 |
| Absolute ECX | $FA | 1 | 4 |
| Absolute EDX | $FB | 1 | 4 |
|

## LSR

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $FC | 2 | 3 |
| Absolute | $FD | 3 | 4 |
| Absolute EAX | $FE | 3 | 5 |
| Absolute ECX | $FF | 1 | 4 |
| Absolute EDX | $CC | 1 | 4 |
|

## MLC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $02 | 2 | 3 |
| Absolute | $03 | 3 | 4 |
| Absolute EAX | $04 | 3 | 5 |
| Absolute ECX | $05 | 1 | 4 |
| Absolute EDX | $06 | 1 | 4 |
|

## MUL

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $07 | 2 | 3 |
| Absolute | $08 | 3 | 4 |
| Absolute EAX | $09 | 3 | 5 |
| Absolute ECX | $0A | 1 | 4 |
| Absolute EDX | $0B | 1 | 4 |
|

## NOP

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $00 | 1 | 3 |
|

## OR

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $0C | 2 | 3 |
| Absolute | $0D | 3 | 4 |
| Absolute EAX | $0E | 3 | 5 |
| Absolute ECX | $0F | 1 | 4 |
| Absolute EDX | $10 | 1 | 4 |
|

## OUT

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Port | $11 | 2 | 3 |
|

## POP

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Accumulator | $12 | 1 | 3 |
| Absolute | $13 | 3 | 5 |
| Implied* | $14 | 1 | 2 |
|

* Just pops and deletes the data

## POPF

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $15 | 1 | 3 |
|

## PUSH

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Accumulator | $16 | 1 | 3 |
| Absolute | $17 | 3 | 5 |
|

## PUSHF

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $18 | 1 | 3 |
|

## ROL

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Accumulator | $19 | 1 | 4 |
| Absolute | $1A | 3 | 5 |
| Absolute EAX | $1B | 3 | 6 |
| Absolute ECX | $1C | 1 | 5 |
| Absolute EDX | $1D | 1 | 5 |
|

## ROR

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Accumulator | $1E | 1 | 4 |
| Absolute | $1F | 3 | 5 |
| Absolute EAX | $20 | 3 | 6 |
| Absolute ECX | $21 | 1 | 5 |
| Absolute EDX | $22 | 1 | 5 |
|

## RSR

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $23 | 1 | 5 |
|

## RTI

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $23 | 1 | 5 |
|

## SBC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $24 | 2 | 3 |
| Absolute | $25 | 3 | 4 |
| Absolute EAX | $26 | 3 | 5 |
| Absolute ECX | $27 | 1 | 4 |
| Absolute EDX | $28 | 1 | 4 |
|

## SLC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $29 | 1 | 2 |
|

## SLI

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $2A | 1 | 2 |
|

## STA

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $2B | 2 | 3 |
| Absolute | $2C | 3 | 4 |
| Absolute EAX | $2D | 3 | 5 |
| Absolute ECX | $2E | 1 | 4 |
| Absolute EDX | $2F | 1 | 4 |
|

## STAC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $30 | 2 | 3 |
| Absolute | $31 | 3 | 4 |
| Absolute EAX | $32 | 3 | 5 |
| Absolute ECX | $33 | 1 | 4 |
| Absolute EDX | $34 | 1 | 4 |
|

## STB

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $35 | 2 | 3 |
| Absolute | $36 | 3 | 4 |
| Absolute EAX | $37 | 3 | 5 |
| Absolute ECX | $38 | 1 | 4 |
| Absolute EDX | $39 | 1 | 4 |
|

## STC

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $3A | 2 | 3 |
| Absolute | $3B | 3 | 4 |
| Absolute EAX | $3C | 3 | 5 |
| Absolute ECX | $3D | 1 | 4 |
| Absolute EDX | $3E | 1 | 4 |
|

## STD

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $3F | 2 | 3 |
| Absolute | $40 | 3 | 4 |
| Absolute EAX | $41 | 3 | 5 |
| Absolute ECX | $42 | 1 | 4 |
| Absolute EDX | $43 | 1 | 4 |
|

## SUB

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $44 | 2 | 3 |
| Absolute | $43 | 3 | 4 |
| Absolute EAX | $44 | 3 | 5 |
| Absolute ECX | $45 | 1 | 4 |
| Absolute EDX | $46 | 1 | 4 |
|

## TAS

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $47 | 1 | 2 |
|

## TSA

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Implied | $48 | 1 | 2 |
|

## XOR

| Address Mode | Opcode | Bytes | Clock Cycles |
|-|-|-|-|
| Immediate Byte | $49 | 2 | 3 |
| Absolute | $4A | 3 | 4 |
| Absolute EAX | $4B | 3 | 5 |
| Absolute ECX | $4C | 1 | 4 |
| Absolute EDX | $4D | 1 | 4 |
|
