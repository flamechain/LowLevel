import binascii

with open('\\'.join(__file__.split('\\')[:-1]) + '\\ASM\\test_code.prg', 'rb') as f:
    hexcode = binascii.hexlify(f.read())

hexcode = str(hexcode).strip("b'").strip("'")
for i in range(len(hexcode)//2):
    print(hexcode[i*2:i*2+2], end=' ')

# value = 128

# if (value & 0b10000000) and (value > 0):
#     value -= 0x100

# print(value)

# Bit7 = 1
# Value = 0b00000000
# print(bin(Value | (Bit7 << 7)))