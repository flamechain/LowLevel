import sys
import re


def __clean_var(line):
    line = re.split(":| ", line)
    newline = []

    for i in line:
        if i != '':
            newline.append(i)

    return newline


def __clean_ins(line):
    line = re.split(",| ", line)
    newline = []

    for i in line:
        if i != '':
            newline.append(i)

    return newline


registers = {
    'eax': '000',
    'ebx': '001',
    'ecx': '010',
    'edx': '011'
}


def Assemble(assembly: str) -> bytearray:
    variables = {}
    truevars = {}
    labels = {}
    final = []

    code = assembly.split('\n')

    cur_lbl = None
    address = 0x4
    start = None

    for i in code:
        if i.startswith('.data'):
            cur_lbl = 'data'
        if i.startswith('.text'):
            cur_lbl = 'text'
        elif (cur_lbl == 'data') and (i.startswith('\t') or i.startswith('    ')):
            parts = __clean_var(i)
            variables[parts[0]] = address
            truevars[parts[0]] = []
            if parts[1] == '.ascii':
                parts[2] = ' '.join(parts[2:])
                if parts[2].startswith('"') and parts[2].endswith('"'):
                    for j in parts[2].replace('"', '').replace('\\n', '\n'):
                        value = '{0:b}'.format(ord(j))
                        final.append('0'*(8-len(value))+value)
                        address += 1
                        truevars[parts[0]].append(j)
            elif parts[1] == 'equ':
                if parts[2].startswith("$-"):
                    variables[parts[0]] = address
                    value = len(''.join(truevars[parts[2].strip('$-')]))
                    truevars[parts[0]] = value
                    value = '{0:b}'.format(value)
                    final.append('0'*(8-len(value))+value)
                    address += 1
            else:
                variables[parts[0]] = address
                truevars[parts[0]] = int(parts[1], 16)
                value = '{0:b}'.format(int(parts[1], 16))
                final.append('0'*(8-len(value))+value)
                address += 1
    
    start = address
    cur_lbl = None

    for i in code:
        if i.startswith('.data'):
            cur_lbl = 'data'
        elif i.startswith('.text'):
            cur_lbl = 'text'
        elif (cur_lbl == 'text') and (i.startswith('_start')):
            value = '{0:b}'.format(start & 0xFF)
            value = '0'*(8-len(value))+value
            final.insert(0, value)
            value = '{0:b}'.format((start & 0xFF00) >> 8)
            value = '0'*(8-len(value))+value
            final.insert(0, value)
            value = '{0:b}'.format((start & 0xFF0000) >> 16)
            value = '0'*(8-len(value))+value
            final.insert(0, value)
            value = '{0:b}'.format((start & 0xFF000000) >> 24)
            value = '0'*(8-len(value))+value
            final.insert(0, value)
        elif (cur_lbl == 'text') and i.startswith('    '):
            parts = __clean_ins(i)
            if parts[0] == 'mov':
                final.append('00000010')
                address += 1
                if parts[2] not in registers:
                    if parts[2].startswith('*'):
                        struct = '01' + registers[parts[1]]
                        if variables[parts[2].strip('*')] < 256:
                            struct += '010'
                            final.append(struct)
                            address += 1
                            value = '{0:b}'.format(variables[parts[2].strip('*')])
                            final.append('0'*(8-len(value))+value)
                            address += 1
                    else:
                        if parts[2] in variables:
                            parts[2] = hex(truevars[parts[2]])
                        if int(parts[2], 16) < 256:
                            struct = '10' + registers[parts[1]] + '000'
                            final.append(struct)
                            address += 1
                            value = '{0:b}'.format(int(parts[2], 16))
                            final.append('0'*(8-len(value))+value)
                            address += 1
                else:
                    struct = '00' + registers[parts[1]] + registers[parts[2]]
                    final.append(struct)
                    address += 1
            elif parts[0] == 'int':
                final.append('00000000')
                address += 1
                if parts[1] in variables:
                    parts[1] = hex(truevars[parts[1]])
                value = '{0:b}'.format(int(parts[1], 16))
                final.append('0'*(8-len(value))+value)
                address += 1

    return final


def main(argv: list) -> print:
    infile = argv[1]
    outfile = 'a.o'

    for i in range(len(argv[2:])):
        if argv[i+2] == "-o":
            outfile = argv[i+3]

    with open(infile, 'r') as f:
        contents = f.read()

    machine_code = Assemble(contents)

    with open(outfile, 'w') as f:
        f.write(''.join(machine_code))


if __name__ == "__main__":
    argv = sys.argv

    main(argv)
