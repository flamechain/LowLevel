
def main(outfile, infile):
    with open(infile, 'r') as f:
        contents = f.read()

    lines = []

    for i in contents.split('\n'):
        toks = i.split(' ')
        tokens = []

        for i in toks:
            if i != '':
                tokens.append(i)

        if tokens == []:
            continue

        if tokens[0] == '#include':
            lines.append('include %s' % tokens[1][1:-3])

        elif tokens[0].startswith('printf'):
            string = ' '.join(tokens)
            string = string.replace('printf("', '')
            string = string[:-3]

            if 'section .data' not in lines:
                lines.append('section .data')

            lines.append('    msg: ascii "%s"' % string)
            lines.append('    msg_len: len msg')

    for i in contents.split('\n'):
        toks = i.split(' ')
        tokens = []

        for i in toks:
            if i != '':
                tokens.append(i)

        if tokens == []:
            continue

        if len(tokens) > 1:
            if tokens[1] == 'main()':
                if 'section .text' not in lines:
                    lines.append('section .text')

                lines.append('main proc')
                continue

        if tokens[0] == '}':
            lines.append('main endp')
            lines.append('_start:')
            lines.append('    call main')
            lines.append('    ret')

        elif tokens[0].startswith('printf'):
            lines.append('    mov eax, msg')
            lines.append('    mov ebx, msg_len')
            lines.append('    call printf')

        elif tokens[0] == 'return':
            lines.append('    ret %s' % tokens[1][:-1])

    with open('build\\' + outfile + '.asm', 'w') as f:
        f.write('\n'.join(lines))

if __name__ == "__main__":
    import sys
    infile = sys.argv[1]
    outfile = sys.argv[3]
    main(outfile, infile)
