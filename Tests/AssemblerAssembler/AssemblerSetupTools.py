def setup(**kwargs):
    '''Put all settings inside this function and they will be applied. Available settings are:

    | Name | Purpose | Type |
    |-|-|-|
    | name | Name of assembler, this is what will be used on the command line | str |
    | author | Optional, puts author in comments | str |
    | version | Give version, version 0.1 will be marked as unstable | float |
    '''
    # Parses Arguments
    filename = kwargs['name']
    author   = kwargs['author']
    version  = kwargs['version']
    date     = kwargs['date']

    # Creates File
    mode = 'x'
    try:
        with open(filename + '.py', 'x') as f:
            pass
    except:
        mode = 'w'

    with open(filename + '.py', mode) as f:
        header = "# %s %s\n#\n# %s\n# Created with AssemblerAssembler\n#\n# %s\n#\n" % (filename, version, author, date)

        if version == 0.1:
            header += '# > Note: Unstable Version\n#\n'
        elif version < 1:
            header += '# > Note: Version may be unstable\n#\n'

        f.write(header)
    
    
