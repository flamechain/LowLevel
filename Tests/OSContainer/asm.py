import re

def create_bin(value, size):
    value = '{0:b}'.format(value)
    value = '0'* (size - len(value)) + value
    return value

def link(code):
    code = code.split('\n')
    start = 0
    cur_sect = ''
    final = []
    for i in code:
        if i.startswith('ENTRY(_start)'):
            pass
        elif i.startswith('SECTIONS'):
            cur_sect = 'SECTIONS'
        elif i.startswith('    ') and (cur_sect == 'SECTIONS'):
            i = i.replace('    ', '')
            if i.startswith('. '):
                start = i.strip('. = ')
                if 'M' in start:
                    start = int(start.strip('M')) * 1000000 # 0x000F4240
            elif i.startswith('.header:'):
                line = i.split(': *')[1]
                with open(line, 'rb') as f:
                    contents = f.read().hex()
                    contents = re.findall('..', contents)
                    multiboot = 0
                    mode = 0
                    length = 0
                    if ''.join(contents[:4]) == 'e85250d6':
                        multiboot = int(''.join(contents[:4]), 16)
                    else:
                        print('Unsuported Multiboot Mode')
                    if ''.join(contents[4:8]) == '00000000':
                        mode = int(''.join(contents[4:8]), 16)
                    else:
                        print('Unsupported OS Mode')
                    if ''.join(contents[8:12]) == '00000008':
                        length = int(''.join(contents[8:12]), 16)
                    else:
                        print('Header checks failed')
                    if int(''.join(contents[12:16]), 16) == (0x100000000 - (multiboot + mode + length)):
                        pass
                    else:
                        print('Checksum failed')
                    if ''.join(contents[16:24]) == '0000000000000008':
                        continue
                    else:
                        print('Invalid End Tag')

            elif i.startswith('.text:'):
                line = i.split(': *')[1]
                with open(line, 'rb') as f:
                    contents = f.read().hex()
                    contents = re.findall('..', contents)
                ret = bytearray()
                for i in contents:
                    ret.extend(bytes([int(i, 16)]))
    sHih = (start & 0xFF000000) >> 24
    sHio = (start & 0xFF0000) >> 16
    sLoh = (start & 0xFF00) >> 8
    sLoo = start & 0xFF


    return ret, (bytes([sHih]), bytes([sHio]), bytes([sLoh]), bytes([sLoo]))

res = 0

def get_val(line, variables, truevars):
    try:
        if line.startswith('0x'):
            return int(line, 16)
        else:
            return int(line)
    except: pass
    global res
    res = 0
    for i in variables:
        if i in line:
            line = line.replace(i, str(variables[i]))
    if ';' in line:
        line = line.split(';')[0].replace(' ', '')
    line = 'global res; res = ' + line
    exec(line, globals(), locals())
    return res

def assemble(code):
    code = code.split('\n')

    variables = {}
    truevars = {}
    labels = {}
    final = []

    cur_sect = None
    cur_lbl = None
    addr_ofst = 0x0
    start = None

    for i in code:
        if i.startswith('section'):
            cur_sect = i.replace('section ', '')
        elif i.endswith(':'):
            cur_lbl = i.strip(':')
            variables[cur_lbl] = addr_ofst
            addr_ofst += 1
        else:
            if i.split(';')[0].replace(' ', '') == '':
                pass
            else:
                addr_ofst += 1

    addr_ofst = 0x0

    for i in code:
        if i.startswith('    '):
            if cur_sect == '.text':
                line = i.replace('    ', '')
                if line.startswith('bits'):
                    if line.split(' ')[1] == '32':
                        pass
                    else:
                        return print("%s bit mode is not available" % line[1])
                elif cur_lbl.startswith('_start'):
                    if line.startswith('hlt'):
                        final.append('00000001')
                        addr_ofst += 1
                    elif line.startswith('mov'):
                        line = line.split(' ')
                        final.append('00000010')
                        addr_ofst += 1
                        if line[1] == 'dword':
                            final.append('11010010')
                            addr_ofst += 1
                            value = create_bin(int(line[2].strip('[],'), 16), 32)
                            final.append(value[:8])
                            final.append(value[8:16])
                            final.append(value[16:24])
                            final.append(value[24:32])
                            addr_ofst += 4
                            value = create_bin(int(line[3], 16), 32)
                            final.append(value[:8])
                            final.append(value[8:16])
                            final.append(value[16:24])
                            final.append(value[24:32])
                            addr_ofst += 4

            elif cur_sect == '.data':
                pass
            else:
                line = i.replace('    ', '')
                if line.startswith('dd '):
                    value = line.replace('dd ', '')
                    value = get_val(value, variables, truevars)
                    value = create_bin(value, 32)
                    final.append(value[:8])
                    final.append(value[8:16])
                    final.append(value[16:24])
                    final.append(value[24:32])
                    addr_ofst += 4
                elif line.startswith('dw '):
                    value = line.replace('dw ', '')
                    value = get_val(value, variables, truevars)
                    value = create_bin(value, 16)
                    final.append(value[:8])
                    final.append(value[8:16])
                    addr_ofst += 2
                elif line.startswith('db '):
                    value = line.replace('db ', '')
                    value = get_val(value, variables, truevars)
                    final.append(create_bin(value, 8))
                elif line.startswith('dq '):
                    value = line.replace('dq ', '')
                    value = get_val(value, variables, truevars)
                    value = create_bin(value, 64)
                    final.append(value[:8])
                    final.append(value[8:16])
                    final.append(value[16:24])
                    final.append(value[24:32])
                    final.append(value[32:40])
                    final.append(value[40:48])
                    final.append(value[48:56])
                    final.append(value[56:64])
                    addr_ofst += 8
                elif line.startswith('dt '):
                    value = line.replace('dt ', '')
                    value = get_val(value, variables, truevars)
                    value = create_bin(value, 48)
                    final.append(value[:8])
                    final.append(value[8:16])
                    final.append(value[16:24])
                    final.append(value[24:32])
                    final.append(value[32:40])
                    final.append(value[40:48])
                    addr_ofst += 6

    ret = bytearray()

    for i in final:
        ret.extend(bytes([int(i, 2)]))

    return ret
