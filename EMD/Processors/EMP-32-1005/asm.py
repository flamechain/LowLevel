from Encodings import *

iso = bytearray()

iso.extend(bytes([ord("R"), ord("W")]))

iso.extend(bytes([
    PUSH, ModIm << 4 | Size8 << 2, ord("A"),
    PUSH, ModIm << 4 | Size32 << 2, 0, 0, 0, 0,
    PUSH, ModIm << 4 | Size32 << 2, 0, 0, 0, 0,
    CALL, ModIm << 4 | Size32 << 2, 0, 0, 0x06, 0xb8,
    CALL, ModIm << 4 | Size32 << 2, 0, 0, 0x06, 0x81,
    JMP, ModIm << 4 | Size8 << 2, 23
]))

for i in range(512-26):
    iso.extend(bytes([0]))

for i in range(256):
    iso.extend(bytes([0x00, 0x00, 0x06, 0x80]))

for i in range(32):
    iso.extend(bytes([0x00, 0x00, 0x06, 0x80]))

iso.extend(bytes([SHUTDWN]))

code = [
    POP, ModReg << 4 | Size32 << 2, RegEDX,
    POP, ModReg << 4 | Size32 << 2, RegECX,
    POP, ModReg << 4 | Size32 << 2, RegEBX,
    POP, ModReg << 4 | Size8 << 2, RegAL,
    PUSH, ModReg << 4 | Size32 << 2, RegEDX,

    MOV, ModRegIm << 4 | Size32 << 2 | Size32, RegEDI, 0x00, 0x0b, 0x80, 0x00,
    MUL, ModRegIm << 4 | Size32 << 2 | Size8, RegEBX, 2,
    ADD, ModRegReg << 4 | Size32 << 2 | Size32, RegEDI, RegEBX,
    MUL, ModRegIm << 4 | Size32 << 2 | Size8, RegECX, 160,
    ADD, ModRegReg << 4 | Size32 << 2 | Size32, RegEDI, RegECX,
    SAL, ModRegIm << 4 | Size16 << 2 | Size8, RegAX, 8,
    OR, ModRegIm << 4 | Size16 << 2 | Size8, RegAX, 0x0f,
    MOV, ModRegdispReg << 4 | Size32 << 2 | Size16, RegEDI, RegAX,

    XOR, ModRegReg << 4 | Size32 << 2 | Size32, RegEAX, RegEAX,
    RET,

    # +55
    MOV, ModRegIm << 4 | Size32 << 2 | Size32, RegECX, 0x00, 0x0b, 0x80, 0x00,
    CMP, ModRegIm << 4 | Size32 << 2 | Size32, RegECX, 0x00, 0x0b, 0x9f, 0x40,
    JE, ModIm << 4 | Size32 << 2, 0, 0, 0x06, 0xb8 + 0xFF,
    MOV, ModRegdispIm << 4 | Size32 << 2 | Size8, RegECX, 0,
    INC, ModReg << 4 |
]

iso.extend(bytes(code))

for i in range(0xb797f - len(code)):
    iso.extend(bytes([0]))

msg = "Loaded 32-bit protected mode"

for i in msg:
    iso.extend(bytes([ord(i), 0x0F]))

for i in range(80*2*2 - (2*len(msg))):
    iso.extend(bytes([0]))

for i in "Booting from Hard Disk...":
    iso.extend(bytes([ord(i), 0x0F]))

for i in range(0x1dce):
    iso.extend(bytes([0]))

with open("boot.bin", 'wb') as f:
    f.write(iso)

# python asm.py; python qemu.py boot.bin
