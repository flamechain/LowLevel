import sys
import re

from Instructions import *

def assemble(code: str) -> bytearray:
    oldcode = code.split('\n')
    code = []
    labels = {}
    variables = {}
    section = None
    addr = 0

    regs32 = {'eax': 0, 'ebx': 1, 'ecx': 2, 'edx': 3, 'edi': 4, 'esi': 5, 'ebp': 6, 'esp': 7}

    for i in oldcode:
        if i.strip() != '':
            if ';' in i:
                i = i.split(';')[0]

                if i.strip() == '':
                    continue

            code.append(i)

    for i in code:
        tokens = i.strip('    ').split(' ')

        if not i.startswith('    '):
            if i.startswith('.'):
                section = tokens[0][1:]

            elif tokens[0].endswith(':'):
                labels[tokens[0][:-1]] = addr

        else:
            if section == 'bss':
                if tokens[0] == 'resb':
                    if tokens[1].startswith('0x'):
                        addr += int(tokens[1], 16)

                    elif len(tokens) > 2:
                        addr += int(tokens[1]) * int(tokens[3])

                    else:
                        addr += int(tokens[1])

            elif section == 'text':
                if tokens[0] == 'hlt':
                    addr += 1

                elif tokens[0] == 'mov':
                    if tokens[1] == 'dword':
                        addr += 13

                    elif tokens[1][:-1] in regs32:
                        addr += 7

    iso = bytearray()

    for i in code:
        tokens = i.strip('    ').split(' ')

        if not i.startswith('    '):
            if i.startswith('.'):
                section = tokens[0][1:]

            elif tokens[0].endswith(':'):
                labels[tokens[0][:-1]] = addr

        else:
            if section == 'bss':
                if tokens[0] == 'resb':
                    if tokens[1].startswith('0x'):
                        for i in range(int(tokens[1], 16)):
                            iso.extend(bytes([0]))

                    elif len(tokens) > 2:
                        for i in range(int(tokens[1]) * int(tokens[3])):
                            iso.extend(bytes([0]))

                    else:
                        for i in range(int(tokens[1])):
                            iso.extend(bytes([0]))

            elif section == 'text':
                if tokens[0] == 'hlt':
                    iso.extend(bytes([HLT]))

                elif tokens[0] == 'mov':
                    if tokens[1] == 'dword':
                        if tokens[3].startswith('0x'):
                            tokens[2] = int(tokens[2][1:-2], 16)
                            tokens[3] = int(tokens[3], 16)
                            iso.extend(bytes([Size32 | AddrDispIm, MOV,
                                (tokens[2] & 0xFF00000000000000) >> 56,
                                (tokens[2] & 0xFF000000000000) >> 48,
                                (tokens[2] & 0xFF0000000000) >> 40,
                                (tokens[2] & 0xFF00000000) >> 32,
                                (tokens[2] & 0xFF000000) >> 24,
                                (tokens[2] & 0xFF0000) >> 16,
                                (tokens[2] & 0xFF00) >> 8,
                                tokens[2] & 0xFF,
                                (tokens[3] & 0xFF000000) >> 24,
                                (tokens[3] & 0xFF0000) >> 16,
                                (tokens[3] & 0xFF00) >> 8,
                                tokens[3] & 0xFF
                            ]))

                    elif tokens[1][:-1] in regs32:
                        if tokens[2] in labels:
                            tokens[2] = labels[tokens[2]]
                            iso.extend(bytes([
                                Size32 | AddrRegIm, MOV, regs32[tokens[1][:-1]],
                                (tokens[2] & 0xFF000000) >> 24,
                                (tokens[2] & 0xFF0000) >> 16,
                                (tokens[2] & 0xFF00) >> 8,
                                tokens[2] & 0xFF
                            ]))

    return iso

def main(args: list) -> int:
    with open(args[0], 'r') as f:
        code = f.read()

    binary = assemble(code)

    with open(args[2], 'wb') as f:
        f.write(binary)

    return 0

if __name__ == "__main__":
    exitcode = main(sys.argv[1:])
    print('Assembled with code %d (%s)' % (exitcode, hex(exitcode)))
    # with open('main.asm', 'r') as f:
    #     code = f.read()
    # assemble(code)
