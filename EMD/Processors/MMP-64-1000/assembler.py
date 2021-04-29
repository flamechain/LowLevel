import sys

def clean(array: list) -> list:
    final = []

    for line in array:
        line = line.split(';')[0]
        line = ' '.join(line.split())

        if line != '':
            if line.startswith(':'):
                line = line.replace(' ', '')

            final.append(line)

    return final

def getval(string: str) -> int:
    string = string.lower()

    if string.startswith('0x'):
        return int(string, 16)

    elif string.startswith('0b'):
        return int(string, 2)

    elif string.endswith('h'):
        return int(string, 16)

    elif string.endswith('b'):
        return int(string, 2)

    return int(string)

def assemble(code: list) -> bytearray:
    code = clean(code)
    binary = bytearray()
    labels = {}
    variables = []
    values = []
    section = None
    addr = 0

    for line in code:
        if line.startswith(':'):
            addr += 6

        else:
            tokens = line.split()

            if tokens == ['.data']:
                section = 'data'

            elif tokens == ['.text']:
                section = '.text'

            elif tokens[0].endswith(':') and len(tokens) == 1:
                labels[tokens[0][:-1]] = addr

            elif tokens[1] == 'equ':
                if section == 'data':
                    variables.append(tokens[0])
                    values.append(getval(tokens[2]))

    section = None
    real_addr = 0

    for line in code:
        tokens = line[1:].split(',')

        if line == '.text':
            section = 'text'

        if line.startswith(':') and section == 'text':
            op1 = addr + variables.index(tokens[0]) * 2
            op2 = addr + variables.index(tokens[1]) * 2

            if len(tokens) == 2:
                segment = bytes([
                    (op1 & 0xFF00) >> 8,
                    op1 & 0xFF,
                    (op2 & 0xFF00) >> 8,
                    op2 & 0xFF,
                    ((real_addr + 6) & 0xFF00) >> 8,
                    (real_addr + 6) & 0xFF
                ])
            elif len(tokens) == 3:
                seglist = [
                    (op1 & 0xFF00) >> 8,
                    op1 & 0xFF,
                    (op2 & 0xFF00) >> 8,
                    op2 & 0xFF
                ]

                if tokens[2] == '$':
                    seglist.append(((real_addr) & 0xFF00) >> 8)
                    seglist.append((real_addr) & 0xFF)

                else:
                    op3 = addr + variables.index(tokens[2]) * 2
                    seglist.append((op3 & 0xFF00) >> 8)
                    seglist.append(op3 & 0xFF)

                segment = bytes(seglist)

            real_addr += 6
            binary.extend(segment)

    for i in range(len(variables)):
        binary.extend(bytes([(values[i] & 0xFF00) >> 8, values[i] & 0xFF]))

    return binary

def main(argv: list) -> int:
    try:
        with open(argv[1], 'r') as f:
            asm = f.readlines()
    except Exception as e:
        return 1

    try:
        binary = assemble(asm)
    except Exception as e:
        print(e)
        return 2

    try:
        with open(argv[1].removesuffix('.asm') + '.o', 'wb') as f:
            f.write(binary)
    except Exception as e:
        return 3

    return 0

if __name__ == "__main__":
    errno: int = main(sys.argv)
    # errno: int = main([0, 'test.asm'])
    print('Program exited with code %d (%s)' % (errno, hex(errno)))
