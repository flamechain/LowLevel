from M6502 import *

def structHex(hex_, length, pre=False):
    struct = hex_[2:]
    while len(struct) < length:
        struct = '0' + struct
    if pre:
        struct = '0x' + struct
    return struct

def viewHex(list, view=0x0000, amount=10):
    print()
    structList = []
    struct = ''
    for i in range(len(list)//16):
        struct = colored(structHex(hex(i*16), 4, pre=True), 'grey')
        for j in range(16):
            struct += ' '
            value = structHex(hex(list[i*16+j]), 2)
            if value == '00':
                struct += colored(value, 'grey')
            else:
                struct += value
        structList.append(struct)
    for i in range(amount):
        try:
            print(structList[(view//16)+i])
        except:
            return
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - -')


def main():
    mem = Mem()
    cpu = CPU()
    cpu.Reset(mem)
    mem.Data[0xFFFC] = cpu.INS_JSR
    mem.Data[0xFFFD] = 0x42
    mem.Data[0xFFFE] = 0x42
    mem.Data[0x4242] = cpu.INS_LDA_IM
    mem.Data[0x4243] = 0x84
    cpu.Execute(8, mem)
    viewHex(mem.Data, view=0xFFF0, amount=2)
    viewHex(mem.Data, view=0x4242, amount=2)
    return 0

print('Program executed:', hex(main()))
