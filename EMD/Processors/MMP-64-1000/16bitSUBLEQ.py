import re

class CPU:
    def On(self, mem):
        mem = mem.data
        pc = [0]

        def get():
            pos = pc[0]
            pc[0] += 1 if pos < len(mem) else -pos
            return mem[pos]

        def fetch():
            return get() << 8 | get()

        while 1:
            a = fetch()
            b = fetch()
            res = ((mem[a] << 8) | mem[a + 1]) - ((mem[b] << 8) | mem[b + 1])
            loc = fetch()
            mem[a:a+1] = [(res & 0xFF00) >> 8 , res & 0xFF]
            ((mem[a] << 8) | mem[a + 1]) > 127 and [pc := [loc]]

class RAM:
    def __init__(self, size=0xFFF):
        self.data = []

        for i in range(size):
            self.data.append(0)

    def LoadFile(self, filename: str) -> None:
        with open(filename, 'rb') as f:
            binary = f.read().hex()
            binary = re.findall("..", binary)

            for i in range(len(binary)):
                self.data[i] = int(binary[i], 16)

ram = RAM(0xFFFF)
cpu = CPU()

ram.LoadFile('test.o')
cpu.On(ram)

# print(ram.data)
