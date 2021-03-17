'''
Handles Everything
'''

import sys
import re

here = '\\'.join(__file__.split('\\')[:-3])
bins = here + '\\src\\bin\\'
scripts = here + '\\src\\scripts\\'

sys.path.append(scripts)

import ALU
import time

# Instruction Set

instructions = {
    '000000': 'ADD',
    '000001': 'SUB',
    '000010': 'MUL',
    '000011': 'DIV',
    '000100': 'AND',
    '000101': 'OR',
    '000110': 'XOR',
    '000111': 'NOT',
    '001000': 'JMP',
    '001001': 'Jcc',
    '001010': 'CMP',
    '001011': 'LOAD',
    '001100': 'MOV',
    '001101': 'NOP',
    '001110': 'OUT',
    '001111': 'IN',
    '010000': 'SIGN',
    '010001': 'HLT',
    '010010': 'POP',
    '010011': 'POPF',
    '010100': 'PUSH',
    '010101': 'PUSHF',
    '010110': 'WAIT',
    '010111': 'NLFY',
    '011000': 'SET',
    '011001': 'STORE',
    '011010': 'EXIT',
    '011011': 'GET',
    '011100': 'FETCH',
    '011101': 'START',
    '011110': 'COPY',
    '011111': 'INMT',
    '100000': 'DCMT',
    '100001': 'LOOP',
    '100010': 'NAME'
}

def get_reg(index):
    with open(bins + 'Registers.bin', 'r') as f:
        data = f.readlines()
    return data[int(index, 2)].replace('\n', '').replace(' ', '')

def write_reg(index, data):
    with open(bins + 'Registers.bin', 'r') as f:
        copy = f.readlines()
    
    copy[int(index, 2)] = data
    with open(bins + 'Registers.bin', 'w') as f:
        f.write(''.join(copy))

def reg_format(data, newline=True):
    data = data.replace(' ', '').replace('\n', '')
    if len(data) == 19:
        data = data[:3] + ' ' + data[3:]
    if newline:
        data += '\n'
    return data

def get_flags():
    with open(bins + 'Registers.bin', 'r') as f:
        data = f.readline()
    data = data.replace(' ', '')
    return [i for i in data]

def hlt():
    while True:
        if get_flags()[1] == '1':
            copy = [i for i in get_reg('0')]
            copy[1] = '0'
            copy = ' '.join(copy) + '\n'
            write_reg('0', copy)
            return
        time.sleep(1/5)

def wait(start):
    while True:
        time.sleep(1/2)
        with open(bins + 'Registers.bin', 'r') as f:
            if start == f.readlines():
                break
            else:
                start = f.readlines()

def onExit():
    clear()

def clear():
    with open(bins + 'RAM.bin', 'w') as f:
        f.write('000000 00000000000000000000000000\n'*16)
    flags_settings = '00000000'
    with open(here + '\\settings\\config.conf', 'r') as f:
        for i in f.readlines():
            if i.startswith('FLAGS-settings'):
                flags_settings = i.strip('FLAGS-settings').replace('\n', '').replace(' ', '')
                flags_settings = ' '.join([i for i in flags_settings])
    with open(bins + 'Registers.bin', 'w') as f:
        f.write(flags_settings + '\n' + ('000 0000000000000000\n'*12) + '0000000000000000\n')

def CPU(boot_operation, boot_bin, eprom_bin, isTest=False):
    bootop = True
    curr_addr = None
    while True:
        if bootop:
            section = boot_operation.replace(' ', '')
        else:
            addr = '{0:b}'.format(curr_addr)
            while len(addr) < 16:
                addr = '0' + addr
            write_reg('1101', addr)

            with open(bins + 'RAM.bin', 'r') as f:
                ram = ''.join(f.readlines()).replace('\n', '').replace(' ', '')
                ram = re.findall('................................', ram)
            try:
                section = ram[curr_addr].replace(' ', '').replace('\n', '')
            except KeyError:
                print('System crashed.')
                return onExit()
        instruction = instructions[section[:6]]
        section = section[6:]

        if instruction == 'ADD':
            num1 = get_reg(section[:5])
            num2 = get_reg(section[5:10])
            result = ALU.add(num1, num2)
            result = reg_format(result)
            write_reg(section[10:15], result)

        elif instruction == 'SUB':
            num1 = get_reg(section[:5])
            num2 = get_reg(section[5:10])
            result = ALU.sub(num1, num2)
            result = reg_format(result)
            write_reg(section[10:15], result)

        elif instruction == 'MUL':
            num1 = get_reg(section[:5])
            num2 = get_reg(section[5:10])
            result = ALU.mul(num1, num2)
            result = reg_format(result)
            write_reg(section[10:15], result)

        elif instruction == 'DIV':
            num1 = get_reg(section[:5])
            num2 = get_reg(section[5:10])
            result = ALU.div(num1, num2)
            result = reg_format(result)
            write_reg(section[10:15], result)

        elif instruction == 'AND':
            num1 = get_reg(section[:5])
            num2 = get_reg(section[5:10])
            result = ALU.bitwise.AND(num1, num2)
            result = reg_format(result)
            write_reg(section[10:15], result)

        elif instruction == 'OR':
            num1 = get_reg(section[:5])
            num2 = get_reg(section[5:10])
            result = ALU.bitwise.OR(num1, num2)
            result = reg_format(result)
            write_reg(section[10:15], result)

        elif instruction == 'XOR':
            num1 = get_reg(section[:5])
            num2 = get_reg(section[5:10])
            result = ALU.bitwise.XOR(num1, num2)
            result = reg_format(result)
            write_reg(section[10:15], result)

        elif instruction == 'NOT':
            num1 = get_reg(section[:5])
            result = ALU.bitwise.NOT(num1)
            result = reg_format(result)
            write_reg(section[10:15], result)

        elif instruction == 'NOP':
            pass

        elif instruction == 'SIGN':
            num1 = get_reg(section[:5])
            result = ALU.sign(num1)
            result = reg_format(result)
            write_reg(section[10:15], result)

        elif instruction == 'CMP':
            pass

        elif instruction == 'HLT':
            hlt()

        elif instruction == 'WAIT':
            with open(bins + 'Registers.bin', 'r') as f:
                init = f.readlines()
            wait(init)

        elif instruction == 'NLFY':
            num = get_reg(section[:5])
            num = '111' + num[3:]
            write_reg(section[:5], num)

        elif instruction == 'GET':
            if section[:16] not in [boot_bin, eprom_bin]:
                with open(bins + 'DISK\\' + section[:16] + '.bin', 'r') as f:
                    data = f.readlines()
                for i in range(len(data)):
                    if not data[i].endswith('\n'):
                        data[i] += '\n'
                with open(bins + 'RAM.bin', 'r') as f:
                    copy = f.readlines()
                start = int(section[16:], 2)
                copy[start:start+len(data)] = data
                with open(bins + 'RAM.bin', 'w') as f:
                    f.write(''.join(copy))
            else:
                print('Access Denied. Cant access address %s' % hex(int(section[:16], 2)))

        elif instruction == 'SET':
            write_reg(section[:5], reg_format(section[5:-2]))

        elif instruction == 'LOAD':
            line = section[:16]
            pos = section[16:21]
            with open(bins + 'RAM.bin', 'r') as f:
                copy = f.readlines()
            line = copy[int(line, 2)]
            write_reg(pos, line)

        elif instruction == 'MOV':
            pos1 = section[:5]
            pos2 = section[5:10]
            line = get_reg(pos1)
            if len(line) == 19:
                line = reg_format(line)
            write_reg(pos2, line)

        elif instruction == 'FETCH':
            with open(bins + 'RAM.bin', 'r') as f:
                copy = f.readlines()
            
            data = get_reg(section[:5])
            data = reg_format(data)
            copy[int(section[5:21], 2)] = data
            with open(bins + 'RAM.bin', 'w') as f:
                f.write(''.join(copy))

        elif instruction == 'STORE':
            if section[:16] not in [boot_bin, eprom_bin]:
                type_ = section[16:17]
                if type_ == '0':
                    type_ = 'w'
                else:
                    type_ = 'a'

                with open(bins + 'RAM.bin', 'r') as f:
                    copy = f.readlines()

                line = copy[int(section[17:], 2)]
                if len(line.replace('\n', '').replace(' ', '')) == 19:
                    line = reg_format(line, newline=False)

                with open(bins + 'DISK\\' + section[:16] + '.bin', type_) as f:
                    f.write(line + '\n')
            else:
                print('Access Denied. Cant access address %s' % hex(int(section[:16], 2)))

        elif instruction == 'EXIT':
            with open(bins + 'RAM.bin', 'r') as f:
                ram = ''.join(f.readlines()).replace('\n', '').replace(' ', '')
                ram = re.split('................................', ram)
            try:
                section2 = ram[curr_addr+1]
                instruction2 = instructions[section2[:6]]
                section2 = section2[6:]
            except KeyError:
                instruction2 = None
            if instruction2 == 'START':
                onExit()
            else:
                return onExit()

        elif instruction == 'JMP':
            curr_addr = int(section[:16], 2)
            bootop = False
            continue

        elif instruction in ['Jcc', 'JCC', 'JMPIF']:
            cond = section[:10]
            jmp = section[10:]
            with open(bins + 'RAM.bin', 'r') as f:
                copy = f.readlines()
            cond = copy[int(cond, 2)].replace(' ', '').replace('\n', '')
            success = False
            if cond.startswith('001010'):
                num1 = get_reg(cond[6:11]).replace(' ', '').replace('\n', '')
                num2 = get_reg(cond[11:16]).replace(' ', '').replace('\n', '')
                if ALU.convert(num1)[0] == ALU.convert(num2)[0]:
                    success = True
            else:
                success = True

            if success == True:
                curr_addr = int(section[10:], 2)
                bootop = False
                continue

        elif instruction == 'START':
            clear()
            with open(bins + 'DISK\\' + boot_bin + '.bin', 'r') as f:
                copy = f.readlines()
            with open(bins + 'RAM.bin', 'r') as f:
                ram = f.readlines()
            
            try:
                ram[:len(copy)] = copy
            except KeyError:
                ram = copy
            
            with open(bins + 'RAM.bin', 'w') as f:
                f.write(''.join(ram))
            curr_addr = 0
            bootop = False
            continue

        elif instruction == 'COPY':
            if section[10:] not in [boot_bin, eprom_bin]:
                with open(bins + 'RAM.bin', 'r') as f:
                    ram = f.readlines()
                    ram = ram[int(section[:10], 2):]
                with open(bins + 'DISK\\' + section[10:] + '.bin', 'w') as f:
                    f.write(''.join(ram))
            else:
                print('Access Denied. Cant access address %s' % hex(int(section[:16], 2)))

        elif instruction == 'INMT':
            line = get_reg(section[:5])
            line = ALU.add(line, '0000000000000000001')
            line = reg_format(line)
            write_reg(section[:5], line)

        elif instruction == 'DCMT':
            line = get_reg(section[:5])
            line = ALU.sub(line, '0000000000000000001')
            line = reg_format(line)
            write_reg(section[:5], line)

        elif instruction == 'IN':
            # 000000 0000000000000000 00000 00000
            port = section[:16]
            with open(bins + 'DISK\\' + port + '.bin', 'r') as f:
                value = f.readlines()[0]
            value = reg_format(value)
            with open(bins + 'DISK\\' + port + '.bin', 'w') as f:
                f.write('')
            write_reg(section[16:21], value)

        elif instruction == 'OUT':
            # 000000 0000000000000000 00000 0 0000
            port = section[:16]
            value = get_reg(section[16:21])
            type_ = section[21:22]
            if type_ == '0':
                type_ = 'a'
            else:
                type_ = 'w'
            while len(port) < 16:
                port = '0' + port
            with open(bins + 'DISK\\' + port + '.bin', type_) as f:
                f.write(value+'\n'*int(section[22:], 2))

        elif instruction == 'LOOP':
            # 000000 00000 000000000000 00000
            copy = get_reg(section[:5]).strip('\n')
            jmp = section[5:21]
            copy = ALU.sub(copy, '000 0000000000000001')
            copy = reg_format(copy)
            write_reg(copy, section[:5])
            if copy.replace(' ', '').strip('\n')[3:] == '0000000000000000':
                curr_addr = int(jmp, 2)
                continue

        elif instruction == 'NAME':
            pass

        if isTest:
            break

        if get_flags()[6] == '1':
            q = input(f'Address: {curr_addr} > ')
            if q == 'q':
                break

        curr_addr += 1
