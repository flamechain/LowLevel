import sys
import re
import os

superpath = os.path.split('tools')[0]
sys.path.append(superpath)

from Source import Memory
from Codes import *
from CPU import CPU

def assemble(oldcode: str) -> bytearray:
    oldcode = oldcode.split('\n')
    code = []
    labels = {}
    variables = {}
    procs = {}
    consts = {}
    strings = {}
    regs64 = {'rax': 0, 'rbx': 1, 'rcx': 2, 'rdx': 3, 'rsi': 4, 'rdi': 5, 'r8': 8, 'r9': 9, 'r10': 10, 'r11': 11, 'r12': 12, 'r13': 13, 'r14': 14, 'r15': 15}
    regs32 = {'eax': 0, 'ebx': 1, 'ecx': 2, 'edx': 3, 'esi': 4, 'edi': 5, 'r8d': 8, 'r9d': 9, 'r10d': 10, 'r11d': 11, 'r12d': 12, 'r13d': 13, 'r14d': 14, 'r15d': 15}
    regs16 = {'ax': 0, 'bx': 1, 'cx': 2, 'dx': 3, 'si': 4, 'di': 5, 'r8w': 8, 'r9w': 9, 'r10w': 10, 'r11w': 11, 'r12w': 12, 'r13w': 13, 'r14w': 14, 'r15w': 15}
    regs8 = {'al': 0, 'bl': 1, 'cl': 2, 'dl': 3, 'sil': 4, 'dil': 5, 'r8b': 8, 'r9b': 9, 'r10b': 10, 'r11b': 11, 'r12b': 12, 'r13b': 13, 'r14b': 14, 'r15b': 15}
    section = None
    addr = 10
    start = None

    for i in oldcode:
        if not i.strip() == '':
            if ';' in i:
                if i.split(';')[0].strip() != '':
                    if i.startswith('    '):
                        code.append('    ' + i.split(';')[0].strip())

                    else:
                        code.append(i.split(';')[0].strip())

                    continue

                else:
                    continue

            code.append(i)

    for i in code:
        tokens = []

        for j in i.split(' '):
            if j not in ['\r', '\n', '']:
                tokens.append(j)

        i = i.replace('    ', '\t')

        if not i.startswith('\t'):
            if tokens == ['.bss']:
                section = 'bss'

            elif tokens == ['.text']:
                section = 'text'

            elif tokens == ['.data']:
                section = 'data'

            elif tokens == ['.code']:
                section = 'text'

            elif len(tokens) > 1:
                if tokens[1] == 'proc':
                    procs[tokens[0]] = addr

        else:
            if section == 'bss':
                variables[tokens[0]] = addr

                if tokens[1] == 'resb':
                    addr += int(tokens[2])

            elif section == 'data':
                variables[tokens[0]] = addr

                if tokens[2].startswith('"'):
                    if tokens[1] == 'db':
                        addr += len(' '.join(tokens[2:]).split('"')[1])
                        strings[tokens[0]] = ' '.join(tokens[2:]).split('"')[1]

                elif tokens[0] == '.const':
                    if tokens[2] == 'equ':
                        if tokens[3] == '$':
                            if tokens[4] == '-':
                                consts[tokens[1]] = len(strings[tokens[5]])

                    elif tokens[3] == 'db':
                        if tokens[3].startswith('0x'):
                            consts[tokens[1]] = int(tokens[3], 16)

                        else:
                            consts[tokens[1]] = int(tokens[3])

                elif tokens[1] == 'db':
                    addr += 1

                elif tokens[1] == 'dw':
                    addr += 2

                elif tokens[1] == 'dd':
                    addr += 4

                elif tokens[1] == 'dq':
                    addr += 8

            elif section == 'text':
                if tokens[0] == 'mov':
                    if tokens[2].startswith('['):
                        addr += 11
                        continue

                    elif tokens[1][:-1] in regs8:
                        addr += 4

                    elif tokens[1][:-1] in regs16:
                        addr += 5

                    elif tokens[1][:-1] in regs32:
                        addr += 7

                    elif tokens[1][:-1] in regs64:
                        addr += 11

                    if tokens[2] in regs16:
                        addr -= 1

                    elif tokens[2] in regs32:
                        addr -= 3

                    elif tokens[2] in regs64:
                        addr -= 7

                    if tokens[1][:-1] in variables:
                        if tokens[2] in regs8:
                            addr += 11

                        elif tokens[2] in regs16:
                            addr += 11 + 1

                        elif tokens[2] in regs32:
                            addr += 11 + 3

                        elif tokens[2] in regs64:
                            addr += 11 + 7

                elif tokens[0] in ['pop', 'push']:
                    if tokens[1][:-1] in (list(regs8.keys()) + list(regs16.keys()) + list(regs64.keys())):
                        addr += 3

                elif tokens[0] in ['ret', 'hlt', 'syscall', 'nop', 'cpuid']:
                    addr += 1

                elif tokens[0] == 'call':
                    addr += 10

                elif tokens[0] == 'db':
                    addr += len(tokens) - 1

    for i in code:
        if i == '_start:':
            start = addr

        elif i == 'end':
            start = addr

    binary = bytearray()
    binary.extend(bytes([
        Pre_64 | Addr_Im, JMP,
        (start & 0xFF00000000000000) >> 56,
        (start & 0xFF000000000000) >> 48,
        (start & 0xFF0000000000) >> 40,
        (start & 0xFF00000000) >> 32,
        (start & 0xFF000000) >> 24,
        (start & 0xFF0000) >> 16,
        (start & 0xFF00) >> 8,
        start & 0xFF]))

    for i in code:
        tokens = []

        for j in i.split(' '):
            if j not in ['\r', '\n', '']:
                tokens.append(j)

        i = i.replace('    ', '\t')

        if len(tokens) > 0:
            if tokens[0] == 'end':
                if 'main' in procs:
                    binary.extend(bytes([
                        Pre_64 | Addr_Im, CALL,
                        (procs['main'] & 0xFF00000000000000) >> 56,
                        (procs['main'] & 0xFF000000000000) >> 48,
                        (procs['main'] & 0xFF0000000000) >> 40,
                        (procs['main'] & 0xFF00000000) >> 32,
                        (procs['main'] & 0xFF000000) >> 24,
                        (procs['main'] & 0xFF0000) >> 16,
                        (procs['main'] & 0xFF00) >> 8,
                        procs['main'] & 0xFF,
                        RET
                    ]))

                return binary

        if i.startswith('\t'):
            if len(tokens) > 1:
                if tokens[1] == 'resb':
                    for i in range(int(tokens[2])):
                        binary.extend(bytes([0]))

                elif tokens[0] == 'mov':
                    mode = Addr_RegIm

                    if tokens[2].startswith('0x'):
                        value = int(tokens[2], 16)

                    elif tokens[2] in variables:
                        value = variables[tokens[2]]

                    elif tokens[2].startswith('['):
                        try:
                            value = variables[tokens[2].strip('[]')]

                        except KeyError as e:
                            print('Undefined variable %s' % e)
                            return

                        mode = Addr_RegDisp

                        if tokens[1][:-1] in regs8:
                            size = Pre_8
                            regcode = regs8[tokens[1][:-1]]

                        elif tokens[1][:-1] in regs16:
                            size = Pre_16
                            regcode = regs16[tokens[1][:-1]]

                        elif tokens[1][:-1] in regs32:
                            size = Pre_32
                            regcode = regs32[tokens[1][:-1]]

                        elif tokens[1][:-1] in regs64:
                            size = Pre_64
                            regcode = regs64[tokens[1][:-1]]

                        binary.extend(bytes([
                            size | mode, MOV, regcode,
                            (value & 0xFF00000000000000) >> 56,
                            (value & 0xFF000000000000) >> 48,
                            (value & 0xFF0000000000) >> 40,
                            (value & 0xFF00000000) >> 32,
                            (value & 0xFF000000) >> 24,
                            (value & 0xFF0000) >> 16,
                            (value & 0xFF00) >> 8,
                            value & 0xFF
                        ]))

                        continue

                    elif tokens[1][:-1] in variables:
                        mode = Addr_DispReg

                        if tokens[2] in regs8:
                            size = Pre_8
                            regcode = regs8[tokens[2]]

                        elif tokens[2] in regs16:
                            size = Pre_16
                            regcode = regs16[tokens[2]]

                        elif tokens[2] in regs32:
                            size = Pre_32
                            regcode = regs32[tokens[2]]

                        elif tokens[2] in regs64:
                            size = Pre_64
                            regcode = regs64[tokens[2]]

                        binary.extend(bytes([
                            size | mode, MOV,
                            (variables[tokens[1][:-1]] & 0xFF00000000000000) >> 56,
                            (variables[tokens[1][:-1]] & 0xFF000000000000) >> 48,
                            (variables[tokens[1][:-1]] & 0xFF0000000000) >> 40,
                            (variables[tokens[1][:-1]] & 0xFF00000000) >> 32,
                            (variables[tokens[1][:-1]] & 0xFF000000) >> 24,
                            (variables[tokens[1][:-1]] & 0xFF0000) >> 16,
                            (variables[tokens[1][:-1]] & 0xFF00) >> 8,
                            variables[tokens[1][:-1]] & 0xFF, regcode
                        ]))

                        continue

                    elif tokens[2] in consts:
                        value = consts[tokens[2]]

                    elif tokens[2] in (list(regs8.keys()) + list(regs16.keys()) + list(regs64.keys())):
                        mode = Addr_RegReg

                        if tokens[2] in regs8:
                            value = regs8[tokens[2]]
                            size = Pre_8

                            if tokens[1][:-1] in regs8:
                                value2 = regs8[tokens[1][:-1]]

                        elif tokens[2] in regs16:
                            value = regs16[tokens[2]]
                            size = Pre_16

                            if tokens[1][:-1] in regs16:
                                value2 = regs16[tokens[1][:-1]]

                        elif tokens[2] in regs32:
                            value = regs32[tokens[2]]
                            size = Pre_32

                            if tokens[1][:-1] in regs32:
                                value2 = regs32[tokens[1][:-1]]

                        elif tokens[2] in regs64:
                            value = regs64[tokens[2]]
                            size = Pre_64

                            if tokens[1][:-1] in regs64:
                                value2 = regs64[tokens[1][:-1]]

                    else:
                        value = int(tokens[2])

                    if mode == Addr_RegReg:
                        binary.extend([size | mode, MOV, value2, value])

                    elif tokens[1][:-1] in regs8:
                        binary.extend(bytes([Pre_8 | mode, MOV, regs8[tokens[1][:-1]], value]))

                    elif tokens[1][:-1] in regs16:
                        binary.extend(bytes([
                            Pre_16 | mode, MOV, regs16[tokens[1][:-1]],
                            (value & 0xFF00) >> 8,
                            value & 0xFF
                        ]))

                    elif tokens[1][:-1] in regs32:
                        binary.extend(bytes([
                            Pre_32 | mode, MOV, regs32[tokens[1][:-1]],
                            (value & 0xFF000000) >> 24,
                            (value & 0xFF0000) >> 16,
                            (value & 0xFF00) >> 8,
                            value & 0xFF
                        ]))

                    elif tokens[1][:-1] in regs64:
                        binary.extend(bytes([
                            Pre_64 | mode, MOV, regs64[tokens[1][:-1]],
                            (value & 0xFF00000000000000) >> 56,
                            (value & 0xFF000000000000) >> 48,
                            (value & 0xFF0000000000) >> 40,
                            (value & 0xFF00000000) >> 32,
                            (value & 0xFF000000) >> 24,
                            (value & 0xFF0000) >> 16,
                            (value & 0xFF00) >> 8,
                            value & 0xFF
                        ]))

                elif tokens[0] == 'pop':
                    if tokens[1] in regs64:
                        binary.extend(bytes([Pre_64 | Addr_Reg, POP, regs64[tokens[1]]]))

                elif tokens[0] == 'push':
                    if tokens[1] in regs64:
                        binary.extend(bytes([Pre_64 | Addr_Reg, PUSH, regs64[tokens[1]]]))

                elif tokens[0] == 'call':
                    if tokens[1] in procs:
                        binary.extend(bytes([
                            Pre_64 | Addr_Im, CALL,
                            (procs[tokens[1]] & 0xFF00000000000000) >> 56,
                            (procs[tokens[1]] & 0xFF000000000000) >> 48,
                            (procs[tokens[1]] & 0xFF0000000000) >> 40,
                            (procs[tokens[1]] & 0xFF00000000) >> 32,
                            (procs[tokens[1]] & 0xFF000000) >> 24,
                            (procs[tokens[1]] & 0xFF0000) >> 16,
                            (procs[tokens[1]] & 0xFF00) >> 8,
                            procs[tokens[1]] & 0xFF
                        ]))

                elif tokens[2].startswith('"'):
                    if tokens[1] == 'db':
                        for j in ' '.join(tokens[2:]).split('"')[1]:
                            binary.extend(bytes([ord(j)]))

                elif tokens[1] == 'equ':
                    if tokens[2] == '$':
                        if tokens[3] == '-':
                            binary.extend(bytes([len(strings[tokens[4]])]))

                elif tokens[1] == 'db':
                    if tokens[2].startswith('0x'):
                        value = int(tokens[2], 16)

                    elif tokens[2] == '?':
                        value = 0

                    else:
                        value = int(tokens[2])

                    binary.extend(bytes([value & 0xFF]))

                elif tokens[1] == 'dw':
                    if tokens[2].startswith('0x'):
                        value = int(tokens[2], 16)

                    elif tokens[2] == '?':
                        value = 0

                    else:
                        value = int(tokens[2])

                    binary.extend(bytes([
                        (value & 0xFF00) >> 8,
                        value & 0xFF
                    ]))

                elif tokens[1] == 'dd':
                    if tokens[2].startswith('0x'):
                        value = int(tokens[2], 16)

                    elif tokens[2] == '?':
                        value = 0

                    else:
                        value = int(tokens[2])

                    binary.extend(bytes([
                        (value & 0xFF000000) >> 24,
                        (value & 0xFF0000) >> 16,
                        (value & 0xFF00) >> 8,
                        value & 0xFF
                    ]))

                elif tokens[1] == 'dq':
                    if tokens[2].startswith('0x'):
                        value = int(tokens[2], 16)

                    elif tokens[2] == '?':
                        value = 0

                    else:
                        value = int(tokens[2])

                    binary.extend(bytes([
                        (value & 0xFF00000000000000) >> 56,
                        (value & 0xFF000000000000) >> 48,
                        (value & 0xFF0000000000) >> 40,
                        (value & 0xFF00000000) >> 32,
                        (value & 0xFF000000) >> 24,
                        (value & 0xFF0000) >> 16,
                        (value & 0xFF00) >> 8,
                        value & 0xFF
                    ]))

                elif tokens[0] == 'db':
                    for j in tokens[1:]:
                        if j.startswith('0x'):
                            if j.endswith(','):
                                j = j[:-1]

                            binary.extend(bytes([int(j, 16)]))

                        else:
                            binary.extend(bytes([int(j)]))

            elif tokens[0] == 'syscall':
                binary.extend(bytes([SYSCALL]))

            elif tokens[0] == 'ret':
                binary.extend(bytes([RET]))

            elif tokens[0] == 'hlt':
                binary.extend(bytes([HLT]))

            elif tokens[0] == 'nop':
                binary.extend(bytes([NOP]))

            elif tokens[0] == 'cpuid':
                binary.extend(bytes([CPUID]))

    return binary

def main(args: list):
    with open(superpath + args[0], 'r') as f:
        code = f.read()

    binary = assemble(code)

    if binary is None:
        return

    if args[1] == '-o':
        with open(superpath + args[2] + '.bin', 'wb') as f:
            f.write(binary)

if __name__ == "__main__":
    # main(sys.argv[1:])
    main(['helloworld.asm', '-o', 'helloworld'])
