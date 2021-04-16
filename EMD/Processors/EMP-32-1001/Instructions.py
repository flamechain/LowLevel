INS_HLT = 0x01
INS_MOV = 0x02
INS_CALL = 0x03
INS_INT = 0x04
INS_RET = 0x05
INS_JMP = 0x06
INS_CMP = 0x07
INS_JE = 0x08
INS_DEC = 0x09
INS_INC = 0x0A


registers = {
    'eax': 0,
    'ebx': 1,
    'ecx': 2,
    'edx': 3,
    'dl': 3,
    'dh': 4,
    'esi': 4,
    'esp': 5,
    'edi': 6,
    'ebp': 7
}

res = 0

def DEC(tokens, variables, pointers, *args):
    code = [INS_DEC]

    if tokens[0] in pointers:
        addr = pointers[tokens[0]]
        code.append((addr & 0xFF000000) >> 24)
        code.append((addr & 0xFF0000) >> 16)
        code.append((addr & 0xFF00) >> 8)
        code.append(addr & 0xFF)

    return code

def INC(tokens, variables, pointers, *args):
    code = [INS_INC]

    if tokens[0] in pointers:
        addr = pointers[tokens[0]]
        code.append((addr & 0xFF000000) >> 24)
        code.append((addr & 0xFF0000) >> 16)
        code.append((addr & 0xFF00) >> 8)
        code.append(addr & 0xFF)

    return code

def JMP(tokens, variables, pointers, procs, labels, *args):
    code = [INS_JMP]

    if tokens[0] in labels:
        addr = labels[tokens[0]]
        code.append((addr & 0xFF000000) >> 24)
        code.append((addr & 0xFF0000) >> 16)
        code.append((addr & 0xFF00) >> 8)
        code.append(addr & 0xFF)

    return code

def JE(tokens, variables, pointers, procs, labels, *args):
    code = [INS_JE]

    if tokens[0] in labels:
        addr = labels[tokens[0]]
        code.append((addr & 0xFF000000) >> 24)
        code.append((addr & 0xFF0000) >> 16)
        code.append((addr & 0xFF00) >> 8)
        code.append(addr & 0xFF)

    return code

def CMP(tokens, variables, pointers, *args):
    code = [INS_CMP]
    mod = 0

    if tokens[0] in pointers:
        mod = mod | 0b10100000

    if tokens[1].startswith('"'):
        mod = mod | 0b01000000

    code.append(mod)

    if tokens[0] in pointers:
        addr = pointers[tokens[0]]
        code.append((addr & 0xFF000000) >> 24)
        code.append((addr & 0xFF0000) >> 16)
        code.append((addr & 0xFF00) >> 8)
        code.append(addr & 0xFF)

    if tokens[1].startswith('"'):
        value = ord(tokens[1].replace('"', ''))
        code.append((value & 0xFF000000) >> 24)
        code.append((value & 0xFF0000) >> 16)
        code.append((value & 0xFF00) >> 8)
        code.append(value & 0xFF)

    return code

def HLT(*args):
    return [INS_HLT]

def MOV(tokens, variables, pointers, *args):
    code = [INS_MOV]

    if tokens[0].lower() in registers:
        mod = 0b01000000
        mod = mod | registers[tokens[0].lower()] << 3

    elif tokens[0] in pointers:
        mod = 0b10011000

        if tokens[1] in registers:
            mod = mod | registers[tokens[1]]

        code.append(mod)
        addr = pointers[tokens[0]]
        code.append((addr & 0xFF000000) >> 24)
        code.append((addr & 0xFF0000) >> 16)
        code.append((addr & 0xFF00) >> 8)
        code.append(addr & 0xFF)

        return code

    if tokens[1].upper() == 'OFFSET':
        mod = mod | 0b001
        code.append(mod)
        if tokens[2] in pointers:
            addr = pointers[tokens[2]]
            code.append((addr & 0xFF000000) >> 24)
            code.append((addr & 0xFF0000) >> 16)
            code.append((addr & 0xFF00) >> 8)
            code.append(addr & 0xFF)

    elif tokens[1] in pointers:
        mod = mod | 0b111
        code.append(mod)
        addr = pointers[tokens[1]]
        code.append((addr & 0xFF000000) >> 24)
        code.append((addr & 0xFF0000) >> 16)
        code.append((addr & 0xFF00) >> 8)
        code.append(addr & 0xFF)


    else:
        mod = mod | 0b000

        if len(tokens) > 2:
            global res

            line = "global res; res = " + ' '.join(tokens[1:])
            splitline = line.split(' ')
        
            for j in range(len(splitline)):
                if splitline[j] in variables:
                    splitline[j] = str(variables[splitline[j]])
            
            line = ' '.join(splitline)
            exec(line, globals(), locals())
            value = int(res)

        elif tokens[1].startswith('0b'):
            value = int(tokens[1], 2)

        elif tokens[1].startswith('"'):
            try:
                value = ord(tokens[1].strip('"'))

            except:
                print("asm.py: error: Register assignment can only be 1 character long\n%s" % ' '.join(['    mov'] + tokens))

        else:
            value = int(tokens[1])

        code.append(mod)
        code.append((value & 0xFF000000) >> 24)
        code.append((value & 0xFF0000) >> 16)
        code.append((value & 0xFF00) >> 8)
        code.append(value & 0xFF)

    return code

def CALL(tokens, variables, pointers, procs, *args):
    code = [INS_CALL]

    if tokens[0] in procs:
        addr = procs[tokens[0]]
        code.append((addr & 0xFF000000) >> 24)
        code.append((addr & 0xFF0000) >> 16)
        code.append((addr & 0xFF00) >> 8)
        code.append(addr & 0xFF)

    return code

def INT(tokens, variables, *args):
    code = [INS_INT]

    if tokens[0] in variables:
        code.append(variables[tokens[0]])

    return code

def RET(tokens, variables, *args):
    code = [INS_RET]

    if tokens[0] in variables:
        code.append(variables[tokens[0]])

    else:
        if '0x' in tokens[0]:
            code.append(int(tokens[0], 16))

    return code
