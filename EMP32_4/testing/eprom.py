from colr import color

class EEPROM:
    def __init__(self):
        self.Data = []

        # I/O Pins
        self.IO = 0

        self.WE = 0 # Write Enable
        self.OE = 0 # Output Enable
        self.CE = 0 # Chip Enable

    def A(self, address: int) -> None:
        if self.CE:
            if self.OE:
                self.IO = self.Data[address]

            elif self.WE:
                self.Data[address] = self.IO

eeprom = EEPROM()
eeprom.CE = 1
addr = 0

while True:
    toprint = ''
    eeprom.IO = 0b10101010
    eeprom.WE = 1
    eeprom.A(addr)
    eeprom.WE = 0
    eeprom.OE = 1

    for i in '{0:b}'.format(eeprom.IO).rjust(8, '0'):
        if i == '0':
            toprint += color(i, fore=(150, 0, 0))

        elif i == '1':
            toprint += color(i, fore=(250, 0, 0))

    print(toprint, end='\r')
    addr += 1

    if addr >= (2**11):
        break

    eeprom.OE = 0

print()
