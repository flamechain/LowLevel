import re

class EEPROM:
    def __init__(self):
        self.Data = []

        self.IO = 0
        self.WE = 0
        self.OE = 0
        self.CE = 0

    def A(self, address: int) -> None:
        if self.CE:
            if self.OE:
                if len(self.Data) <= address:
                    self.IO = 0

                else:
                    self.IO = self.Data[address]

            elif self.WE:
                while len(self.Data) <= address:
                    self.Data.append(0x0)

                self.Data[address] = self.IO


def EEPROM_PROGRAMMER(filename: str, storage: EEPROM) -> None:
    address = 0
    storage.CE = 1
    storage.WE = 1

    with open(filename, 'rb') as f:
        contents = f.read().hex()

    for i in re.findall('..', contents):
        storage.IO = int(i, 16)
        storage.A(address)
        address += 1

    storage.CE = 0
    storage.WE = 0
    print('Sucessfully wrote %d bytes' % address)

def WriteFile():
    data = bytearray()
    data.extend(bytes([i for i in range(256)]))
    with open('data.bin', 'wb') as f:
        f.write(data)

# WriteFile()
# myStorage = EEPROM()
# EEPROM_PROGRAMMER(filename='data.bin', storage=myStorage)
