import strutils, sequtils, tables, macros, typetraits
import ../../common/jmc, ../../common/util
import assemblerutil

type
    Macro* = object
        name*: string
        parameters*: seq[MacroParameter]
        lines*: seq[CodeLine]

        # For processing and instruction matching
        # InDiVidual parameters and their type sets
        idvParams*: seq[Param]
        idvParamTypeSets*: seq[set[SymbolType]]

    MacroParameter = object
        case isAddress*: bool
        of true: internalParameters*: seq[MacroParameter]
        of false: name*: string

# Gets macros from macro definition code
proc getMacros*(codeLines: seq[CodeLine]): seq[Macro] =
    result = @[]

    var
        currentMacroValid = false
        currentMacro = Macro(name: "", parameters: @[], lines: @[])

    for cl in codeLines.items():
        let
            file = cl.file
            line = cl.line
            code = cl.code

        if code[code.len - 1] == ':':
            if currentMacroValid:
                result &= currentMacro
                currentMacro = Macro(name: "", parameters: @[], lines: @[])
            
            let tokens = code.assemblerTokenize().mapIt(it.strip().replace(":", ""))
            currentMacroValid = true
            currentMacro.name = tokens[0]
            if tokens.len > 1:
                for token in tokens[1..tokens.len-1]:
                    if token[0] == '[' and token[token.len-1] == ']':
                        let ip = token[1..token.len-2].split(" ").map(
                            proc(t: string): MacroParameter = MacroParameter(isAddress: false, name: t)
                        )

                        currentMacro.parameters &= MacroParameter(isAddress: true, internalParameters: ip)
                    else:
                        currentMacro.parameters &= MacroParameter(isAddress: false, name: token)
        elif currentMacroValid:
            currentMacro.lines &= CodeLine(file: file, line: line, code: code, fromMacro: true, macroFile: file, macroLine: line)

    if currentMacroValid:
        result &= currentMacro

    # Check macro parameters for correct definiton format
    proc isValidParameter(p: string): bool =
        p.len == 3 and p[0] == '%' and
            p[1] in {'R', 'I', 'X'} and p[2] in Digits

    for m in result.mitems():
        # Check all parameters for validity
        var
            badParam: string
            checkFailed = false

        for p in m.parameters:
            if (p.isAddress and 
                p.internalParameters.anyIt(not it.name.isValidParameter())):
                checkFailed = true
                badParam = p.internalParameters.filterIt(not it.name.isValidParameter())[0].name
                break
            elif not p.isAddress and not p.name.isValidParameter():
                checkFailed = true
                badParam = p.name

        assemblerAssert(
            not checkFailed, "Invalid macro parameter " & badParam,
            m.lines[0].file, m.lines[0].line - 1
        )

        # Generate replacement data for this macro
        m.idvParams = concat(m.parameters.mapIt(
                if it.isAddress:
                    it.internalParameters.map(
                        proc (p: MacroParameter): Param = Param(name: p.name, inAddress: true)
                    )
                else:
                    @[Param(name: it.name, inAddress: false)]
            )
        )

        m.idvParamTypeSets = m.idvParams.mapIt(
            case $it.name[1]
            of "I": IntConstantSymbol + { SymbolType.Label }
            of "R": { SymbolType.Register }
            of "X": IntConstantSymbol + { SymbolType.Register }
            else: { 0.SymbolType } # Will never happen
        )