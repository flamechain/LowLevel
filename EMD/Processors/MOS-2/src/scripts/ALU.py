conversions = {
    '000': 'int',
    '001': 'float',
    '010': 'uint',
    '011': 'ufloat'
}

def convert(node):
    datatype = node[0:3]
    value = node[3:]
    pos = None
    if datatype == '000':
        return [int(value, 2), datatype, None]
    elif datatype == '010':
        if value[0] == '1':
            return [-int(value[1:], 2), datatype, None]
        else:
            return [int(value[1:], 2), datatype, None]
    elif datatype == '001':
        pos = int(value[:4], 2)
        value = str(int(value[4:], 2))
        result = value[:pos] + '.' + value[pos:]
        return [result, datatype, None]
    elif datatype == '011':
        if value[0] == '1':
            var = -1
        else:
            var = 1
        pos = int(value[1:5], 2)
        value = str(int(value[5:], 2))
        result = value[:pos] + '.' + value[pos:]
        return [result * var, datatype, pos]

def floatify(node, u, pos, neg=False):
    node = '{0:b}'.format(int(str(node)[7:]))
    type = '001' if u else '011'
    if not u:
        while len(node) < 12:
            node = '0' + node
        if neg:
            node = '1' + node
        else:
            node = '0' + node
    else:
        while len(node) < 13:
            node = '0' + node
    if pos is None:
        pos = '000'
    else:
        pos = '{0:b}'.format(pos)
    while len(pos) < 3:
        pos = '0' + pos
    return type + pos + node

def finish(node, type, pos=None):
    if node < 0:
        pre = '1'
    else:
        pre = '0'
    if type in ['float', 'ufloat']:
        if type == 'float':
            result = floatify(node, True, pos, bool(int(pre)))
        else:
            result = floatify(node, False, pos, bool(int(pre)))
    else:
        node = int(node)
        try:
            result = '{0:b}'.format(abs(node))
        except:
            if type == '010':
                return finish(node, '011', pos)
            else:
                return finish(node, '001', pos)
    while len(result) < 16:
        result = '0' + result
    if type in ['int', 'float']:
        result = pre + result[1:]
    types = {'int': '010', 'float': '011', 'uint': '000', 'ufloat': '001'}
    try:
        result = types[type] + result
    except:
        result = type + result
    return result

class bitwise:
    @staticmethod
    def OR(node1, node2):
        node1 = convert(node1)
        node2 = convert(node2)
        type1 = None
        type2 = None
        pos = None
        if isinstance(node1[0] | node2[0], float):
            type1 = 'float'
        else:
            type1 = 'int'
        if (node1[1] in ['010', '011']) or (node2[1] in ['010', '011']):
            type2 = ''
        else:
            type2 = 'u'
        if type1 == 'float':
            pos = max([node1[2], node2[2]])
        type = type2 + type1
        result = finish(node1[0] | node2[0], type, pos)
        return result

    @staticmethod
    def AND(node1, node2):
        node1 = convert(node1)
        node2 = convert(node2)
        type1 = None
        type2 = None
        pos = None
        if isinstance(node1[0] & node2[0], float):
            type1 = 'float'
        else:
            type1 = 'int'
        if (node1[1] in ['010', '011']) or (node2[1] in ['010', '011']):
            type2 = ''
        else:
            type2 = 'u'
        if type1 == 'float':
            pos = max([node1[2], node2[2]])
        type = type2 + type1
        result = finish(node1[0] & node2[0], type, pos)
        return result

    @staticmethod
    def NOT(node1):
        node1 = convert(node1)
        type1 = None
        type2 = None
        pos = None
        if isinstance(~node1[0], float):
            type1 = 'float'
        else:
            type1 = 'int'
        if (node1[1] in ['010', '011']):
            type2 = ''
        else:
            type2 = 'u'
        if type1 == 'float':
            pos = node1[2]
        type = type2 + type1
        result = finish(~node1[0], type, pos)
        return result

    @staticmethod
    def XOR(node1, node2):
        node1 = convert(node1)
        node2 = convert(node2)
        type1 = None
        type2 = None
        pos = None
        if isinstance(node1[0] ^ node2[0], float):
            type1 = 'float'
        else:
            type1 = 'int'
        if (node1[1] in ['010', '011']) or (node2[1] in ['010', '011']):
            type2 = ''
        else:
            type2 = 'u'
        if type1 == 'float':
            pos = max([node1[2], node2[2]])
        type = type2 + type1
        result = finish(node1[0] ^ node2[0], type, pos)
        return result

def add(node1, node2):
    node1 = convert(node1)
    node2 = convert(node2)
    type1 = None
    type2 = None
    pos = None
    if isinstance(node1[0] + node2[0], float):
        type1 = 'float'
    else:
        type1 = 'int'
    if (node1[1] in ['010', '011']) or (node2[1] in ['010', '011']):
        type2 = ''
    else:
        type2 = 'u'
    if type1 == 'float':
        pos = max([node1[2], node2[2]])
    type = type2 + type1
    result = finish(node1[0] + node2[0], type, pos)
    return result

def sub(node1, node2):
    node1 = convert(node1)
    node2 = convert(node2)
    type1 = None
    type2 = None
    pos = None
    if isinstance(node1[0] - node2[0], float):
        type1 = 'float'
    else:
        type1 = 'int'
    if (node1[1] in ['010', '011']) or (node2[1] in ['010', '011']):
        type2 = ''
    else:
        type2 = 'u'
    if type1 == 'float':
        pos = max([node1[2], node2[2]])
    type = type2 + type1
    result = finish(node1[0] - node2[0], type, pos)
    return result

def div(node1, node2):
    node1 = convert(node1)
    node2 = convert(node2)
    type1 = None
    type2 = None
    pos = None
    if isinstance(node1[0] / node2[0], float):
        if (node1[0] // node2[0]) != (node1[0] / node2[0]):
            type1 = 'float'
        else:
            type1 = 'int'
    else:
        type1 = 'int'
    if (node1[1] in ['010', '011']) or (node2[1] in ['010', '011']):
        type2 = ''
    else:
        type2 = 'u'
    if type1 == 'float':
        try:
            pos = node1[2] + node2[2]
        except:
            pass
    type = type2 + type1
    result = finish(node1[0] / node2[0], type, pos)
    while len(result) > 19:
        result = result[:-1]
    return result

def mul(node1, node2):
    node1 = convert(node1)
    node2 = convert(node2)
    type1 = None
    type2 = None
    pos = None
    if isinstance(node1[0] * node2[0], float):
        type1 = 'float'
    else:
        type1 = 'int'
    if (node1[1] in ['010', '011']) or (node2[1] in ['010', '011']):
        type2 = ''
    else:
        type2 = 'u'
    if type1 == 'float':
        try:
            pos = node1[2] + node2[2]
        except:
            pass
    type = type2 + type1
    result = finish(node1[0] * node2[0], type, pos)
    return result

def sign(node1):
    if convert(node1)[0] < 0:
        return '01010000000000000000000000000001'
    else:
        return '01000000000000000000000000000001'
