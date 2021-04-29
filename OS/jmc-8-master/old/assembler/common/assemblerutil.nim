import strutils, sequtils, tables, math
import ../../common/jmc, ../../common/util

when not defined(js):
    import os

type
    # Represents a parameter of any type
    # Can be either in an address (in between [] brackets) or on its own
    Param* = object
        inAddress*: bool
        name*: string

    CodeLine* = object
        file*: string
        line*: uint
        code*: string
        macroFile*: string
        macroLine*: uint
        fromMacro*: bool

# Throws an assembly exception
proc assemblerError*[T: SomeInteger](message: string, file: string, line: T): void =
    raise newException(Exception, "Error: " & message & " in file " & file & " (" & $(line.int) & ")")

# Assert specifically for the assembler
template assemblerAssert*[T: SomeInteger](condition: bool, message: string, file: string, line: T): void =
    if not condition:
        assemblerError(message, file, line)

template assemblerAssert*(condition: bool, message: string, cl: CodeLine): void =
    if not condition:
        let preMessage = if cl.fromMacro: "(From macro file $1 ($2))" % [cl.macroFile, $cl.macroLine] else: ""
        assemblerError(preMessage & message, cl.file, cl.line)

# Replaces strings with "STRING_<N>"
# Example: "I'm a \"string!\"" -> ("I'm a STRING_0", ["string!"])
proc replaceStrings*(str: string): (string, seq[string]) =
    var
        stringIndex = 0 
        currentString = ""
        inDQ = false
        inSQ = false

    result[0] = ""
    result[1] = @[]

    # Process the string per-character. If we aren't in any quotes and we
    # encounter a quote, then start building a string to add to the list.
    # Only pay attention to the relevant quote character that started
    # the string literal. Replace each string with a "STRING_N".
    for i, c in str.pairs():
        if not inSQ and c == '\"' and not (i != 0 and str[i - 1] == '\\'):
            if inDQ:
                result[1] &= "\"" & currentString & "\""
                currentString = ""
            else:
                result[0] &= "STRING_" & $stringIndex
                stringIndex += 1
            inDQ = not inDQ
        elif not inDQ and c == '\'' and not (i != 0 and str[i - 1] == '\\'):
            if inSQ:
                result[1] &= '\'' & currentString & '\''
                currentString = ""
            else:
                result[0] &= "STRING_" & $stringIndex
                stringIndex += 1
            inSQ = not inSQ
        elif inDQ or inSQ:
            currentString &= c
        else:
            result[0] &= c

# Undoes 'replaceStrings'
proc unreplaceStrings*(str: string, strings: seq[string]): string =
    result = str

    # This protects against, for instance, a fake string literal hidden in a
    # comment because if 'replace' fails to find the replacement string then
    # it will simply return the input string unchanged.
    for i in 0..strings.len-1:
        result = result.replace("STRING_" & $i, strings[i])

# Preprocesses lines of assembly code by:
# Removing comments
# Removing commas
# Converting all letters to uppercase (and ignoring strings!)
proc preProcess*(code: string): string {.procvar.} =
    # Ignore strings
    let (replaced, replacedStrings) = replaceStrings(code)
    
    # Remove comments by substring-ing to the rightmost ';'
    let decommented =
        if ';' in replaced: replaced[0..replaced.rfind(';')-1].strip()
        else: replaced

    # Remove commas and capitalize
    let unreplaced = decommented.replace(",", "").strip().toUpperAscii()

    # Undo string replacement and return
    return unreplaceStrings(unreplaced, replacedStrings)

# Tokenize but ignore tokens inside of brackets and whitespace inside of strings 
proc assemblerTokenize*(str: string): seq[string] =
    var
        inBrackets = false
        inDQ = false
        inSQ = false
        currentToken = ""

    result = @[]
    for i, c in str.pairs():
        if c == '\"' and not inSQ and not (i != 0 and str[i - 1] == '\\'):
            inDQ = not inDQ
        elif c == '\'' and not inDQ and not (i != 0 and str[i - 1] == '\\'):
            inSQ = not inSQ
        elif c == '[' and not inBrackets:
            inBrackets = true
        elif c == ']' and inBrackets:
            inBrackets = false

        if c in Whitespace and (not inBrackets) and (not inDQ) and (not inSQ):
            result &= currentToken
            currentToken = " "
        else:
            currentToken &= c
    result &= currentToken
    result = result.map(proc (str: string): string = str.strip())

# Types of symbols that can appear in assembly code
type SymbolType* {.pure.} = enum
    Label, DecConstant, HexConstant, BinConstant, CharConstant, Instruction, Register, StringLiteral, Address

# Symbols that are constants that have integer representation
const IntConstantSymbol* = { SymbolType.DecConstant, SymbolType.HexConstant, SymbolType.BinConstant, SymbolType.CharConstant }

# 'Labels' that refer to the current instruction's memory address 
const HereLabels* = ["$.h", "$.l", "$"]

# Determines if a string is a valid label
proc isValidLabel*(label: string): bool =
    return label in HereLabels or 
        (label[0] in ({'.'} + Letters) and (@label[1..label.len-1]).all(proc(c: char): bool = c in (Letters + Digits + {'_'})))

# Deduces the type of a symbol
proc getSymbolType*(symbol: string, file: string, line: uint): SymbolType =
    if symbol[0] == '[' and symbol[symbol.len-1] == ']':
        return SymbolType.Address
    elif symbol[0] == '\'' and symbol[symbol.len-1] == '\'' and symbol.len <= 4:
        return SymbolType.CharConstant
    elif symbol[0] == '\"' and symbol[symbol.len-1] == '\"':
        return SymbolType.StringLiteral
    elif symbol.startsWith("0B") and
        (@symbol[2..symbol.len-1]).all(proc(c: char): bool = c in {'0', '1'}):
        return SymbolType.BinConstant
    elif symbol.startsWith("0X") and
        (@symbol[2..symbol.len-1]).all(proc(c: char): bool = c in {'0'..'9', 'A'..'F'}):
        return SymbolType.HexConstant
    elif (@symbol).allIt(it.isDigit() or it in {'-'}):
        return SymbolType.DecConstant
    elif symbol in toSeq(items(Instruction)).map(proc (i: Instruction): string = $i):
        return SymbolType.Instruction
    elif symbol in toSeq(items(Register)).map(proc (r: Register): string = $r):
        return SymbolType.Register
    elif symbol.isValidLabel():
        return SymbolType.Label
    else:
        assemblerAssert(false, "Unknown symbol type for symbol '" & symbol & "'", file, line)

# Gets the value of a constant from its string representation
proc getConstantValue*(constant: string, file: string, line: uint): int =
    # Get the symbol type and type check it, but only in debug builds
    let constantType = constant.getSymbolType(file, line)
    assert(constantType in IntConstantSymbol)
    
    case constantType
    of SymbolType.CharConstant:
        let c = constant[1..constant.len-2]
        if c.len == 1:
            return c[0].int
        elif c[0] == '\\' and c[1] in {'\'', '\"', '\\', 'n', 'r', 't', 'b', 'f', 'v', '0'}:
            return case c[1]
            of '\'', '\"', '\\': c[1].int
            of 'n': 10
            of 'r': 13
            of 't': 9
            of 'b': 8
            of 'f': 12
            of 'v': 11
            of '0': 0
            else: 0
        raise newException(Exception, "Invalid escaped character constant '" & $c[1] & "'")
    of SymbolType.BinConstant:
        return constant.parseBinInt()
    of SymbolType.HexConstant:
        return constant.parseHexInt()
    of SymbolType.DecConstant:
        return constant.parseInt()
    else: assert false

proc toCodeLines*(file: string, code: string): seq[CodeLine] =
    let
        # Preprocessed
        ppCode = code.splitLines().map(preProcess)

        # Indexed and Included code
        iiCode = toSeq(ppCode.pairs()).map(proc (x: (int, string)): seq[CodeLine] =
                let
                    line = x[0]
                    str = x[1]
                if str.assemblerTokenize()[0] == ".INCLUDE":
                    when not defined(js):
                        let tokens = str.assemblerTokenize()
                        assemblerAssert(
                            tokens[1].getSymbolType(file, line.uint) == SymbolType.StringLiteral,
                            "Invalid filename for '.include' statement",
                            file, line
                        )
                        # Include this file's code lines recursively
                        let
                            sp = splitPath(file)
                            fp = joinPath(if sp[0].len == 0: "." else: sp[0], tokens[1][1..tokens[1].len-2])
                        return toCodeLines(fp, readFile(fp))
                    else:
                        assemblerAssert(false, ".include directive not allowed in JS assembler", file, line + 1)
                else:
                    return @[CodeLine(file: file, line: line.uint + 1, code: str, fromMacro: false, macroFile: nil, macroLine: 0)]
            )

    # Concatentate the seq[seq[CodeLine]] into a seq[CodeLine]
    # Filter out any empty lines
    result = iiCode
            .concat()
            .filter(proc (c: CodeLine): bool = c.code.len != 0)

    # Block-out lines that are between .block and .endblock directives
    var inBlock = false
    result = result.filter(proc (c: CodeLine): bool =
            let
                token0 = c.code.assemblerTokenize()[0]
                ib = inBlock

            if token0 == ".BLOCK":
                inBlock = true
            elif token0 == ".ENDBLOCK":
                assemblerAssert(inBlock, ".endblock without matching .block", c)
                inBlock = false

            return not (ib or inblock)
        )

# Processes any basic mathmatical expressions contained in parentheses
# Can handle operators +, -, *, /, %, and ^
proc processConstantExpressions*(str: string, file: string, line: uint, cl: CodeLine): string =
    # Returns a list of all parenthesized expressions and their locations
    # NOTE: Only finds top-level expressions. Use recursive parsing to find inner expressions.
    proc findExpressions(str: string): seq[string] =
        result = @[]    
        var
            inParens: bool
            currentExpression = ""
            nestLayers = 0
        
        for c in str:
            if c == '(':
                inc nestLayers
            elif c == ')':
                dec nestLayers

            if c == '(' and not inParens:
                inParens = true
            elif c == ')' and inParens and nestLayers == 0:
                inParens = false
                result &= (currentExpression & ")")
                currentExpression = ""

            if inParens:
                currentExpression &= $c

        if currentExpression.len != 0:
            result &= currentExpression

        result = result.mapIt(it.strip())

    # Process constant expressions
    proc process(s: string): int =
        # Recursively process any internal expressions until we are left with only top-level ones
        var ss = s[1..s.len-2]
        for expression in findExpressions(ss):
            ss = ss.replace(expression, $process(expression))

        # Disregard any order of operations. Always parenthesize! Process from left to right
        const Operators = {'+', '-', '*', '/', '%', '^', '<', '>', '&', '|', '~'}

        assemblerAssert(
            (@ss).allIt(it in Digits + HexDigits + Whitespace + Operators + { 'X' }),
            "Invalid character in constant parenthesized expression",
            cl
        )

        # Remove spaces, we're going to add our own
        ss = ss.replace(" ", "")

        # Add spaces around Operators so we can tokenize
        # Only add a right side space to '-' and '~' if they are not preceded by another operator
        # This maintains the integrity of negative numbers
        var spaced = ""
        for i, c in ss.pairs():
            if c in Operators:
                if (c == '-' or c == '~') and (i == 0 or ss[i - 1] in Operators):
                    spaced &= " " & $c
                else:
                    spaced &= " " & $c & " "
            else:
                spaced &= c

        # Process '~'d expressions
        let nTokens = spaced.split(" ").mapIt(it.strip()).filterIt(it[0] == '~')
        for tk in nTokens:
            spaced = spaced.replace(tk, $(not getConstantValue(tk[1..tk.len-1], file, line).int))

        # Use an accumulator to carry the value left to right
        var
            tokens = spaced.split(" ").mapIt(it.strip()).filterIt(it.len != 0)
            accumulator = getConstantValue(tokens[0], file, line).int

        # Delete the accumulator string (first token)
        tokens.delete(0)

        # Crawl gradually to the left while consuming each operator and token in sequence
        while tokens.len > 0:
            assemblerAssert(tokens.len >= 2, "Uneven number of operands in constant expression", cl)

            let
                op = tokens[0]
                rhs = getConstantValue(tokens[1], file, line).int
            
            # Remove the two tokens just consumed
            for i in 0..1: tokens.delete(0)

            assemblerAssert(op.len == 1 and op[0] in Operators, "Invalid operator in constant expression", cl)

            case op[0]
            of '+': accumulator += rhs
            of '-': accumulator -= rhs
            of '*': accumulator *= rhs
            of '/': accumulator = accumulator div rhs
            of '%': accumulator = accumulator mod rhs
            of '^': accumulator = pow(accumulator.float, rhs.float).int
            of '<': accumulator = accumulator shl rhs
            of '>': accumulator = accumulator shr rhs
            of '&': accumulator = accumulator and rhs
            of '|': accumulator = accumulator or rhs
            else: assert false

        return accumulator

    result = str
    for expression in findExpressions(str):
        result = result.replace(expression, $process(expression))