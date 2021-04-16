class Memory:
    def __init__(self, size=2**16):
        '''#### Supplied Memory object for EMP64 that creates a virtual RAM of n size.

        Defaults to 16-bit limit of 2^16.

        ## Example

        ```
        from Source import Memory

        memory = Memory(100)
        memory.Data[0x0] = 4
        ```

        Now memory address 0x0 contains 4.'''

        self.Data = []

        for i in range(size):
            self.Data.append(0x0)

class EFLAGS:
    def __init__(self):
        self.CF = 0
        self.PF = 0
        self.AF = 0
        self.ZF = 0
        self.SF = 0
        self.TF = 0
        self.IF = 1
        self.DF = 1
        # 0
        self.OF = 0
        self.DE = 0
        self.IO = 1
        self.PL = 1
        self.NT = 0
        self.ID = 1
        self.RF = 0

    def full(self):
        return self.CF << 15 | self.PF << 14 | self.AF << 13 | self.ZF << 12 | self.SF << 11 | self.TF << 10 | self.IF << 9 | self.DF << 8 | self.OF << 6 | self.DE << 5 | self.IO << 4 | self.PL << 3 | self.NT << 2 | self.ID << 1 | self.RF

    def load(self, value: int):
        self.CF = value & 0b1000000000000000
        self.PF = value & 0b0100000000000000
        self.AF = value & 0b0010000000000000
        self.ZF = value & 0b0001000000000000
        self.SF = value & 0b0000100000000000
        self.TF = value & 0b0000010000000000
        self.IF = value & 0b0000001000000000
        self.DF = value & 0b0000000100000000
        self.OF = value & 0b0000000001000000
        self.DE = value & 0b0000000000100000
        self.IO = value & 0b0000000000010000
        self.PL = value & 0b0000000000001000
        self.NT = value & 0b0000000000000100
        self.ID = value & 0b0000000000000010
        self.RF = value & 0b0000000000000001

class IA32_EFER:
    def __init__(self):
        self.PE = 0
        self.TE = 1
        self.NE = 1
        self.LME = 1
        self.LMA = 0
        self.WP = 1

    def full(self):
        return self.PE << 7 | self.TE << 4 | self.NE << 3 | self.LME << 2 | self.LMA << 1 | self.WP

class DR6:
    def __init__(self):
        pass

    def full(self):
        return

class DR7:
    def __init__(self):
        self.LDR0 = 0
        self.GDR0 = 0
        self.LDR1 = 0
        self.GDR1 = 0
        self.LDR2 = 0
        self.GDR2 = 0
        self.LDR3 = 0
        self.GDR3 = 0
        self.CDR0 = 0
        self.SDR0 = 3
        self.CDR1 = 0
        self.SDR1 = 3
        self.CDR2 = 0
        self.SDR2 = 3
        self.CDR3 = 0
        self.SDR3 = 3

    def full(self):
        return self.LDR0 << 31 | self.GDR0 << 30 | self.LDR1 << 29 | self.GDR1 << 28 | self.LDR2 << 27 | self.GDR2 << 26 | self.LDR3 << 25 | self.GDR3 << 24 | self.CDR0 << 14 | self.SDR0 << 12 | self.CDR1 << 10 | self.SDR1 << 8 | self.CDR2 << 6 | self.SDR2 << 4 | self.CDR3 << 2 | self.SDR3

class TR:
    def __init__(self):
        self.SZ = 0
        self.SA = 0

    def full(self):
        return self.SZ << 63 | self.SA

class TSS:
    def __init__(self):
        self.IOPL = 3
        self.PR = 0
        self.IOPB = 0

    def full(self):
        return self.IOPL << 29 | self.PR << 25 | self.IOPB

class IDTE:
    def __init__(self):
        self.TP = 0
        self.LC = 0

    def full(self):
        return self.TP << 16 | self.LC
