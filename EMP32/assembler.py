import re
import argparse
import sys
import instructions as ins


def clean_file(code: list) -> list:
    '''Cleans useless whitespace and comments for parsing'''
    newcode = []

    for i in code:
        if ';' in i:
            i = i.split(';')[0]

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

res = 0

packages = {
    'EMPIrvine': {'ReadChar': [0, 2, [0x0C, 0xCC]], 'WriteString': [0, 2, [0x0C, 0xCD]]}
}


def parse_precode(code: list) -> tuple:
    '''Parses sections, labels, variables, globals, etc. First Pass.'''
    variables = {}
    labels = {}
    final = []
    procs = {}
    sections = []
    cur_sect = None
    addr = 0x0
    entry = None

    for i in code:
        tokens = re.split(',| ', i)
        if not i.startswith("    "):

            if tokens[0].lower() == 'section':
                if not tokens[1].startswith('.'):
                    error("Sections must start with section classifier, '.'")
                
                sections.append(tokens[1][1:])
                cur_sect = tokens[1][1:]
                check_len(tokens, 2, "Section keyword only takes 1 argument, section name")

            elif tokens[0].endswith(':'):
                check_len(tokens, 1, "Invalid syntax: %s" % i)

                if tokens[0] == '_start:':
                    entry = addr

                else:
                    labels[tokens[0][:-1]] = addr

            elif tokens[1].upper() == 'PROC':
                check_len(tokens, 2, "Invalid syntax: %s" % i)
                procs[tokens[0]] = [addr, None]

            elif tokens[1].upper() == 'ENDP':
                check_len(tokens, 2, "Invalid syntax: %s" % i)
                procs[tokens[0]][1] = addr

            elif tokens[0].upper() == 'INCLUDE':
                check_len(tokens, 2, "Include have 1 argument, package name\n%s" % i)

                if tokens[1] in packages:
                    for i in packages[tokens[1]]:
                        procs[i] = packages[tokens[1]][i][:2]

                        for i in packages[tokens[1]][i][2]:
                            final.append(i)
                            addr += 1


                else:
                    error("Unknown package: %s" % tokens[1])

        else:
            oldtokens = tokens
            tokens = []

            for j in oldtokens:
                if j != '':
                    tokens.append(j)

            if cur_sect in ['text', 'code']:
                if tokens[0] in ['hlt', 'ret']:
                    addr += 1
                elif tokens[0] in ['call']:
                    addr += 3
                else:
                    addr += 2

                    if len(tokens) > 1:
                        if tokens[1] not in registers:
                            addr += 4

                    if len(tokens) > 2:
                        if tokens[2] not in registers:
                            if tokens[2].upper() == 'OFFSET':
                                if tokens[3] in variables:
                                    addr += len(variables[tokens[3]])
                            addr += 4

            elif cur_sect == 'data':
                if not tokens[0].endswith(':'):
                    error("Variables must be declared with ':'\n %s" % i)

                if tokens[1] == '.ascii':

                    string = ' '.join(tokens[2:]).split('"')

                    if string[0] != '':
                        error("Ascii strings must be enclosed in double-quotes\n%s" % i)

                    for i in string[2].split(','):
                        string[1] += chr(int(i.strip(' ')))

                    variables[tokens[0][:-1]] = string[1]

                elif tokens[1] == 'len':
                    check_len(tokens, 3, "To many values passed into %s" % tokens[0][:-1])

                    if tokens[2] in variables:
                        if isinstance(variables[tokens[2]], str):
                            variables[tokens[0][:-1]] = len(variables[tokens[2]])

                        else:
                            error("Can only take the length of ascii strings")

                    else:
                        error("Unknown variable %s" % tokens[2])

                else:
                    global res

                    line = "global res; res = " + ' '.join(tokens[1:])
                    splitline = line.split(' ')
                
                    for j in range(len(splitline)):
                        if splitline[j] in variables:
                            splitline[j] = str(variables[splitline[j]])
                    
                    line = ' '.join(splitline)
                    exec(line, globals(), locals())
                    variables[tokens[0][:-1]] = res

    return final, sections, labels, variables, entry, procs


def assemble(code: list) -> bytearray:
    '''Assembles code and returns it in binary form'''
    code = clean_file(code)
    cur_sect = None
    cur_proc = None
    addr = 0
    final, sections, labels, variables, entry, procs = parse_precode(code)

    instructions = {
        'BRK': ins.BRK,
        'NOP': ins.NOP,
        'ADD': ins.ADD,
        'SUB': ins.SUB,
        'MUL': ins.MUL,
        'DIV': ins.DIV,
        'MOV': ins.MOV,
        'JMP': ins.JMP,
        'JCC': ins.Jcc,
        'CMP': ins.CMP,
        'HLT': ins.HLT,
        'CALL': ins.CALL
    }

    for i in code:
        tokens = re.split(',| ', i)
        oldtokens = tokens
        tokens = []

        for j in oldtokens:
            if j != '':
                tokens.append(j)

        if tokens[0].lower() == "section":
            cur_sect = tokens[1][1:]
        
        elif (cur_sect == "text") and i.startswith("    "):
            results = instructions[tokens[0].upper()](addr, tokens[1:], variables, procs)
            addr = results[0]
            for j in results[1]:
                final.append(j)

        elif (cur_sect == "code"):
            if not i.startswith('    '):
                if tokens[1] == 'PROC':
                    cur_proc = tokens[0]
            else:
                results = instructions[tokens[0].upper()](addr, tokens[1:], variables, procs)
                addr = results[0]
                for j in results[1]:
                    final.append(j)



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
        with open(argv.i, 'r') as f:
            code = f.read()
            code = code.split('\n')

    except:
        error("No such file %s" % argv.i)

    binary = assemble(code)
    outfile = "a.o"

    try:
        outfile = argv.o

    except:
        pass

    with open(outfile, "wb") as f:
        f.write(binary)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('i', help="Input file to assemble into an object file.")
    # parser.add_argument('-o', help="Output file to store the object file. Default is a.o")
    # args = parser.parse_args()
    class Args:
        i = 'platform.asm'
        o = 'plt.bin'

    main(Args)
