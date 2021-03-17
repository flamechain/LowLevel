import re
import argparse
import sys
import Instructions as Ins

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
    'EAX': 0b000, # General
    'EBX': 0b001, # General
    'ECX': 0b010, # General
    'EDX': 0b011, # General
    'ESI': 0b100, # General
    'ESP': 0b101, # General
    'EDI': 0b110, # Return
    'EBP': 0b111, # Offset
    'AX': 0b1000, # 8-bit
    'BX': 0b1001, # 8-bit
    'CX': 0b1010, # 8-bit
    'DX': 0b1011  # 8-bit
}

def pass_one(code):
    variables = {}
    strings = {}
    procs = {}
    final = []
    labels = {}
    entry = 0
    addr = 0

    for i in code:
        tokens = re.split(',| ', i)
        oldtokens = tokens
        tokens = []

        for j in oldtokens:
            if j != '':
                tokens.append(j)

        if not i.startswith('    '):
            if tokens[0] == '_start:':
                entry += addr
                check_len(tokens, 1, "Invalid syntax: %s" % i)

            elif tokens[0].endswith(':'):
                labels[tokens[0][:-1]] = addr
                check_len(tokens, 1, "Invalid syntax: %s" % i)

            elif tokens[0] == 'section':
                cur_sect = tokens[1][1:]
                check_len(tokens, 2, "Sections only take 1 argument, name\n%s" % i)

            elif tokens[1] == 'PROC':
                procs[tokens[0]] = addr
                check_len(tokens, 2, "Procedure tags take 1 argument, procedure name\n%s" % i)

            elif tokens[1] == 'ENDP':
                check_len(tokens, 2, "Procedure tags take 1 argument, procedure name\n%s" % i)

            elif tokens[0] == 'INCLUDE':
                check_len(tokens, 2, "Include have 1 argument, package name\n%s" % i)

                if True:
                    error("Unsupported feature: Include")

                else:
                    error("Unknown package: %s" % tokens[1])

        else:
            if cur_sect == 'data':
                if not tokens[0].endswith(':'):
                    error("Variables must be declared with ':'\n %s" % i)

                if tokens[1] == '.ascii':

                    string = ' '.join(tokens[2:]).split('"')

                    if string[0] != '':
                        error("Ascii strings must be enclosed in double-quotes\n%s" % i)

                    for i in string[2].split(','):
                        string[1] += chr(int(i.strip(' ')))

                    variables[tokens[0][:-1]] = addr
                    strings[tokens[0][:-1]] = string[1]

                    for i in string[1].replace('\\n', '\n'):
                        final.append(ord(i))
                        addr += 1
                
                elif tokens[1] == 'len':
                    check_len(tokens, 3, "Len takes 1 argument: string\n%s" % i)

                    if tokens[2] in strings:
                        variables[tokens[0][:-1]] = addr
                        final.append(len(strings[tokens[2]] & 0xFF))
                        addr += 1

                    else:
                        error("Can only take len of string\n%s" % i)

            else:
                addr += 5

    return variables, procs, final, labels, entry

def assemble(code):
    code = clean_file(code)
    cur_sect = None
    
    instructions = {
        'INT': Ins.INT,
        'CALL': Ins.CALL,
        'RET': Ins.RET,
        'JMP': Ins.JMP,
        'CMP': Ins.CMP,
        'JE': Ins.JE,
        'JGE': Ins.JGE,
        'JNE': Ins.JNE,
        'DEC': Ins.DEC,
        'INC': Ins.INC,
        'PUSH': Ins.PUSH,
        'POP': Ins.POP,
        'MOV': Ins.MOV,
        'ADD': Ins.ADD,
        'SUB': Ins.SUB
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

        elif (cur_sect in ['text', 'code']) and i.startswith('    '):
            results = instructions[tokens[0].upper()]( tokens[1:], variables, procs, labels)

            for j in results:
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

def main(argv):
    try:
        with open(argv.i, 'r') as f:
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

    with open(outfile + '.o', "wb") as f:
        f.write(binary)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('i', help="Input file to assemble into an object file.")
    parser.add_argument('-o', help="Output file to store the object file. Default is a.o")
    args = parser.parse_args()
    class Args:
        i = 'main.asm'
        o = 'main'

    main(args)

