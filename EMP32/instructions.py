import sys

# Opcodes for CPU
INS_BRK = 0x00
INS_NOP = 0x01
INS_ADD = 0x02
INS_SUB = 0x03
INS_MUL = 0x04
INS_DIV = 0x05
INS_MOV = 0x06
INS_JMP = 0x07
INS_Jcc = 0x08
INS_CMP = 0x09
INS_HLT = 0x0A
INS_CALL = 0x0B
INS_INT = 0x0C

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

# Encoders for Assembler
def BRK(addr, tokens, variables, *args) -> list:
    pass


def CALL(addr, tokens, variables, procs) -> list:
    code = [INS_CALL]
    addr += 1

    if tokens[0] in procs:
        code.append(procs[tokens[0]][0])
        code.append(procs[tokens[0]][1] - procs[tokens[0]][0])
        addr += 2

    else:
        try:
            tokens[0] = int(tokens[0])
            code.append(tokens[0])
            addr += 1
        except:
            print("assembler: error: Unknown procedure '%s'" % tokens[0])
            sys.exit()

    return [addr, code]


def NOP(addr, tokens, variables, *args) -> list:
    pass


def ADD(addr, tokens, variables, *args) -> list:
    pass


def SUB(addr, tokens, variables, *args) -> list:
    pass


def MUL(addr, tokens, variables, *args) -> list:
    pass


def DIV(addr, tokens, variables, *args) -> list:
    pass


def MOV(addr, tokens, variables, *args) -> list:
    global registers

    code = [INS_MOV]
    addr += 1

    if (tokens[0].upper() in registers) and (tokens[1].upper() in registers) and (len(tokens) == 2):
        value = registers[tokens[0].lower()] << 3 | registers[tokens[1].lower()]
        code.append(value)
        addr += 1

    elif (tokens[0].upper() in registers):
        value = 0b01 << 6 | registers[tokens[0].upper()] << 3
        code.append(value)
        code.append((addr & 0xFF000000) >> 24)
        code.append((addr & 0xFF0000) >> 16)
        code.append((addr & 0xFF00) >> 8)
        code.append(addr & 0xFF)
        addr += 5

        if tokens[1] == 'OFFSET':
            if tokens[2] in variables:
                for i in variables[tokens[2]]:
                    code.append(ord(i))
                    addr += 1

                return [addr, code]

        global res

        line = "global res; res = " + ' '.join(tokens[1:])
        splitline = line.split(' ')
    
        for j in range(len(splitline)):
            if splitline[j] in variables:
                splitline[j] = str(variables[splitline[j]])
        
        line = ' '.join(splitline)
        exec(line, globals(), locals())
        resHih = (res & 0xFF000000) >> 24
        resHio = (res & 0xFF0000) >> 16
        resLoh = (res & 0xFF00) >> 8
        resLoo = res & 0xFF
        code.append(resHih)
        code.append(resHio)
        code.append(resLoh)
        code.append(resLoo)
        addr += 4

    return [addr, code]


def JMP(addr, tokens, variables, *args) -> list:
    pass


def Jcc(addr, tokens, variables, *args) -> list:
    pass


def CMP(addr, tokens, variables, *args) -> list:
    pass


def HLT(addr, tokens, variables, *args) -> list:
    return [addr+1, [0xA]]
