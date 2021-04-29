import macros, strutils, algorithm, math

# @TODO This is bad
proc `|=`*[S, T](s: var S, t: T): void = s = s or t

proc rfind*(s: string, sub: set[char], start: int = -1): int {.noSideEffect.} =
  ## Searches for `sub` in `s` in reverse starting at position `start`.
  ##
  ## Searching is case-sensitive. If `sub` is not in `s`, -1 is returned.
  let realStart = if start == -1: s.len-1 else: start
  for i in countdown(realStart, 0):
    if s[i] in sub: return i
  return -1

## Seriously? This isn't in the Nim stdlib????
# @TODO Commit this to Nim's strutils...
proc parseBinInt*(s: string): int {.noSideEffect, procvar.} =
    var
        start = 0
        ignoredPlaces = 0
    if s[0] == '0' and (s[1] in {'b', 'B'}): start = 2
    for i, c in (@s[start..s.len-1]).reversed().pairs():
        if c == '_': inc(ignoredPlaces)
        result += pow(2, float(i - ignoredPlaces)).int * (if c == '1': 1 else: 0)

## Gets a proc's name from its NimNode
proc getProcName*(n: NimNode): string =
    return $(if n[0].kind == nnkPostFix: n[0][1] else: n[0]).ident

## Gets a proc's return type name from its NimNode
proc getProcReturnType*(n: NimNode): string =
    return $n[3][0].ident

## Extracts names from a parameter node
## Example: x, y: int -> "x, y"
##          x: int -> "x"
proc getParamName(n: NimNode): string =
    result = ""
    assert n.kind == nnkIdentDefs
    for i in 0..n.len-1:
        # Skip the second to last (type identifier) and last (default value) nodes
        if i + 2 < n.len:
            result &= $n[i]

        # If there's another parameter name after this one, add a comma
        if i + 2 < n.len-1:
            result &= ", "

## Declares a constructor. For ease of use with 'ref object' types.
## Delcaration should match this:
## proc constructor(self: T, a: A, b: B, c, d: Z): void {.ctor.} = ...
macro ctor*(c: expr): stmt {.immediate.} =
    let
        # Formal parameters node
        fp = c[3]
        ctorType = fp[1][1]
        ctorName = getProcName(c)

    # Get the params from the constructor proc. Skip the return type (index 0).
    var paramNames = ""
    for i in 1..fp.len-1:
        # Skip nodes not related to proc parameters and skip the 'self' param
        if fp[i].kind != nnkIdentDefs or
            (fp[i].kind == nnkIdentDefs and $fp[i][0] == "self"):
            continue

        paramNames &= getParamName(fp[i])

        # Add a comma if there are more parameters to follow
        if (i + 1) != fp.len and fp[i + 1].kind == nnkIdentDefs:
            paramNames &= ", "

    # Generate an AST for the 'new' proc
    var newProc = parseStmt("""
        proc `new`(t: type(X)): X =
            new(result)
            $1(result, $2)
    """ % [ctorName, paramNames])

    # Export the 'new' function only if the constructor is exported
    if c[0].kind == nnkPostFix:
        newProc[0][0] = newNimNode(nnkPostFix)
        newProc[0][0].add(newIdentNode("*"))
        newProc[0][0].add(newNimNode(nnkAccQuoted))
        newProc[0][0][1].add(newIdentNode("new"))

    # 'new' proc formal params
    var npfp = newProc[0][3]

    # Replace 'X' with the constructor's type
    npfp[0] = ctorType
    npfp[1][1][1] = ctorType

    # Seek to the index of the formal params node at which we need to start adding parameters
    # Start at 1 so that we skip past the return type of the constructor (void)
    var addIndex = 1
    while addIndex < npfp.len and npfp[addIndex].kind == nnkIdentDefs:
        inc(addIndex)

    # Steal the parameters off of the constructor's AST add append them on to the AST of the new proc
    # Exclude the return type(1) and 'self' parameter(2)
    for i in 2..fp.len-1:
        npfp.insert(addIndex, fp[i])
        inc(addIndex)

    # Add the generic parameters of the constructor to the new proc if they exist
    if c[2].len > 0:
        newProc[0][2] = c[2]

    # Add the original constructor and the overridden 'new' proc to the AST
    result = newStmtList()
    result.add(c)
    result.add(newProc)