here = '\\'.join(__file__.split('\\')[:-3])

def bios():
    boot_bin = None
    EPROM_bin = None
    with open(here + '\\settings\\config.conf', 'r') as f:
        settings = f.readlines()
    for i in settings:
        if i.startswith('boot'):
            boot_bin = i.strip('boot').replace(' ', '').replace('\n', '')
        elif i.startswith('EPROM'):
            EPROM_bin = i.strip('EPROM').replace(' ', '').replace('\n', '')
    if boot_bin == 'EPROM':
        boot_bin = EPROM_bin
    boot_bin = '{0:b}'.format(int(boot_bin, 16))
    EPROM_bin = '{0:b}'.format(int(EPROM_bin, 16))
    while len(boot_bin) < 16:
        boot_bin = '0' + boot_bin
    while len(EPROM_bin) < 16:
        EPROM_bin = '0' + EPROM_bin
    return [boot_bin, EPROM_bin]
