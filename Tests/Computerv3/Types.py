class Bit:...

class Byte:
    def __init__(self, value):
        self.value = value

    def wrap(self):
        if self.value > 0b1111111111111111:
            self.value = 0
        if self.value < 0b0:
            self.value = 0b1111111111111111

    def wrapValue(self, value):
        if value > 0b1111111111111111:
            value = 0
        if value < 0b0:
            value = 0b1111111111111111
        return value

    def hex(self):
        return hex(self.value)

    def int(self):
        return int(self.value)

    def __add__(self, o):
        return Byte(self.wrapValue(self.value + Byte(o).value))

    def __sub__(self, o):
        return Byte(self.wrapValue(self.value - Byte(o).value))

    def __repr__(self):
        return self.value

    def __str__(self):
        return str(self.value)

class Word:...

class DWord:...

class QWord:...

class uBit:...

class uByte:...

class uWord:...

class uDWord:...

class uQWord:...
