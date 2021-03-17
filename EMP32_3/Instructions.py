INS_INT = 0x0
INS_CALL = 0x1
INS_RET = 0x2
INS_MOV = 0xC
INS_HLT = 0xF

decoder = {
    0: 'INT',
    1: 'CALL',
    2: 'RET',
    0xC: 'MOV',
    0xF: 'HLT'
}

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

def NOP(*args):
    return [INS_NOP, 0x0, 0x0, 0x0, 0x0]

def DEC(tokens, variables, *args):
    pass

def INC(tokens, variables, *args):
    pass

def JMP(tokens, variables, procs, labels, *args):
    pass

def JE(tokens, variables, procs, labels, *args):
    pass

def CMP(tokens, variables, *args):
    pass

def HLT(*args):
    return [INS_HLT, 0x0, 0x0, 0x0, 0x0]

def MOV(tokens, variables, *args):
    code = [INS_MOV]

    if (tokens[0] in registers) and (tokens[1] in registers):
        code.append(0)
        code.append(registers[tokens[0]])
        code.append(registers[tokens[1]])
        code.append(0)

    elif (tokens[0] in registers):
        try:
            tokens[1] = int(tokens[1])
            code.append(0b011)
            code.append(registers[tokens[0]])
            code.append((tokens[1] & 0xFF00) >> 8)
            code.append(tokens[1] & 0xFF)
        except:
            if tokens[1] in variables:
                code.append(0b001)
                code.append(registers[tokens[0]])
                code.append((variables[tokens[1]] & 0xFF00) >> 8)
                code.append(variables[tokens[1]] & 0xFF)

    return code

def CALL(tokens, variables, procs, *args):
    code = [INS_CALL]

    if tokens[0] in procs:
        addr = procs[tokens[0]]
        code.append(0b110)
        code.append((addr & 0xFF00) >> 8)
        code.append(addr & 0xFF)
        code.append(0x0)

    return code

def INT(tokens, *args):
    code = [INS_INT, int(tokens[0]), 0x0, 0x0, 0x0]

    return code

def RET(tokens, *args):
    if tokens != []:
        code = [INS_RET, int(tokens[0]), 0x0, 0x0, 0x0]
    else:
        code = [INS_RET, 0x0, 0x0, 0x0, 0x0]

    return code
