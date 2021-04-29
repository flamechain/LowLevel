import strutils, sequtils, tables
import ../../common/jmc, ../../common/util
import assemblerutil, assemblermc, assemblermacros

const
    DEFAULT_ORG = 0
    DEFAULT_MACROS = staticRead("macros.asm")

type Patch = tuple[label: string, location: uint, file: string, line: uint]

# Assembles a basic instruction into a sequence of bytes.
# Returns the sequence of bytes assembled into the instruction.
# Automatically adds any labels into the list of patches
proc assembleLine(file: string, line: uint, code: string, cl: CodeLine, location: uint, parentLabel: string, patches: var seq[Patch]): seq[uint8] =
    result = @[]
    let
        tokens = code.assemblerTokenize()
        opcodeName = tokens[0]
        opcode = parseEnum(opcodeName, Instruction.PUSH)
        argTypes = tokens[1..tokens.len-1].map(proc (t: string): SymbolType = t.getSymbolType(file, line))

    # Check to ensure a valid instruction
    try: discard parseEnum[Instruction](opcodeName)
    except: assemblerAssert(false, "Unknown instruction '" & opcodeName & "'", cl)

    # Load the first result byte with the opcode in the most significant 4 bits
    # All instruction bytes are structured this way
    result &= opcode.uint8 shl 4

    # Argument number and type checking
    template argCheck(expected: int, types: varargs[set[SymbolType]]): void =
        # Number check
        assemblerAssert(
            tokens.len == expected + 1,
            "Expected " & $expected & " arguments for instruction, got " & $(tokens.len - 1), cl
        )

        # Type check
        assert(expected == types.len)
        for i, s in types.pairs():
            assemblerAssert(argTypes[i] in s, "Incorrectly typed argument '" & tokens[i + 1] & "' (argument " & $(i + 1) & ")", cl)

    template processAddress(addressToken: string): void =
        assert(addressToken.getSymbolType(file, line) == SymbolType.Address)
        let
            addressValue = addressToken[1..addressToken.len-2].strip()
            addressType = addressValue.getSymbolType(file, line)

        assemblerAssert(
            addressType in { SymbolType.Label } + IntConstantSymbol,
            "Invalid memory address", cl
        )

        if addressType == SymbolType.Label:
            # Patch and leave space for two empty address bytes
            # Make '.' labels into '<parent>.<label>'
            patches &= (
                label: if addressValue[0] == '.': parentLabel & addressValue
                    else: addressValue,
                location: location + 1,
                file: file,
                line: line
            )
            result &= @[0.uint8, 0.uint8]
        else:
            # Emit the constant address in two 16-bit words. Low first since the machine is little-endian.
            let address16 = addressValue.getConstantValue(file, line).uint16
            result &= uint8(address16 and 0xFF)
            result &= uint8(address16 shr 8)

    # Arithmetic instructions
    if opcode in ({Instruction.ADD..Instruction.CMP} + { Instruction.MW }):
        argCheck(2, { SymbolType.Register }, { SymbolType.Register } + IntConstantSymbol)

        result[0] |= uint8(if argTypes[1] in IntConstantSymbol: 0x00 else: 0x08)
        result[0] |= parseEnum(tokens[1], Register.A).uint8

        # Store the constant in the second word
        if argTypes[1] in IntConstantSymbol:
            let cv = tokens[2].getConstantValue(file, line)
            assemblerAssert(cv <= 255, "Constant greater than 0xFF", cl)
            result &= cv.uint8
        else:
            result &= parseEnum(tokens[2], Register.A).uint8
    elif opcode == Instruction.PUSH or opcode == Instruction.JNZ:
        argCheck(1, { SymbolType.Register } + IntConstantSymbol)

        result[0] |= uint8(if argTypes[0] in IntConstantSymbol: 0x00 else: 0x08)

        if argTypes[0] in IntConstantSymbol:
            let cv = tokens[1].getConstantValue(file, line)
            assemblerAssert(cv <= 255, "Constant greater than 0xFF", cl)
            result &= cv.uint8
        else:
            result[0] |= parseEnum(tokens[1], Register.A).uint8
    elif opcode == Instruction.POP:
        argCheck(1, { SymbolType.Register })
        result[0] |= parseEnum(tokens[1], Register.A).uint8

        # Always set the Z/register bit becuase POP can only have a register argument
        result[0] |= 0x08.uint8
    elif opcode == Instruction.LW:
        result[0] |= parseEnum(tokens[1], Register.A).uint8
        if tokens.len == 2:
            argCheck(1, { SymbolType.Register })
            result[0] |= 0x08.uint8
        else:
            argCheck(2, { SymbolType.Register }, { SymbolType.Address })
            processAddress(tokens[2])
    elif opcode == Instruction.SW:
        result[0] |= parseEnum(tokens[if tokens.len == 2: 1 else: 2], Register.A).uint8
        if tokens.len == 2:
            argCheck(1, { SymbolType.Register })
            result[0] |= 0x08.uint8
        else:
            argCheck(2, { SymbolType.Address }, { SymbolType.Register })
            processAddress(tokens[1])
    elif opcode == Instruction.LDA:
        argCheck(1, { SymbolType.Address })
        processAddress(tokens[1])
    else:
        assemblerAssert(false, "Unknown instruction " & tokens[0], cl)

proc directive(line: string, lineFile: string, lineNumber: uint,
        location: var uint, org: var uint, defines: var TableRef[string, string]): seq[uint8] =
    # Currently recognized directives:
    # .org <imm> - Sets the origin of the program. Only to be used once per program.
    # .define <x> <y> - Defines <x> to be <y> and replaces all instances of 'x' with 'y'
    # .db <x> - Places bytes <x> into the program at the current location
    # .resb <x> - Reserves <x> number of bytes
    # .microcode - Denotes microcode instead of regular JMC-8 assembly
    # .include, .block, and .enblock are processed elsewhere as pseudo-directives
    let tokens = line.assemblerTokenize()
    case tokens[0][1..tokens[0].len-1]
    of "ORG":
        assemblerAssert(
            tokens.len == 2 and tokens[1].getSymbolType(lineFile, lineNumber) in IntConstantSymbol,
            "Invalid '.org' directive", lineFile, lineNumber
        )
        assemblerAssert(org == DEFAULT_ORG, "Only one '.org' directive per object file", lineFile, lineNumber)
        org = tokens[1].getConstantValue(lineFile, lineNumber).uint
    of "DEFINE":
        assemblerAssert(tokens.len == 3, "Invalid '.define' directive", lineFile, lineNumber)
        defines[tokens[1]] = tokens[2]
    of "DB":
        assemblerAssert(tokens.len > 1, "No value specified for '.db' directive", lineFile, lineNumber)
        assemblerAssert(
            tokens[1..tokens.len-1].all(
                proc (tk: string): bool = tk.getSymbolType(lineFile, lineNumber) in ({ SymbolType.StringLiteral } + IntConstantSymbol)
            ),
            "Invalid '.db' directive argument", lineFile, lineNumber
        )
        var bytes = newSeq[uint8]()
        for token in tokens[1..tokens.len-1]:
            if token.getSymbolType(lineFile, lineNumber) in IntConstantSymbol:
                let
                    constantValue = token.getConstantValue(lineFile, lineNumber)
                    byteCount =
                        if constantValue.uint in 0x00.uint..0xFF.uint: 1
                        elif constantValue.uint in 0x100.uint..0xFFFF.uint: 2
                        elif constantValue.uint in 0x10000.uint..0xFFFFFFFF.uint: 3
                        elif constantValue.uint in 0x1000000000.uint..0xFFFFFFFFFFFFFFFF.uint: 4
                        else: 0
                assemblerAssert(byteCount > 0, "Constant " & token & " larger than 64 bits", lineFile, lineNumber)
                for i in 0..byteCount-1: bytes &= uint8((constantValue shr (i * 8)) and 0xFF)
            else:
                for c in token[1..token.len-2]:
                    bytes &= c.uint8
        location += bytes.len.uint
        return bytes
    of "RESB":
        assemblerAssert(tokens[1].getSymbolType(lineFile, lineNumber) in IntConstantSymbol, "Invalid '.resb' directive", lineFile, lineNumber)
        let size = tokens[1].getConstantValue(lineFile, lineNumber)
        assemblerAssert(size > 0, "Cannot '.resb' a negative number of bytes", lineFile, lineNumber)
        location += size.uint
        return repeat(0.uint8, size)
    else: assemblerAssert(false, "Unknown directive " & tokens[0], lineFile, lineNumber)
    return @[]

# Assembles assembly code into a sequence of bytes
proc assemble*(file: string, code: string): seq[uint8] =
    # Process all macros
    let macros = getMacros(toCodeLines("DEFAULT_MACROS", DEFAULT_MACROS))

    var
        # Program origin. Only to be set once, otherwise it's at the default
        org: uint = DEFAULT_ORG

        # Current location in bytes
        location: uint = 0

        # Map of labels to their locations in bytes
        labels = newTable[string, uint]()

        # The last label to be defined. Used for labels with a preceding '.'.
        parentLabel: string = nil

        # List of constants that have been '.define'd
        defines = newTable[string, string]()

        # List of patches that need to be made at the end of the assebmly
        patches = newSeq[Patch]()

    # Check if this is supposed to be microcode
    var codeLines = toCodeLines(file, code)
    if codeLines.any(proc (c: CodeLine): bool = c.code.assemblerTokenize()[0] == ".MICROCODE"):
        return microcodeAssemble(codeLines)

    let byteSequences = codeLines
            .map do (c: CodeLine) -> seq[uint8]:
        proc codePreProcess(cs: string, file: string, line: uint, cl: CodeLine): string =
            result = cs

            # Process all '.define's and all '$' constants
            for k, v in defines.pairs():
                result = result.replace(k, v)

            # And replace and '$.h', '$.l', and '$'s with the current instruction's location
            result = result.replace("$.H", $int((org + location) shr 8))
            result = result.replace("$.L", $int((org + location) and 0xFF))
            result = result.replace("$", $int(org + location))

            # Process any constant expressions in parentheses
            result = result.processConstantExpressions(file, line, cl)

        let
            line = c.line
            file = c.file
            code = c.code.codePreProcess(file, line, c)

        if code[code.len - 1] == ':':
            # Processes labels
            # Labels with a preceding '.' are turned into children of the previous label in that their
            # internal representation is converted into <parent label> + <this label>.
            # So, the label '.loop' with the preceding label 'main' would be represented internally as
            # 'main.loop'.
            let labelValue = code[0..code.len-2]
            if code[0] == '.':
                assemblerAssert(parentLabel != nil, "Can't start program with a '.' label", c)
                labels[parentLabel & labelValue] = location
            else:
                parentLabel = labelValue
                labels[labelValue] = location
        elif code[0] == '.':
            return directive(code, file, line, location, org, defines)
        else:
            let
                tokens = code.assemblerTokenize()
                matches = macros.filterIt(it.name == tokens[0])

            # Generate the lines of code corresponding to this line
            let lineGen = proc(): seq[CodeLine] =
                if matches.len != 0:
                    # Determine the right match based on parameter types. Ignore address boxing.
                    let
                        lineParams = concat(tokens[1..tokens.len-1].mapIt(
                            if it.contains("["):
                                it.replace("[", "").replace("]", "").split(" ").map(proc(s: string): Param = Param(name: s, inAddress: true))
                            else:
                                @[Param(name: it, inAddress: false)]
                            )
                        )
                        lineArgTypes = lineParams.map(proc (lp: Param): auto = lp.name.getSymbolType(file, line))

                    var
                        foundMatch = false
                        match: Macro

                    for m in matches:
                        if lineArgTypes.len != m.idvParamTypeSets.len:
                            continue
                        

                        var failed = false
                        for i in 0..lineArgTypes.len-1:
                            if lineArgTypes[i] notin m.idvParamTypeSets[i] or
                                lineParams[i].inAddress != m.idvParams[i].inAddress:
                                failed = true
                                break

                        if not failed:
                            match = m
                            foundMatch = true

                    assemblerAssert(
                        foundMatch,
                        "Macro(s) with name " & tokens[0] & " found, but none with matching parameter types", c
                    )

                    # Perform the text replacement of parameters from the macro with their values in the current context
                    # Make sure the lines point to the macro file that they came from
                    var r = newSeq[CodeLine]()
                    for cl in match.lines:
                        var codeResult = cl.code
                        for i in 0..lineParams.len-1:
                            codeResult = codeResult.replace(match.idvParams[i].name, lineParams[i].name)
                        r &= CodeLine(file: file, line: line, code: codeResult, fromMacro: true, macroFile: cl.file, macroLine: cl.line)
                    return r
                else:
                    return @[CodeLine(file: file, line: line, code: code, fromMacro: false, macroFile: nil, macroLine: 0)]

            # Preprocess any extra lines that we may have due to this line being a macro
            var lines = lineGen()

            # Assemble the lines into their
            var assembled = newSeq[uint8]()
            for ln in lines.mitems():
                try:
                    # Preprocessing is done here so that the '$' symbol functions correctly
                    ln.code = codePreProcess(ln.code, ln.file, ln.line, ln)

                    # Location adding is also done here for the functionality of the '$' symbol
                    let asline = assembleLine(ln.file, ln.line, ln.code, ln, location, parentLabel, patches)
                    assembled &= asline
                    location += asline.len.uint
                except Exception:
                    if ln.fromMacro:
                        echo "(MACRO) from file " & ln.macroFile & " (" & $ln.macroLine & ")"
                    raise getCurrentException()
            return assembled
        return @[]

    result = byteSequences.concat()

    # Perform all patches
    for p in patches:
        assemblerAssert(p.label in labels, "Undefined label '" & p.label & "'", p.file, p.line)
        let labelAddress = org + labels[p.label]
        result[p.location.int] = uint8(labelAddress and 0xFF)
        result[p.location.int + 1] = uint8(labelAddress shr 8)