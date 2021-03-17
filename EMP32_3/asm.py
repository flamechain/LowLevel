import re
import argparse
import sys
import Instructions as Ins

def clean_file(code: list) -> list:
    '''Cleans useless whitespace and comments for parsing'''
    newcode = []

    for i in code:
        i = re.split(';|#|//', i)[0]

        if i.strip(' \n\t') != '':
            while i.endswith(' ') or i.endswith('\r') or i.endswith('\n'):
                i = i[:-1]

            if i.startswith('\t'):
                i = "    " + i[1:]
        
            newcode.append(i)

    return newcode

def error(message=None):
    '''Exits if error'''
    if message:
        print("assembler.py: error:", message)

    sys.exit()

def check_len(values: list, length: int, message=None) -> None:
    '''Checks length of tokens'''
    if len(values) != length:
        error(message)

registers = {
    'EAX': 0b000,
    'EBX': 0b001,
    'ECX': 0b010,
    'EDX': 0b011,
    'ESI': 0b100,
    'ESP': 0b101,
    'EDI': 0b110,
    'EBP': 0b111
}

packages = [
    'stdio'
]

def pass_one(code):
    variables = {}
    strings = {}
    procs = {}
    final = []
    labels = {}
    cur_sect = None
    entry = None
    addr = 0x0

    for i in code:
        tokens = re.split(',| ', i)
        oldtokens = tokens
        tokens = []

        for j in oldtokens:
            if j != '':
                tokens.append(j)

        if not i.startswith('    '):
            if tokens[0] == '_start:':
                entry = addr
                check_len(tokens, 1, "Invalid syntax: %s" % i)

            elif tokens[0].endswith(':'):
                labels[tokens[0][:-1]] = addr
                check_len(tokens, 1, "Invalid syntax: %s" % i)

            elif tokens[0] == 'section':
                cur_sect = tokens[1][1:]
                check_len(tokens, 2, "Sections only take 1 argument, name\n%s" % i)

            elif tokens[1] == 'proc':
                procs[tokens[0]] = addr
                check_len(tokens, 2, "Procedure tags take 1 argument, procedure name\n%s" % i)

            elif tokens[1] == 'endp':
                check_len(tokens, 2, "Procedure tags take 1 argument, procedure name\n%s" % i)

            elif tokens[0] == 'include':
                check_len(tokens, 2, "Include have 1 argument, package name\n%s" % i)

                if tokens[1] in packages:
                    with open('packages\\' + tokens[1] + '.asm', 'r') as f:
                        package_code = f.read().split('\n')
                        results = assemble(package_code, True)

                        for i in results[0]:
                            final.append(i)
                            addr += 1

                        for i in results[1]:
                            procs[i] = results[1][i]

                else:
                    error("Unknown package: %s" % tokens[1])

        else:
            if cur_sect == 'data':
                if not tokens[0].endswith(':'):
                    error("Variables must be declared with ':'\n %s" % i)

                if tokens[1] == 'ascii':

                    string = ' '.join(tokens[2:]).split('"')

                    if string[0] != '':
                        error("Ascii strings must be enclosed in double-quotes\n%s" % i)

                    for i in string[2].split(','):
                        if i.strip(' ') == '':
                            continue

                        string[1] += chr(int(i.strip(' ')))

                    variables[tokens[0][:-1]] = addr
                    strings[tokens[0][:-1]] = string[1]

                    for i in string[1].replace('\\n', '\n'):
                        final.append(ord(i))
                        addr += 1

                elif tokens[1] == 'byte':
                    if tokens[2] == '?':
                        tokens[2] = 0

                    else:
                        tokens[2] = int(tokens[2])

                    variables[tokens[0][:-1]] = addr
                    final.append(tokens[2])
                    addr += 1

                elif tokens[1] == 'len':
                    if tokens[2] in variables:
                        variables[tokens[0][:-1]] = addr
                        value = len(strings[tokens[2]])
                        final.append(value)
                        addr += 1

                    else:
                        error("Len must be of variable\n%s" % i)

            elif cur_sect == 'text':
                addr += 5

    return variables, procs, final, labels, entry

def assemble(code, stringed=False):
    code = clean_file(code)
    cur_sect = None

    instructions = {
        'NOP': Ins.NOP,
        'HLT': Ins.HLT,
        'MOV': Ins.MOV,
        'CALL': Ins.CALL,
        'INT': Ins.INT,
        'RET': Ins.RET,
        'JMP': Ins.JMP,
        'CMP': Ins.CMP,
        'JE': Ins.JE,
        'DEC': Ins.DEC,
        'INC': Ins.INC
    }

    variables, procs, final, labels, entry = pass_one(code)

    for i in code:
        tokens = re.split(',| ', i)
        oldtokens = tokens
        tokens = []

        for j in oldtokens:
            if j != '':
                tokens.append(j)

        if tokens[0].lower() == "section":
            cur_sect = tokens[1][1:]

        elif (cur_sect == 'text') and i.startswith('    '):
            results = instructions[tokens[0].upper()](tokens[1:], variables, procs, labels)
            for j in results:
                final.append(j)

    if stringed:
        return [final, procs]

    obj = bytearray()
    enHiH = (entry & 0xFF000000) >> 24
    enHiL = (entry & 0xFF0000) >> 16
    enLoH = (entry & 0xFF00) >> 8
    enLoL = entry & 0xFF
    obj.extend(bytes([enHiH]))
    obj.extend(bytes([enHiL]))
    obj.extend(bytes([enLoH]))
    obj.extend(bytes([enLoL]))

    for i in final:
        obj.extend(bytes([i]))

    return obj

def main(argv: list) -> None:
    '''Manages arguments and gets assembled machine code'''
    try:
        with open('build\\' + argv.i, 'r') as f:
            code = f.read()
            code = code.split('\n')

    except:
        error("No such file %s" % argv.i)

    binary = assemble(code)
    outfile = 'a'

    try:
        outfile = argv.o

    except:
        pass

    with open('build\\' + outfile + '.o', "wb") as f:
        f.write(binary)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('i', help="Input file to assemble into an object file.")
    # parser.add_argument('-o', help="Output file to store the object file. Default is a.o")
    # args = parser.parse_args()
    class Args:
        i = 'main.asm'
        o = 'main'

    main(Args)
