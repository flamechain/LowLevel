import strutils, sequtils, tables, hashes
import ../../common/jmc, ../../common/util
import assemblerutil

type
    MC1 {.pure.} = enum
        r0_out = 0x0001,
        r1_out = 0x0002,
        reg_in = 0x0004,
        ir1_out = 0x0008,
        ir2_out = 0x0010,
        addr_imm = 0x0020,
        addr_ij = 0x0040,
        addr_sp = 0x0080,
        mem_in = 0x0100,
        mem_out = 0x0200,
        i_in = 0x0400,
        j_in = 0x0800,
        last = 0x4000

    MC0 {.pure.} = enum
        r0_out = 0x0001,
        r1_out = 0x0002,
        reg_in = 0x0004,
        ir1_out = 0x0008,
        ir2_out = 0x0010,
        load_f = 0x0020,
        alu_out = 0x0040,
        load_x = 0x0080,
        load_y = 0x0100,
        sp_inc = 0x0200,
        sp_dec = 0x0400,
        load_pc_ij = 0x0800,
        stop_if_zero = 0x1000,
        last = 0x4000

proc getMCWord(code: string, file: string, line: uint): uint16 =
    let tokens = code.assemblerTokenize()
    result = 0

    # Simoultaneously construct the microcode word and identify its type
    var isMC1 = false
    for mcb in tokens:
        try: discard parseEnum[MC0](mcb)
        except:
            isMC1 = true

        try: discard parseEnum[MC1](mcb)
        except:
            isMC1 = false

        try:
            result |= (if isMC1: parseEnum[MC1](mcb).uint16 else: parseEnum[MC0](mcb).uint16)
        except:
            assemblerAssert(false, "Unrecognized microcode bit " & mcb, file, line)

    # Set the MSB if this is MC1
    result |= uint16(if isMC1: 0x8000 else: 0x0000)            

# Needed for the 'sections' table
# @TODO: Pull request?
proc hash(x: uint): Hash = toU32(x.int64).Hash

proc microcodeAssemble*(codeLines: seq[CodeLine]): seq[uint8] =
    var
        # List of sections to be emitted into the final byte sequence
        # Indexed by their locations in ROM
        sections = newTable[uint, seq[uint16]]()

        # Current section. Contains:
        # List of instructions it applies to
        # Boolean, true if this is a const section
        # Sequence of actual microcode words
        section: (seq[Instruction], bool, seq[uint16])
        sectionValid = false

    # Called when done processing a section
    proc done(): void =
        if sectionValid and section[2].len != 0:
            # Add the 'last' bit into the last word of microcode
            section[2][section[2].len - 1] |= MC0.last.uint16
            for i in section[0]:
                sections[uint((i.int shl 8) or (if section[1]: 0x10 else: 0x00))] = section[2]
        sectionValid = false

    for c in codeLines:
        let
            line = c.code
            lineNumber = c.line
            file = c.file

        if line == ".MICROCODE":
            continue
        elif line[line.len-1] == ':':
            if line[0] == '.':
                assemblerAssert(sectionValid, "'.' section without parent", file, lineNumber)
                assemblerAssert(line[1..line.len-2] in ["CONST", "ELSE"], "Invalid '.' section name", file, lineNumber)
                if line[1..line.len-2] == "CONST":
                    section[1] = true
                else:
                    done()
                    section = (section[0], false, @[])
                    sectionValid = true
            else:
                done()
                let instructions = line.assemblerTokenize()
                    .map(proc (tk: string): string = tk.replace(":", ""))
                    .map(proc (tk: string): Instruction =
                        try: return parseEnum[Instruction](tk)
                        except: assemblerAssert(false, "Invalid instruction", file, lineNumber)
                        return Instruction.PUSH
                    )
                section = (instructions, false, @[])
                sectionValid = true
        else:
            assemblerAssert(sectionValid, "Orphaned microcode word (not in a section)", file, lineNumber)
            section[2] &= line.getMCWord(file, lineNumber)

    # Process whatever the last section was
    done()

    # Fill in the resultant byte sequence
    result = @[]
    for i in 0..(max(toSeq(sections.keys())) + 32):
        block add:
            for k, v in sections.pairs():
                if i in k..(k + v.len.uint - 1):
                    result &= uint8(v[int(i - k)] and 0xFF)
                    result &= uint8(v[int(i - k)] shr 8)
                    break add
            result &= @[0.uint8, 0.uint8]