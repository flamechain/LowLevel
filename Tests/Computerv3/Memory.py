'''
Contains all memory storage types as classes
'''

import termcolor

class VirtualMemory:
    def __init__(self):
        '''Creates virtual memory'''
        self.Data = []
        self.address_length = 4
        self.MAX_MEMORY = 16**4
        for i in range(self.MAX_MEMORY):
            self.Data.append(0x00)

    def Wipe(self) -> None:
        '''Wipes all virutal memory'''
        for i in range(len(self.Data)):
            self.Data[i] = 0x00

    def ViewHex(self, view_range: range) -> None:
        '''Prints formatted hex of memory within given range'''

        def HexOfLength(value: int, length: int, include_0x=False):
            '''Creates a string in hex format of a specific length'''
            string = str(hex(value))[2:]
            string = '0'*(length-len(string)) + string
            if include_0x: string = '0x' + string
            string = string.upper().replace('X', 'x')

            return string

        print(termcolor.colored(f'{" " * (self.address_length+2)} 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F', 'grey'))
        HexData = []

        for i in range(len(self.Data)//16):
            string = termcolor.colored(HexOfLength(i*16, 4, include_0x=True), 'grey')

            for j in range(16):
                string += ' '
                value = HexOfLength(self.Data[i*16+j], 2)

                if value == '00':
                    string += termcolor.colored(value, 'grey')

                else:
                    string += value

            HexData.append(string)

        for i in view_range:
            try:
                print(HexData[i])

            except:
                return
