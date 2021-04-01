from Instructions import *

kernel = bytearray()

with open("kernel.iso", 'wb') as f:
    for i in range(0x400):
        kernel.extend(bytes([0]))

    kernel.extend(bytes([
        Size32 | AddrDispIm, MOV,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x0b, 0x80, 0x00,
        0x2f, 0x4f, 0x2f, 0x4b,
        HLT
    ]))

    for i in range(0xb8000):
        kernel.extend(bytes([0]))

    f.write(kernel)
