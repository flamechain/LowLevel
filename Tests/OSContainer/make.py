import re
import os
import asm

def mx86_link(argv):
    with open(argv[0].replace('/', '\\'), 'r') as f:
        linker_ld = f.read()
    
    for i in range(len(argv)):
        if argv[i] == '-o':
            outfile = argv[i+1]

    binary, pc = asm.link(linker_ld)

    with open(outfile.replace('/', '\\'), 'wb') as f:
        f.write(pc[0] + pc[1] + pc[2] + pc[3] + binary)

def asm_assemble(argv):
    with open(argv[0].replace('/', '\\'), 'r') as f:
        code_asm = f.read()

    for i in range(len(argv)):
        if argv[i] == '-o':
            outfile = argv[i+1]

    obj = asm.assemble(code_asm)

    with open(outfile.replace('/', '\\'), 'wb') as f:
        f.write(obj)

def make_command(line, variables):
    line = line.replace(' $', '')
    line = re.split('\(|\)', line)
    newline = ''
    for i in line:
        if i != '':
            newline += i
    newline = newline.split(' ')
    mypath = os.path.split(__file__)[0]
    results = []
    if newline[0] == 'shell':
        if newline[1] == 'find':
            for i in os.walk(mypath):
                if i[0].endswith(newline[2].replace('/', '\\')):
                    files = i[2]
            if newline[3].startswith('*'):
                for i in files:
                    if i.endswith(newline[3].strip('*')):
                        results.append(newline[2] + '/' + i)
    elif newline[0] == 'patsubst':
        for i in variables[newline[2].split(',')[1]]:
            res = newline[2].split(',')[0]
            res = res.replace('%', i.split('/')[-1].split('.')[0])
            results.append(res)

    return results
                
def make_exec(source, command):
    mypath = os.path.split(__file__)[0]
    coms = command.strip('\t').split(' ')
    if coms[0] == 'mkdir':
        if coms[1].startswith('$('):
            if coms[1].strip('$(') == 'dir':
                if coms[2].strip(')') == '$@':
                    direct = source.split('/')[:-1]
                    path = mypath
                    try:
                        for i in direct:
                            path = os.path.join(path, i)
                            os.mkdir(path)
                    except:
                        pass
        else:
            direct = coms[1].split('/')
            path = mypath
            try:
                for i in direct:
                    path = os.path.join(path, i)
                    os.mkdir(path)
            except:
                pass
    elif coms[0] == 'asm':
        if coms[1].startswith('$('):
            if coms[1].strip('$(') == 'patsubst':
                if coms[4].strip(')') == '$@':
                    infile = coms[3].replace('%', source.split('/')[-1].split('.')[0])
        if coms[5] == '-o':
            if coms[6] == '$@':
                outfile = source
        asm_assemble([infile, '-o', outfile])
    elif coms[0] == 'Mx86':
        mx86_link(coms[1:])

def make(file):
    variables = {}
    i = 0
    lines = file.split('\n')
    while i < len(lines):
        ln = lines[i]
        if ':=' in ln:
            line = ln.split(':=')
            name = line[0].strip(' ')
            if line[1].startswith(' $'):
                value = make_command(line[1], variables)
            variables[name] = value
        elif ln.endswith(':'):
            if ln.strip('$():') in variables:
                commands = []
                for j in lines[i+1:]:
                    if j.startswith('\t'):
                        commands.append(j)
                    else:
                        break
                for j in variables[ln.strip('$():')]:
                    for k in commands:
                        make_exec(j, k)
        elif ln.split(' ')[0] in ['mkdir', 'Mx86']:
            make_exec(None, ln)

        i += 1

def main():
    with open('makefile', 'r') as f:
        makefile = f.read()

    make(makefile)


if __name__ == "__main__":
    main()
